# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest
import six


def test_simple_run(flake8dir):
    flake8dir.make_py_files(
        example="""
        x  = 1
        """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        './example.py:1:2: E221 multiple spaces before operator'
    ]


def test_make_py_files_no_positional_args(flake8dir):
    with pytest.raises(TypeError) as excinfo:
        flake8dir.make_py_files(1, example="""
            x  = 1
        """)
    assert 'make_py_files takes no positional arguments' in six.text_type(excinfo.value)


def test_make_py_files_requires_at_least_one_kwarg(flake8dir):
    with pytest.raises(TypeError) as excinfo:
        flake8dir.make_py_files()
    assert 'make_py_files requires at least one keyword argument' in six.text_type(excinfo.value)


def test_passing_args(flake8dir):
    flake8dir.make_py_files(
        example="""
        x  = 1
        """
    )
    result = flake8dir.run_flake8(extra_args=['--ignore', 'E221'])
    assert result.out_lines == []


def test_setup_cfg(flake8dir):
    flake8dir.make_setup_cfg("""
        [flake8]
        ignore = E221
    """)
    flake8dir.make_py_files(
        example="""
        x  = 1
        """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []
