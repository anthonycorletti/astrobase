# Contributing

First, here are a few simple ways to help.

#### Star [astrobase](https://github.com/astrobase/astrobase) on GitHub!
By adding a star, other users will be able to find Astrobase more easily and see that it has been already useful for others.

#### Watch [astrobase](https://github.com/astrobase/astrobase) for new releases!
You can "watch" Astrobase in GitHub (clicking the "watch" button at the top right). There you can select "Releases only". Then you will receive notifications whenever there's a new release (a new version) of Astrobase with bug fixes and new features.

#### Connect with Astrobase
Follow us on twitter [@astrobasecloud](https://twitter.com/astrobasecloud).

#### Open a pull request or issue.

[Issues](https://github.com/astrobase/astrobase/issues/new/choose) and [pull requests](https://github.com/astrobase/astrobase/pulls) are very welcome!


---

Now if you already cloned the repository and you know that you need to deep dive in the code, here are some guidelines to set up your environment.


## Use a virtual environment

```sh
$ python -m venv .venv
```

This will create a directory `./venv/` with python binaries and then you will be able to install packages for that isolated environment.

Next, activate the environment.

```sh
$ source ./venv/bin/activate
```

To check that it worked correctly;

```sh
$ which python pip
/path/to/astrobase/.venv/bin/python
/path/to/astrobase/.venv/bin/pip
```

Using [`pyenv`](https://github.com/pyenv/pyenv) is highly suggested for local python development.

## Flit

Astrobase uses `flit` to manage dependencies.

After activating the environment as described above, install flit:

```sh
$ pip install --upgrade flit
```

Install dependencies

```sh
./scripts/install.sh
```

## Formatting and Linting

```sh
./scripts/lint.sh
./scripts/format.sh
```

## Tests

```sh
./scripts/test-cov-html.sh
```

This command generates a directory `./htmlcov/`, if you open the file` ./htmlcov/index.html` in your browser, you can explore interactively the regions of code that are covered by the tests, and notice if there is any region missing.

## Local Uvicorn, Gunicorn, and Docker

```sh
./scripts/uvicorn-run.sh
```

```sh
./scripts/gunicorn-run.sh
```

```sh
./scripts/docker-build.sh
./scripts/docker-run.sh
```

