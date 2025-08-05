# CONTRIBUTING

## Getting started

```bash
git clone https://gitlab.esrf.fr/XRD/darfix.git
cd darfix
pip install .[dev]
```

## Linting

The configuration for [black](https://black.readthedocs.io/en/stable/) and [flake8](https://flake8.pycqa.org/en/latest/index.html) can be modified in `setup.cfg`.

Both can be run from the command line once installed:

```bash
black .
```

```bash
flake8
```

## Testing

Tests can be run with `pytest`

```bash
pytest .
```

### Test files

Test files are hosted on [silx.org](http://www.silx.org/pub/darfix/) and are automatically fetched when tests are run.

The file `input.h5` contains 2 scans:

- `1.1`: Rebinned data from the [55mn dataset](https://xrd.gitlab-pages.esrf.fr/darfix/development/index.html#test-datasets) with 1 positionner `diffry`
- `2.1`: Rebinned data from the [55mn dataset](https://xrd.gitlab-pages.esrf.fr/darfix/development/index.html#test-datasets) with 2 positionners `diffry` and `diffrx`.

## Write documentation

The documentation is composed of RST files located in `doc`. You can look at the [Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html) for information on how to write RST files.

If a new file is created, don't forget to reference it in one of the `toctree` directive.

## Build documentation

The documentation is built with [Sphinx](https://www.sphinx-doc.org/en/master/) that generates HTML pages out of the RST files. The configuration of Sphinx is in `doc/conf.py`.

Requirements (including Sphinx) can be installed with

```bash
pip install .[doc]
```

Then, build the documentation with

```bash
sphinx-build doc build/sphinx/html -E -a
```

The generated HTML pages will be available in `build/sphinx/html`. You can browse them by opening `build/sphinx/html/index.html` in your browser.

## Make a new release

Check the following things:

- Your working tree is clean and up to date with the remote `main`
- The relevant changes of the new version are in the CHANGELOG.

If not, checkout the remote `main` and use [Compare](https://gitlab.esrf.fr/XRD/darfix/-/compare) to review the commits since last release and write the user-facing changes in the CHANGELOG.

Once this is done, the version number in `src/darfix/_version.py` needs to be incremented. Review the changes of the version contained in the CHANGELOG to decide which part of the version number `major.minor.patch` you need to increment:

- _major_: Breaking changes (e.g. widget removed, inputs/output changed)
- _minor_: New features that are not breaking (e.g. new widget, new input in an existing widget)
- _patch_: Bug fixes

The change of version number needs then to be committed to the remote `main` branch (e.g. via a MR), which will trigger a pipeline building the package. Once this pipeline is finished, you can release the built package by triggering the `release_pypi` job on the [Pipelines page](https://gitlab.esrf.fr/XRD/darfix/-/pipelines) (Play button).
