extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
project = "Python Social Auth"
copyright = "2012, Matías Aguirre"
exclude_patterns = ["build"]
pygments_style = "sphinx"
html_theme = "pyramid"
html_static_path = []
htmlhelp_basename = "PythonSocialAuthdoc"
latex_documents = [
    (
        "index",
        "PythonSocialAuth.tex",
        "Python Social Auth Documentation",
        "Matías Aguirre",
        "manual",
    )
]
man_pages = [
    (
        "index",
        "pythonsocialauth",
        "Python Social Auth Documentation",
        ["Matías Aguirre"],
        1,
    )
]
intersphinx_mapping = {
    "python": ("http://docs.python.org/", None),
}
