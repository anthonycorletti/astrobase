### Preliminary Setup for EKS Deployments

In order to deploy clusters on Amazon Elastic Kubernetes Engine (EKS), you'll need to do some preliminary setup.

#### IAM Roles, Security Groups, and Subnets

You'll need to have a resource group ready and and active directory application with permissions to create AKS clusters.

When using astrobase remotely, say in AKS itself, astrobase will use the permissions on the resource and nothing more.
