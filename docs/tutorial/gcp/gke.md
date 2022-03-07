### Running Astrobase and deploying a GKE Cluster

_**Note:** In order for Astrobase to work properly, you should authenticate to all cloud providers you wish to use in the same runtime as the astrobase server. Astrobase does not store or manage any provider credentials. Astrobase Enterprise and Astrobase Cloud do support cross-cloud and cross-account authentication and authorization._

For this example we'll deploy a cluster to Google Cloud Kuberentes Engine (GKE).

### Connect to GCP

First, in one terminal session, assuming you are doing this example locally, authenticate to GCP.

```sh
gcloud auth application-default login
```

Next create a project.

```sh
gcloud projects create super-cool-project
gcloud config set project super-cool-project
```

### Set your Astrobase profile and start your server

```sh
astrobase profile create local --no-secure
```

Set your profile and check that it was set properly.

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

### Start the astrobase server

Make sure to run this where you've authenticated to GCP

```sh
astrobase server
```

Set up your project.

```sh
astrobase provider setup gcp --project-id $(gcloud config get-value project) --service-name "container.googleapis.com"
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

### Deploy the cluster!

```sh
astrobase cluster gke create \
--project-id $(gcloud config get-value project) \
--file "gke-cluster.yaml"
```

### Cleaning up!

```sh
astrobase cluster gke delete \
--project-id $(gcloud config get-value project) \
--file "gke-cluster.yaml"
```

Delete the project in GCP

```sh
gcloud projects delete super-cool-project
```
