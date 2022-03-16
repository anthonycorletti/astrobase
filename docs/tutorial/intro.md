### Requirements

If you're using python already you can install astrobase directly from pypi.

```sh
pip install astrobasecloud
```

Also, if you would prefer to not install with python, you can also build a docker container and run Astrobase that way too.

Simply clone the repository;

```sh
git clone https://github.com/astrobase/astrobase.git && cd astrobase
./scripts/docker-build.sh
# and check that everything's working as expected
./scripts/docker-run.sh astrobase
```

### How & where to run Astrobase

Astrobase can run locally as a python package or docker container.

Astrobase can also be deployed as a docker container into a Kubernetes cluster, or wherever you can run a docker container.

Also, Astrobase can be deployed into any service that can run a python runtime with a custom entrypoint (e.g. Google App Engine).

### So what about multiple cloud providers?

Glad you asked. [Continue reading](../quickstart) for setup instructions and examples for AWS, GCP, and Azure.

### More questions before you get started?

[Leave us a question!](https://github.com/astrobase/astrobase/issues/new?assignees=&labels=question&template=question.md&title=%5BQUESTION%5D)
