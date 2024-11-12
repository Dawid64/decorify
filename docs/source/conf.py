import sys
from pathlib import Path

sys.path.insert(0, str(Path('..', '..').resolve()))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Decorify'
copyright = '2024, Dawid Siera, Julian Mikołajczak, Michał Redmer, Adam Tomys'
author = 'Dawid Siera, Julian Mikołajczak, Michał Redmer, Adam Tomys'
release = '0.1.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

autoapi_dirs = ['../../decorify']
templates_path = ['_templates']
exclude_patterns = []
autoapi_keep_files = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
