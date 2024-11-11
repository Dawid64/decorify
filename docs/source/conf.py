import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

project = 'pydecorators'
copyright = '2024, Dawid Siera, Julian Mikołajczak, Michał Redmer, Adam Tomys'
author = 'Dawid Siera, Julian Mikołajczak, Michał Redmer, Adam Tomys'
release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    "sphinx.ext.viewcode",
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '../tests']
# autodoc_mock_imports = ["pydecorators.basic"]

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
