================
pytest-flake8dir
================

.. image:: https://img.shields.io/travis/adamchainz/pytest-flake8dir/master.svg
        :target: https://travis-ci.org/adamchainz/pytest-flake8dir

.. image:: https://img.shields.io/pypi/v/pytest-flake8dir.svg
        :target: https://pypi.python.org/pypi/pytest-flake8dir

A pytest fixture for testing flake8 plugins.

A quick example:

.. code-block:: python

    def test_something(flake8dir):
        flake8dir.makepyfile(
            example="""
            x  = 1
            """
        )
        out = flake8dir.run_flake8()
        assert out.errors == [
            'example.py:1:2: E221 multiple spaces before operator'
        ]

Installation
============

Use **pip**:

.. code-block:: sh

    pip install pytest-flake8dir

Tested on Python 2.7 and Python 3.6.

API
===

``flake8dir`` fixture
---------------------

A pytest fixture extending Pytest's built-in ``tmpdir`` fixture
(`docs <https://docs.pytest.org/en/latest/tmpdir.html>`_), with extra
behaviour for running flake8 and parsing the output.

Use the standard ``tmpdir`` behaviour to set up your python file(s) to be
linted with ``flake8``, then call the ``run_flake8()`` method to get back a
``Flake8Result``.

``Flake8Result``
----------------

Represents the parsed output of a flake8 run.

The ``errors`` attribute containsa list of the error lines that ``flake8``
output.

.. _tmpdir: https://docs.pytest.org/en/latest/tmpdir.html
