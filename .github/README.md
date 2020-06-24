# Autoformatting of files

The CSV and CIF files are validated using pre-commit hooks.


## Install pre-commit hooks locally

```
cd .workflows
pip install -r requirements.txt
pre-commit install
```

## Run pre-commit hooks locally

Once installed, the pre-commit hooks will run at every commit automatically.

In order to run them on the entire database, use
```
pre-commit run --all-files
```
