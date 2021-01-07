# type: ignore
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
import importlib.metadata

metadata = importlib.metadata.metadata("LISA")

project = metadata["Name"].upper()
project_copyright = "Microsoft"  # TODO: Add year and verify.
author = metadata["Author"]
version = metadata["Version"]
release = version

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "recommonmark",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.githubpages",
    "sphinx.ext.linkcode",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
]

# Scan all found documents for autosummary directives, and generate
# stub pages for each, instead of using `sphinx-autogen` directly.
autosummary_generate = True


def linkcode_resolve(domain, info):
    """Configure linkcode extension."""
    if domain != "py":
        return None
    module = info["module"]
    if not module:
        return None

    # Map to subfolders.
    if module.startswith("lisa"):
        folder = "pytest-lisa"
    elif module.startswith("target"):
        folder = "pytest-target"
    elif module.startswith("playbook"):
        folder = "pytest-playbook"
    else:
        folder = ""

    filename = module.replace(".", "/")
    url = metadata["Project-Url"].split(", ")[1]
    # TODO: Update this branch to `main` branch after PR is merged.
    branch = "andschwa/pytest"
    return f"{url}/blob/{branch}/{folder}/{filename}.py"


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", ".archive", ".pytest_cache", "dist"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
