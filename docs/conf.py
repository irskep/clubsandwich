import os

READ_THE_DOCS = os.environ.get('READTHEDOCS', None) == 'True'

needs_sphinx = '1.5'

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.intersphinx', 'sphinx.ext.ifconfig']
intersphinx_mapping = {}

#templates_path = ['_templates']
exclude_patterns = ['_build']
source_suffix = '.rst'
master_doc = 'index'
#pygments_style = 'sphinx'

# project info

project = u'clubsandwich'
copyright = u'2017 Steve Johnson'
# The short X.Y version. Can refer to in docs with |version|.
version = '0.1'
# The full version, including alpha/beta/rc tags.
# Can refer to in docs with |release|.
release = '0.1a1'
#language = None

html_title = "%(project)s v%(release)s docs - BearLibTerminal framework for Python" % {
    'project': project, 'release': release}
html_short_title = "Home"

#if not READ_THE_DOCS:
#    html_theme_options['ga_ua'] = 'UA-foo'
#    html_theme_options['ga_domain'] = 'bar'

# Necessary for best search results
html_show_sourcelink = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'csdoc'