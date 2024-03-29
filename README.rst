================
pytest-flake8dir
================

.. image:: https://img.shields.io/github/workflow/status/adamchainz/pytest-flake8dir/CI/main?style=for-the-badge
   :target: https://github.com/adamchainz/pytest-flake8dir/actions?workflow=CI

.. image:: https://img.shields.io/pypi/v/pytest-flake8dir.svg?style=for-the-badge
   :target: https://pypi.org/project/pytest-flake8dir/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
   :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

----

**Unmaintained:** Following temporary directory fixture changes in pytest, I
made a successor library,
`pytest-flake8-path <https://pypi.org/project/pytest-flake8-path/>`__. I
recommend you use that instead.

----

A pytest fixture for testing flake8 plugins.

A quick example:

.. code-block:: python

    def test_simple_run(flake8dir):
        flake8dir.make_example_py(
            """
            x  = 1
        """
        )
        result = flake8dir.run_flake8()
        assert result.out_lines == [
            "./example.py:1:2: E221 multiple spaces before operator"
        ]

Installation
============

Use **pip**:

.. code-block:: sh

    python -m pip install pytest-flake8dir

Python 3.6 to 3.10 supported.

----

**Working on a Django project?**
Check out my book `Speed Up Your Django Tests <https://gumroad.com/l/suydt>`__ which covers loads of best practices so you can write faster, more accurate tests.

----

API
===

``flake8dir`` fixture
---------------------

A pytest fixture that wraps Pytest's built-in ``tmpdir`` fixture
(`docs <https://docs.pytest.org/en/latest/tmpdir.html>`__), to create a
temporary directory, allow adding files, and running flake8.

If you're using this to test a flake8 plugin, make sure flake8 is picking up
your plugin during tests. Normally this is done with a ``setup.py`` entrypoint,
which makes ``tox`` the easiest way to guarantee this is ready as it will run
``setup.py install`` on your project before running tests.

``flake8dir.make_py_files(**kwargs: str) -> None``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creates one python file for each passed keyword argument, with name
corresponding to the keyword argument + '.py', and content according the string
value of the argument. The value will be processed with ``textwrap.dedent()``
so mixed indentation is not a problem in your test files.

For example, this creates two python files in the temporary directory, called
``example1.py`` and ``example2.py``, each containing one line with an
assignment:

.. code-block:: python

    def test_sample(flake8dir):
        flake8dir.make_py_files(
            example1="""
                x = 1
            """,
            example2="""
                y = 1
            """,
        )

``flake8dir.make_example_py(content: str) -> None``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A shortcut for ``make_py_files(example=content)``, for when you are using a
single file over and over. This creates just ``example.py``, which is often
all you need for testing a rule.

For example:

.. code-block:: python

    def test_sample(flake8dir):
        flake8dir.make_example_py(
            """
            x = 1
        """
        )

``flake8dir.make_setup_cfg(contents: str) -> str``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Makes the file ``setup.cfg`` in the test directory with contents equal to the
string passed in. This is again processed with ``textwrap.dedent()`` so
indentation is not a worry. You'll probably want to set the ``[flake8]``
section header to configure flake8.

For example, this makes flake8 ignore rule E101:

.. code-block:: python

    def test_sample(flake8dir):
        flake8dir.make_setup_cfg(
            """
            [flake8]
            ignore = E101
        """
        )

``flake8dir.make_file(filename: str, content: str) -> None``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make an arbitrary file with the given filename - this function is the inner
implementation for ``make_py_files`` and ``make_setup_cfg``. ``filename`` may
include directories, like ``mydir/foo.py``, and they will be created.
``content`` is subject to the same ``textwrap.dedent()`` processing as
mentioned above.

For example:

.. code-block:: python

    def test_sample(flake8dir):
        flake8dir.make_file(
            "myfile/foo.py",
            """
            x = 1
        """,
        )

``flake8dir.run_flake8(extra_args: list[str] | None = None) -> Flake8Result``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Runs flake8 and returns a ``Flake8Result`` representing the results.

``extra_args`` may be a list of extra flags to pass to flake8, for example
passing ``["--ignore", "E101"]`` would achieve the same thing as the above
``setup.cfg`` example. Note some arguments are already passed to ensure flake8
runs in an isolated manner - see source.


``Flake8Result``
----------------

Represents the parsed output of a flake8 run.

``Flake8Result.out: str``
~~~~~~~~~~~~~~~~~~~~~~~~~

The full string of output (stdout) generated by flake8.

``Flake8Result.err: str``
~~~~~~~~~~~~~~~~~~~~~~~~~

The full string of error output (stderr) generated by flake8.

``Flake8Result.exit_code: int``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The exit code that the flake8 run exited with.

``Flake8Result.out_lines: list[str]``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A list of individual lines of output, without trailing newlines. This is the
most useful tool for making assertions against.

For example, given a result you can check for a particular line being output:

.. code-block:: python

    result = flake8dir.run_flake8()
    expected = "./example.py:1:2: E221 multiple spaces before operator"
    assert expected in result.out_lines

``Flake8Result.err_lines: list[str]``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Like ``out_lines``, but for error output.
