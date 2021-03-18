import subprocess
import sys
from textwrap import dedent

import pytest


@pytest.fixture
def flake8dir(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp("flake8dir")
    yield Flake8Dir(tmpdir)


class Flake8Dir:
    def __init__(self, tmpdir):
        self.tmpdir = tmpdir
        self.make_setup_cfg("[flake8]\n")

    def make_py_files(self, *args, **kwargs):
        if len(args) != 0:
            raise TypeError("make_py_files takes no positional arguments")
        if len(kwargs) == 0:
            raise TypeError("make_py_files requires at least one keyword argument")

        for name, content in kwargs.items():
            self.make_file(name + ".py", content)

    def make_example_py(self, content):
        self.make_py_files(example=content)

    def make_setup_cfg(self, content):
        self.make_file("setup.cfg", content)

    def make_file(self, filename, content):
        path = self.tmpdir.join(filename)
        path.dirpath().ensure_dir()
        fixed_content = dedent(content).strip() + "\n"
        path.write(fixed_content.encode("utf-8"), "wb")

    def run_flake8(self, extra_args=None):
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
        return Flake8Result(process.stdout.read(), process.returncode)


class Flake8Result:
    def __init__(self, out, exit_code):
        self.out = out
        self.exit_code = exit_code

        lines = out.strip().split("\n")
        if lines[-1] == "":
            lines = lines[:-1]
        self.out_lines = lines
