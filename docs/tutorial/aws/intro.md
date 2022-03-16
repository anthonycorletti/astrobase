### Preliminary Setup for EKS Deployments

In order to deploy clusters on Amazon Elastic Kubernetes Engine (EKS), you'll need to do some preliminary setup.

#### IAM Roles, Security Groups, and Subnets

You'll need to have an account ready with billing enabled and some IAM permissions configured.

When using astrobase remotely, say in EKS itself, astrobase will use the permissions on the cloud resource and nothing more.
