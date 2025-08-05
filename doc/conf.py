# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import importlib.metadata

project = "darfix"
release = importlib.metadata.version(project)
version = ".".join(release.split(".")[:2])
copyright = "2019-2025, ESRF"
author = "ESRF"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.doctest",
    "sphinx_autodoc_typehints",
    "sphinxcontrib.video",
    "nbsphinx",
    "recommonmark",
    "ewokssphinx",
    "sphinx_design",
]
templates_path = ["_templates"]
exclude_patterns = []

source_suffix = [".rst", ".md"]

always_document_param_types = True

autosummary_generate = True
autodoc_default_flags = [
    "members",
    "undoc-members",
    "show-inheritance",
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_title = f"{project} {version}"
html_static_path = ["_static"]
html_logo = "img/darfix_icon8.png"
html_theme_options = {
    "logo": {"text": html_title},
    "icon_links": [
        {
            "name": "gitlab",
            "url": "https://gitlab.esrf.fr/XRD/darfix",
            "icon": "fa-brands fa-gitlab",
        },
        {
            "name": "pypi",
            "url": "https://pypi.org/project/darfix",
            "icon": "fa-brands fa-python",
        },
    ],
    "footer_start": ["copyright"],
}
