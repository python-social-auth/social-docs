# Python Social Auth - Documentation

Python Social Auth is an easy to setup social authentication/registration
mechanism with support for several frameworks and auth providers.

## Description

This is the documentation repository for the
[social-auth ecosystem](https://github.com/python-social-auth/social-core).

## Documentation

Project documentation is available at <https://python-social-auth.readthedocs.io/>.

For AI assistants, use the [documentation index](https://python-social-auth.readthedocs.io/llms.txt)
to find individual Markdown pages, or download the
[complete documentation](https://python-social-auth.readthedocs.io/llms-full.txt)
as a single Markdown file. These exports are generated from the same sources as
the HTML documentation.

To build the documentation locally:

```sh
uv sync --group docs
uv run --group docs sphinx-build -b html -W docs docs/_build/html
```

The HTML pages, Markdown pages, `llms.txt`, and `llms-full.txt` are written to
`docs/_build/html`. Each page is available as both `page.html.md` and `page.md`;
the index links to the `page.html.md` version. Generated files are not committed.

## Contributing

Contributions are welcome!

Only the core and Django modules are currently in development. All others are in maintenance only mode, and maintainers are especially welcome there.

See the [CONTRIBUTING.md](https://github.com/python-social-auth/.github/blob/main/CONTRIBUTING.md) document for details.

## Versioning

This project follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## License

This project follows the BSD license. See the [LICENSE](LICENSE) for details.
