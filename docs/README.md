# Astrobase Docs

Hi there! Welcome to Astrobase's docs.

Astrobase assumes that you already have an account with one of our supported cloud vendors and have credentials configured on your local machine.

If you have not created a free account yet, here are links to free trials;
- Google Cloud; https://cloud.google.com/free
- AWS; https://aws.amazon.com/free
- Azure; https://azure.microsoft.com/en-us/free/

To get started using Astrobase right away, we suggest reading through the [astrobase cli README](https://github.com/astrobase/cli/blob/master/README.md) and/ or checking out our [showcase](https://github.com/astrobase/showcase).

If you'd like to start hacking on astrobase, check out the [contributing guide](../CONTRIBUTING.md).

For more details about Astrobase, and using astrobase, read on!

## Design and Architecture

Astrobase was created because infrastructure and deployment management of containerized systems is not easy - **we believe it should be**.

Developers and teams of developers should not have to spend time solving problems that occur from opionionated infrastructure-as-code tools that make changes they did not intend. Astrobase simply passes requests directly to cloud providers and allows you to manage all cloud resources from one control-plane.

Astrobase will not restrict developers to a special deployment toolset. Developers can use whatever tool they want to deploy their services – be it `kubectl`, `helm`, `nomad`, or something else! This is why we take a lightweight approach to resource deployment. Similarly to how you define clusters in the form of `.yaml` files, specify a parent resource `.yaml` file that references your configs, and deploy!

We're also fed up with how difficult it can be to pass a parameter to yaml files. So we made it simple.

Just define your parameter in `yaml` kindof like how you would an environemnt variable

```yaml
# resources.yaml
apiVersion: v0
resources:
    - name: simple-nginx
      provider: gke
      cluster_name: astrobase-$ENV-gke
      cluster_location: $LOCATION
      resource_location: ./kubernetes
```

And pass parameters when applying your resources like so:

```sh
$ astrobase apply -f resources.yaml -v "ENV=dev LOCATION=us-central1"
```


## Installation and Usage

To see how to install and use the astrobase api server, check out the [contributing guide](../CONTRIBUTING.md).
