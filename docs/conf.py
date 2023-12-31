# -- Project information -----------------------------------------------------
project = "gears"
copyright = "2023, Kazuya Takei"
author = "Kazuya Takei"
release = "0.0.0"

# -- General configuration ---------------------------------------------------
extensions = ["sphinx.ext.todo"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
