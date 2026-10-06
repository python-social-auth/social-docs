extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_llm.txt",
]
llms_txt_description = (
    "Python Social Auth provides social authentication and authorization for Python "
    "applications. This documentation covers installation, framework integration, "
    "authentication providers, configuration, pipelines, and extension APIs."
)
llms_txt_full_build = True
llms_txt_suffix_mode = "auto"
llms_txt_nested_enabled = False
llms_txt_summary_enabled = False
# These unsupported nodes are omitted from Markdown; code blocks remain intact.
llms_txt_suppress_unknown_node_warnings = ["caption", "abbreviation"]
markdown_anchor_sections = True
markdown_anchor_signatures = True
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
    "python": ("https://docs.python.org/3/", None),
}
