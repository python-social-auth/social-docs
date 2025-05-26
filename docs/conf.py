extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]
templates_path = ["_templates"]
master_doc = "index"
project = "Python Social Auth"
project_copyright = "Python Social Auth team"
exclude_patterns = ["build"]
pygments_style = "sphinx"
html_theme = "furo"
html_logo = "images/logo.svg"
html_title = project
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
