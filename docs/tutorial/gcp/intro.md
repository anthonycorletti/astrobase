### Preliminary Setup for GCP Deployments

In order to deploy clusters on GCP (GKE), you'll need to do some preliminary setup.

#### Project ID and Google Application Credentials

You'll need to have a Google Cloud project created already with the GKE (Google Kubernetes Engine) and GCE (Google Compute Engine) APIs enabled. You can use `astrobase provider setup gcp --help` to automatically setup your project for you. Continue on in the tutorial to learn how to do this.

Make sure you can complete the `gcloud auth login` flow from the shell session from which you're running `astrobase server` to create and manage clusters.

When using astrobase remotely, say in Google Cloud Run or GKE itself, astrobase will use the permissions on the cloud resource and nothing more.
