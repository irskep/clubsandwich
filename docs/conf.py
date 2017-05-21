import os

READ_THE_DOCS = os.environ.get('READTHEDOCS', None) == 'True'

needs_sphinx = '1.5'

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.intersphinx', 'sphinx.ext.ifconfig']
intersphinx_mapping = {}

templates_path = ['_templates']
exclude_patterns = ['_build']
source_suffix = '.rst'
master_doc = 'index'
#pygments_style = 'sphinx'

# project info

project = u'clubsandwich'
copyright = u'2017 Steve Johnson'
# The short X.Y version. Can refer to in docs with |version|.
version = '0.1.0'
# The full version, including alpha/beta/rc tags.
# Can refer to in docs with |release|.
release = '0.1.0'
#language = None

html_title = "%(project)s v%(release)s docs - roguelike framework for Python" % {
    'project': project, 'release': release}
html_short_title = "Home"

# Necessary for best search results
html_show_sourcelink = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'csdoc'

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
    ],
}

html_theme_options = {
    'github_user': 'irskep',
    'github_repo': 'clubsandwich',
    'github_button': True,
    'github_count': False,
    'github_banner': True,
    'canonical_url': 'http://steveasleep.com/clubsandwich/',
    'description': "A roguelike framework for Python 3 using BearLibTerminal",
    'sidebar_collapse': False,
    'show_related': True,
    'fixed_sidebar': True,
    'page_width': '960px',
    'analytics_id': 'UA-4517625-6',
}