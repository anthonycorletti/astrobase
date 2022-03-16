### Preliminary Setup for GCP Deployments

In order to deploy clusters on GCP (GKE), you'll need to do some preliminary setup.

#### Project ID and Google Application Credentials

You'll need to have a Google Cloud project created already with a billing account attached.

Make sure you can complete the `gcloud auth login` flow from the shell session from which you're running `astrobase server` to create and manage clusters.

When using astrobase remotely, say in Google Cloud Run or GKE itself, astrobase will use the permissions on the cloud resource and nothing more.
