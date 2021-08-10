import subprocess
import sys
from textwrap import dedent
from typing import Generator, List, Optional

import py
import pytest
from _pytest.tmpdir import TempdirFactory


class Flake8Result:
    def __init__(self, out: str, err: str, exit_code: int) -> None:
        self.out = out
        self.out_lines = out.strip().splitlines()
        self.err = err
        self.err_lines = err.strip().splitlines()
        self.exit_code = exit_code


class Flake8Dir:
    def __init__(self, tmpdir: py.path.local) -> None:
        self.tmpdir = tmpdir
        self.make_setup_cfg("[flake8]\n")

    def make_py_files(self, **kwargs: str) -> None:
        if len(kwargs) == 0:
            raise TypeError("make_py_files requires at least one keyword argument")

        for name, content in kwargs.items():
            self.make_file(name + ".py", content)

    def make_example_py(self, content: str) -> None:
        self.make_py_files(example=content)

    def make_setup_cfg(self, content: str) -> None:
        self.make_file("setup.cfg", content)

    def make_file(self, filename: str, content: str) -> None:
        path = self.tmpdir.join(filename)
        path.dirpath().ensure_dir()
        fixed_content = dedent(content).strip() + "\n"
        path.write(fixed_content.encode("utf-8"), "wb")

    def run_flake8(self, extra_args: Optional[List[str]] = None) -> Flake8Result:
        args = [
            sys.executable,
            "-m",
            "flake8",
            "--jobs",
            "1",
            "--config",
            "setup.cfg",
            ".",
        ]
        if extra_args:
            args.extend(extra_args)

        process = subprocess.Popen(
            args=args,
            cwd=str(self.tmpdir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        process.wait()

        # type narrowing
        assert process.stdout is not None
        assert process.stderr is not None

        return Flake8Result(
            out=process.stdout.read(),
            err=process.stderr.read(),
            exit_code=process.returncode,
        )


@pytest.fixture
def flake8dir(tmpdir_factory: TempdirFactory) -> Generator[Flake8Dir, None, None]:
    tmpdir = tmpdir_factory.mktemp("flake8dir")
    yield Flake8Dir(tmpdir)
