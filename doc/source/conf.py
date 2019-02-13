import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx', 
    'sphinx.ext.coverage',
    'sphinx.ext.autosummary',
]

# Napoleon settings
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = False

project = 'dccd'
copyright = '2017-2019, Arthur Bernard'
author = 'Arthur Bernard'
version = 1.0
release = 1.0.0
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_theme_option = {
	'display_version': True,
    'prev_next_buttons_location': 'both',
    'style_external_links': True,
    'vcs_pageview_mode' : '',
    'style_nav_header_background': 'black',
    # Toc options
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': False,
    'titles_only': False,
    'github_url': 'https://github.com/ArthurBernard/Download_Crypto_Currencies_Data',
}
html_static_path = ['_static']
html_context = {
    "display_github": True, # Integrate GitHub
    "github_user": "ArthurBernard", # Username
    "github_repo": "Download_Crypto_Currencies_Data", # Repo name
    "github_version": "master", # Version
    "conf_py_path": "/source/", # Path in the checkout to the docs root
}

autosummary_generate = True