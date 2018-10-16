# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from contextlib import contextmanager
from textwrap import dedent

import pytest
import six
from flake8.main.cli import main as flake8_main


__version__ = '1.3.0'


@pytest.fixture
def flake8dir(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('flake8dir')
    yield Flake8Dir(tmpdir)


class Flake8Dir(object):
    def __init__(self, tmpdir):
        self.tmpdir = tmpdir
        self.make_setup_cfg('[flake8]\n')

    def make_py_files(self, *args, **kwargs):
        if len(args) != 0:
            raise TypeError('make_py_files takes no positional arguments')
        if len(kwargs) == 0:
            raise TypeError('make_py_files requires at least one keyword argument')

        for name, content in kwargs.items():
            self.make_file(name + '.py', content)

    def make_example_py(self, content):
        self.make_py_files(example=content)

    def make_setup_cfg(self, content):
        self.make_file('setup.cfg', content)

    def make_file(self, filename, content):
        path = self.tmpdir.join(filename)
        path.dirpath().ensure_dir()
        fixed_content = dedent(content).strip() + '\n'
        path.write(fixed_content.encode('utf-8'), 'wb')

    def run_flake8(self, extra_args=None):
        args = [
            'flake8',
            '--jobs', '1',
            '--config', 'setup.cfg',
            '.',
        ]
        if extra_args:
            args.extend(extra_args)

        exit_code = 0  # In case --exit-zero has been passed
        with self.tmpdir.as_cwd(), patch_sys_argv(args), captured_stdout() as stdout:
            try:
                flake8_main()
            except SystemExit as exc:
                exit_code = exc.code
        full_output = stdout.getvalue()
        return Flake8Result(full_output, exit_code)


class Flake8Result(object):
    def __init__(self, out, exit_code):
        self.out = out
        self.exit_code = exit_code

        lines = out.strip().split('\n')
        if lines[-1] == '':
            lines = lines[:-1]
        self.out_lines = lines


@contextmanager
def patch_sys_argv(new_argv):
    orig = sys.argv
    sys.argv = new_argv
    yield
    sys.argv = orig


@contextmanager
def captured_output(stream_name):
    """Return a context manager used by captured_stdout/stdin/stderr
    that temporarily replaces the sys stream *stream_name* with a StringIO.
    Note: This function and the following ``captured_std*`` are copied
          from CPython's ``test.support`` module."""
    orig_stdout = getattr(sys, stream_name)
    setattr(sys, stream_name, six.StringIO())
    try:
        yield getattr(sys, stream_name)
    finally:
        setattr(sys, stream_name, orig_stdout)


def captured_stdout():
    """Capture the output of sys.stdout:
       with captured_stdout() as stdout:
           print("hello")
       self.assertEqual(stdout.getvalue(), "hello\n")
    """
    return captured_output("stdout")
