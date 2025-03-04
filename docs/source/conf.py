# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ContractDA'
copyright = '2024, Sheng-Jung Yu'
author = 'Sheng-Jung Yu'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary'
    ]

templates_path = ['_templates']
exclude_patterns = []

# -- Auto generation import --------------------------------------------------
import pathlib
import sys
# Generate autodoc stubs for functions and classes.
autoclass_content = 'both'
autosummary_generate = True
autodoc_member_order = 'groupwise'
sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
