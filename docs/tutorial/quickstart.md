Let's get Astrobase set up and deploy a cluster on Google Cloud's Kubernetes Engine.

### Installation

Let's install Astrobase via PyPI

```sh
pip install astrobasecloud
```

Check that the installation worked

```sh
astrobase
```

Should print the help menu.

### Creating your profile

Astrobase profiles are configuration values that reference an astrobase server.

The values live in `~/.astrobase/config.json` by default. A `config.json` looks like;

```json
{
  "local": {
    "name": "local",
    "host": "localhost",
    "port": 8787,
    "secure": false
  }
}
```

You can view commands to interact with Astrobase profiles by running `astrobase profile --help`.

Let's walk through and example of setting up an Astrobase profile.

```sh
astrobase profile create local --no-secure
```

Now let's set it to be our current profile. We can do that by setting the `ASTROBASE_PROFILE` environment variable.

```
export ASTROBASE_PROFILE=local
astrobase profile current
{
  "name": "local",
  "host": "localhost",
  "port": 8787,
  "secure": false
}
```

Awesome. Now we're ready to initialize Astrobase and create our kubernetes cluster.

### Running Astrobase and deploying a cluster

_**Note:** In order for Astrobase to work properly, you should authenticate to all cloud providers you wish to use in the same runtime as the astrobase server. Astrobase does not store or manage any provider credentials. Astrobase Enterprise and Astrobase Cloud do support cross-cloud and cross-account authentication and authorization._

For this example we'll deploy a cluster to Google Cloud Kuberentes Engine (GKE).

First, in one terminal session, assuming you are doing this example locally, authenticate to GCP.

```sh
gcloud auth application-default login
```

Next create a project.

```sh
gcloud projects create super-cool-project
gcloud config set project super-cool-project
```

Start astrobase in the session you used to authenticate to GCP

```sh
astrobase server
```

Set up your project.

```sh
astrobase provider setup gcp --project-id $(gcloud config get-value project)
```

Create the file `gke-cluster.yaml`

```yaml
---
cluster:
  name: astrobase-quickstart
  provider: gcp
  location: us-central1-c
  node_pools:
    - name: default
      initial_node_count: 1
      autoscaling:
        enabled: true
        min_node_count: 1
        max_node_count: 3
```

Deploy the cluster!

```sh
astrobase cluster gke create \
--project-id $(gcloud config get-value project) \
--file "gke-cluster.yaml"
```

Cleaning up!

```sh
astrobase cluster gke delete \
--project-id $(gcloud config get-value project) \
--file "gke-cluster.yaml"
```

Delete the project in GCP

```sh
gcloud projects delete super-cool-project
```
