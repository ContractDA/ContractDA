.. ContractDA documentation master file, created by
   sphinx-quickstart on Tue Mar  5 11:57:03 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ContractDA's documentation!
======================================

**ContractDA** is a project under development, aiming to create a design automation tool for contract-based design.
The tool features specification, verification, simulation, and synthesis of contracts.


- Specification: ContractDA will support assume-guarantee contracts and constraint-behavior contracts [MEMOCODE23_1]_ for specifying different types of cyber-physical systems.
- Verification: ContractDA will support verification of the correctness of contracts in terms of consistency, compatibility, and risks in independent design [MEMOCODE23_2]_.
- Simulation: Given contracts for a design, ContractDA allows contract-level simulation to obtain an estimation of the design performance.
- Synthesis: Given a system specification, optimization criteria, and a library of available subsystems specified in contracts. ContractDA can select components to satisfy the design specification and optimize the criteria.

For more information, we recommend reading the following paper to understand the theories and background on design automation of contract-based design.

- “Constraint-Behavior Contracts: A Formalism for Specifying Physical Systems,” [MEMOCODE23_1]_ Sheng-Jung Yu, Inigo Incer, and Alberto Sangiovanni-Vincentelli, MEMOCODE, 2023.
- “Contract Replaceability for Ensuring Independent Design using Assume-Guarantee Contracts,” [MEMOCODE23_2]_ Sheng-Jung Yu, Inigo Incer, and Alberto Sangiovanni-Vincentelli, MEMOCODE, 2023.

Dependency and Development Environment:

- PDM_ for package management
- sphinx_ for documentation generation
- pytest_ for unit test

.. _PDM: https://pdm-project.org/latest/
.. _sphinx: https://www.sphinx-doc.org/en/master/index.html
.. _pytest: https://docs.pytest.org/en/8.0.x/contents.html

.. [MEMOCODE23_1] https://ieeexplore.ieee.org/document/10316201
.. [MEMOCODE23_2] https://ieeexplore.ieee.org/document/10316205

.. note::
   This Project is under active development

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

For more information, check out the :doc:`usage` section for further information, including how to :ref:`install <installation>` the project.

.. toctree::
   :maxdepth: 10
   :caption: Contents:

   usage
   api




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
