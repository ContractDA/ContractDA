# ContractDA

ContractDA is a project under development, aiming to create a design automation tool for contract-based design.
The tool features specification, verification, simulation, and synthesis of contracts.
*    Specification: ContractDA will support assume-guarantee contracts and [constraint-behavior contracts][CBContract23] for specifying different types of cyber-physical systems.
*    Verification: ContractDA will support verification of the correctness of contracts in terms of consistency, compatibility, and [risks in independent design][Independent23].
*    Simulation: Given contracts for a design, ContractDA allows contract-level simulation to obtain an estimation of the design performance.
*    Synthesis: Given a system specification, optimization criteria, and a library of available subsystems specified in contracts. ContractDA can select components to satisfy the design specification and optimize the criteria.

For more information, we recommend reading the following paper to understand the theories and background on design automation of contract-based design.
*    [“Constraint-Behavior Contracts: A Formalism for Specifying Physical Systems,”][CBContract23] Sheng-Jung Yu, Inigo Incer, and Alberto Sangiovanni-Vincentelli, MEMOCODE, 2023.
*    [“Contract Replaceability for Ensuring Independent Design using Assume-Guarantee Contracts,”][Independent23] Sheng-Jung Yu, Inigo Incer, and Alberto Sangiovanni-Vincentelli, MEMOCODE, 2023.

Dependency:

*    PDM for package management
*    sphinx for documentation generation


[CBcontract23]: https://ieeexplore.ieee.org/document/10316201
[Independent23]: https://ieeexplore.ieee.org/document/10316205
