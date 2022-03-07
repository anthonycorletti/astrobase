### Preliminary Setup for AKS Deployments

In order to deploy clusters on Azure Kubernetes Engine (AKS), you'll need to do some preliminary setup.

#### Resource group and Active Directory Applicaton Credentials

You'll need to have a resource group ready and and active directory application with permissions to create AKS clusters.

When using astrobase remotely, say in AKS itself, astrobase will use the permissions on the resource and nothing more.
