import os
import flake8
import pytest


class TestPyTestFlake8Dir:
    def test_make_py_files_single(self, flake8dir):
        flake8dir.make_py_files(
            example="""
            x  = 1
        """
        )
        result = flake8dir.run_flake8()

        if os.name == 'nt':
            assert result.out_lines == [
                ".\\example.py:1:2: E221 multiple spaces before operator"
            ]
        else:
            assert result.out_lines == [
                "./example.py:1:2: E221 multiple spaces before operator"
            ]
        assert result.exit_code == 1

    def test_make_py_files_single_nt(self, flake8dir):
        flake8dir.make_py_files(
            example="""
            x  = 1
        """
        )
        result = flake8dir.run_flake8(use_nt_paths=True)

        if os.name == 'nt':
            assert result.out_lines == [
                "./example.py:1:2: E221 multiple spaces before operator"
            ]
        else:
            assert result.out_lines == [
                "./example.py:1:2: E221 multiple spaces before operator"
            ]
        assert result.exit_code == 1

    def test_make_py_files_double(self, flake8dir):
        flake8dir.make_py_files(
            example1="""
                x  = 1
            """,
            example2="""
                y  = 2
            """,
        )
        result = flake8dir.run_flake8()

        if os.name == 'nt':
            assert result.out_lines == [
                ".\\example1.py:1:2: E221 multiple spaces before operator",
                ".\\example2.py:1:2: E221 multiple spaces before operator",
            ]
        else:
            assert result.out_lines == [
                "./example1.py:1:2: E221 multiple spaces before operator",
                "./example2.py:1:2: E221 multiple spaces before operator",
            ]

    def test_make_py_files_no_positional_args(self, flake8dir):
        with pytest.raises(TypeError) as excinfo:
            flake8dir.make_py_files(
                1,
                example="""
                x  = 1
            """,
            )
        assert "make_py_files takes no positional arguments" in str(excinfo.value)

    def test_make_py_files_requires_at_least_one_kwarg(self, flake8dir):
        with pytest.raises(TypeError) as excinfo:
            flake8dir.make_py_files()
        assert "make_py_files requires at least one keyword argument" in str(excinfo.value)

    def test_make_example_py(self, flake8dir):
        flake8dir.make_example_py(
            """
            x  = 1
        """
        )
        result = flake8dir.run_flake8()

        if os.name == 'nt':
            assert result.out_lines == [
                ".\\example.py:1:2: E221 multiple spaces before operator"
            ]
        else:
            assert result.out_lines == [
                "./example.py:1:2: E221 multiple spaces before operator"
            ]

    def test_make_setup_cfg(self, flake8dir):
        flake8dir.make_setup_cfg(
            """
            [flake8]
            ignore = E221
        """
        )
        flake8dir.make_py_files(
            example="""
            x  = 1
            """
        )
        result = flake8dir.run_flake8()
        assert result.out_lines == []

    def test_make_file(self, flake8dir):
        flake8dir.make_file(
            "myexample.py",
            """
            x  = 1
        """,
        )
        result = flake8dir.run_flake8()

        if os.name == 'nt':
            assert result.out_lines == [
                ".\\myexample.py:1:2: E221 multiple spaces before operator"
            ]
        else:
            assert result.out_lines == [
                "./myexample.py:1:2: E221 multiple spaces before operator"
            ]

    def test_extra_args(self, flake8dir):
        flake8dir.make_py_files(
            example="""
            x  = 1
            """
        )
        result = flake8dir.run_flake8(extra_args=["--ignore", "E221"])
        assert result.out_lines == []

    def test_extra_args_version(self, flake8dir):
        result = flake8dir.run_flake8(extra_args=["--version"])
        assert result.out.startswith(flake8.__version__ + " ")

    def test_separate_tmpdir(self, flake8dir, tmpdir):
        flake8dir.make_py_files(
            example="""
            x  = 1
            """
        )
        assert not tmpdir.join("example.py").check()
