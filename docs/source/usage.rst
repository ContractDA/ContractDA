Usage 
=====

.. _installation:

Installation
------------

To develop for ContractDA, first install pdm using pip:

.. code-block:: console

   $ pip install pdm

Then, install the project and all the required dependencies

.. code-block:: console

   $ pdm install

After installation, the tool should be ready for development.
You can use either pdm or directly activate the virtual environment.
For example, to use pdm to call the python inside the virtual environment:

.. code-block:: console

   $ pdm run python

For another example, to activate the virtual environment and then run python:

.. code-block:: console

   $ source .venv/bin/activate
   $ python 