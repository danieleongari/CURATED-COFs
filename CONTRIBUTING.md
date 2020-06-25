# Contributing directly to the repository

You can contribute to the repository directly via pull requests.

## Autoformatting of files

The CSV and CIF files are validated using pre-commit hooks.


## Install pre-commit hooks locally

```
pip install -r .github/requirements.txt
pre-commit install
```

## Run pre-commit hooks locally

Once installed, the pre-commit hooks will run at every commit automatically.

In order to run them on the entire database, use
```
pre-commit run --all-files
```
