=======
History
=======

2.3.1 (2021-03-18)
------------------

* Use sys.executable to invoke flake8. This ensures that we run the flake8
  installed to match the current interpreter, in multi-interpreter
  environments.

2.3.0 (2020-12-13)
------------------

* Drop Python 3.5 support.
* Support Python 3.9.
* Move license from ISC to MIT License.

2.2.0 (2019-12-19)
------------------

* Update Python support to 3.5-3.8, as 3.4 has reached its end of life.
* Converted setuptools metadata to configuration file. This meant removing the
  ``__version__`` attribute from the package. If you want to inspect the
  installed version, use
  ``importlib.metadata.version("pytest-flake8dir")``
  (`docs <https://docs.python.org/3.8/library/importlib.metadata.html#distribution-versions>`__ /
  `backport <https://pypi.org/project/importlib-metadata/>`__).

2.1.0 (2019-04-13)
------------------

* Run ``flake8`` in a ``subprocess`` rather than trying to get a speed boost by
  running it in the current process. This is to overcome plugin state not
  resetting in-process in ``flake8`` 3.7.0+.

2.0.0 (2019-02-28)
------------------

* Drop Python 2 support, only Python 3.4+ is supported now.

1.3.0 (2018-10-16)
------------------

* A temporary ``setup.cfg`` file is now always created with no options and
  passed as ``--config``, to avoid flake8 merging in user-specific settings.
  Use ``make_setup_cfg`` to set the contents of this file.

1.2.0 (2018-02-25)
------------------

* The exit code from ``flake8`` is now saved on the ``Flake8Result`` object.
  Any tests that relied on catching ``SystemExit`` themselves will need
  refactoring to use the new attribute for their assertions.

1.1.0 (2017-06-23)
------------------

* Add convenience methods ``make_example_py`` and ``make_file``.

1.0.0 (2017-06-22)
------------------

* First version with basic fixture supporting ``make_py_files``,
  ``make_setup_cfg`` and ``run_flake8``.
