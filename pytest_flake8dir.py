# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
from contextlib import contextmanager
from textwrap import dedent

import pytest
import six
from flake8.main.cli import main as flake8_main


__version__ = '1.0.0'


@pytest.fixture
def flake8dir(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('flake8dir')
    yield Flake8Dir(tmpdir)


class Flake8Dir(object):
    def __init__(self, tmpdir):
        self.tmpdir = tmpdir

    def make_py_files(self, *args, **kwargs):
        if len(args) != 0:
            raise TypeError('make_py_files takes no positional arguments')
        if len(kwargs) == 0:
            raise TypeError('make_py_files requires at least one keyword argument')

        for name, content in kwargs.items():
            path = self.tmpdir.join(name).new(ext='py')
            path.dirpath().ensure_dir()
            fixed_content = dedent(content).strip() + '\n'
            path.write(fixed_content.encode('utf-8'), 'wb')

    def make_setup_cfg(self, content):
        path = self.tmpdir.join('setup.cfg')
        path.dirpath().ensure_dir()
        fixed_content = dedent(content).strip() + '\n'
        path.write(fixed_content.encode('utf-8'), 'wb')

    def run_flake8(self, extra_args=None):
        args = [
            'flake8',
            '--jobs', '1',
            '--exit-zero',
            '.',
        ]
        if extra_args:
            args.extend(extra_args)

        with tmp_chdir(six.text_type(self.tmpdir)), patch_sys_argv(args), captured_stdout() as stdout:
            flake8_main()
        full_output = stdout.getvalue()
        return Flake8Result(full_output)


class Flake8Result(object):
    def __init__(self, out):
        self.out = out

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
def tmp_chdir(dir):
    orig = os.getcwd()
    os.chdir(dir)
    yield
    os.chdir(orig)


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
