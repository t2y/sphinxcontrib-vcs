Git directive
=============

.. contents:: contents
   :local:

Options
-------

The repository directive takes these options.

- **number_of_revisions**: positive integer

  Set the number of revision to show commit history. Default is 10.

- **revision**: revision string

  Set revision string to show particular commit history.

- **with_ref_url**:

  Set as a flag to show commit URL on repository hosting service.
  It supports github_ and bitbucket_.

.. _github: https://github.com/
.. _bitbucket: https://bitbucket.org/

- **include_diff**:

  Set as a flag to show diff text with commit history.
  The diff text is hidden with initial state.
  Clicking around commit message shows the diff text.

Top commit history
------------------

::

    .. git::
        :number_of_revisions: 20
        :with_ref_url:
        :include_diff:


.. git::
    :number_of_revisions: 20
    :with_ref_url:
    :include_diff:


Particular commit log
---------------------

::

    .. git::
        :revision: 33e6b629ed3d6ed63f64136661642f594b1f4d6f
        :with_ref_url:
        :include_diff:


.. git::
    :revision: 33e6b629ed3d6ed63f64136661642f594b1f4d6f
    :with_ref_url:
    :include_diff:

