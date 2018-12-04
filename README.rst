XBlocker
========

("XBLOCK External Runtime")

An independently deployable Django application that implements an XBlock runtime.

Using with Docker Devstack
--------------------------

Prerequisite: Have your Open edX `Devstack <https://github.com/edx/devstack>`_ properly installed.

#. Clone this repo and ``cd`` into it.

#. Start the service.

   .. code::

       make dev.up


#. Run the provision command to install dependencies, migrate databases etc.

   .. code::

       make dev.provision

#. Run a shell on the container

   .. code::

       make xblocker-shell

#. To start the django developement server, from the shell on the container run:

   .. code::

       make runserver

#. The xblocker container is also added to the ``devstack_default`` docker network.
   This allows it to be accessed from any of the devstack containers as ``edx.devstack.xblocker``.
   Test this by running the following command from any devstack container shell:

   .. code::

       curl edx.devstack.xblocker:18222/api/v1/ -v

#. Run ``make`` to get a list of all available commands.

Get Help
--------

Ask questions and discuss this project on `Slack <https://openedx.slack.com/messages/general/>`_ or in the `edx-code Google Group <https://groups.google.com/forum/#!forum/edx-code>`_.

License
-------

The code in this repository is licensed under version 3 of the AGPL unless otherwise noted. Please see the LICENSE_ file for details.

.. _LICENSE: https://github.com/open-craft/xblocker/blob/master/LICENSE

How To Contribute
-----------------

Contributions are welcome. Please read `How To Contribute <https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst>`_ for details. Even though it was written with ``edx-platform`` in mind, these guidelines should be followed for Open edX code in general.

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org.
