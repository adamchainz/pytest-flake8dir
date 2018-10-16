.. :changelog:

History
=======

Pending Release
---------------

.. Insert new release notes below this line

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
