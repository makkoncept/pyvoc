# PyVoc Documentation

This folder contains auto-generated API documentation for the PyVoc project.

The documentation is automatically generated daily using GitHub Actions and the pdoc3 tool.

## Viewing Documentation

The documentation is generated in HTML format and can be viewed by opening `index.html` in a web browser.

## Manual Generation

To manually generate documentation, run:

```bash
pip install pdoc3
pdoc --html --output-dir doc pyvoc --force
```

This will generate HTML documentation from the Python source code in the `pyvoc` package.
