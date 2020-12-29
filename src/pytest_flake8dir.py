import os
from subprocess import Popen, PIPE
from textwrap import dedent
from pathlib import Path

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
        p = Path(path)
        with p.open(mode='wb') as fi:
            fi.write(fixed_content.encode("utf-8"))

    def run_flake8(self, extra_args=None, use_nt_paths=False):
        args = ["flake8", "--jobs", "1", "--config", "setup.cfg", "."]
        if extra_args:
            args.extend(extra_args)

        with Popen(
                args=args,
                cwd=str(self.tmpdir),
                stdout=PIPE,
                stderr=PIPE,
                universal_newlines=True) as process:
            process.wait()
            process_output = process.stdout.read()

            # Note: this will break tests using workarounds unless grandfathered in or opt-in feature flag used.
            if os.name == 'nt' and use_nt_paths:
                process_output = process_output.replace('\\', '/')

        return Flake8Result(process_output, process.returncode)


class Flake8Result:
    def __init__(self, out, exit_code):
        self.out = out
        self.exit_code = exit_code

        lines = out.strip().split("\n")
        if lines[-1] == "":
            lines = lines[:-1]
        self.out_lines = lines
