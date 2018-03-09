#!/usr/bin/env python3

import os
import sys
import datetime

# import libmc
sys.path.insert(0, os.path.abspath('../../'))

import libmc

# Sphinx extensions.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.graphviz',
    'sphinx.ext.autosummary',
    'sphinx.ext.githubpages',
    'sphinxcontrib.napoleon'
]

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'libmc'
copyright = str(datetime.datetime.today().year) + ', ' + libmc.__author__
author = libmc.__author__

# The short X.Y version.
version = libmc.__version__

# The full version, including alpha/beta/rc tags.
release = libmc.__version__

# The theme to use for HTML pages.
html_theme = 'sphinx_rtd_theme'
