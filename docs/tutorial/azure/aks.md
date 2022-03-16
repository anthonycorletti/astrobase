### Running Astrobase and deploying an AKS Cluster

_**Note:** In order for Astrobase to work properly, you should authenticate to all cloud providers you wish to use in the same runtime as the astrobase server. Astrobase does not store or manage any provider credentials. Astrobase Enterprise and Astrobase Cloud do support cross-cloud and cross-account authentication and authorization._

For this example we'll deploy a cluster to Azure Kubernetes Engine.

### Connect to Azure

#### Configure your Azure Resource Group

```sh
$ az group create --name astrobase --location eastus
```

#### Create an Azure Active Directory Application and Register the Application to manage resources

Follow these links (assuming you have an admin owner configured as yourself already)

1. [Register an application with Azure AD and create a service principal](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#app-registration-app-objects-and-service-principals)
1. [Assign a role to the application](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#assign-a-role-to-the-application)
1. [Get your tenant and app ID values](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#get-tenant-and-app-id-values-for-signing-in)
1. [Authentication: Create and get your Application Secret](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#option-2-create-a-new-application-secret)
1. [Configure your access policies](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#configure-access-policies-on-resources)

#### Export Azure Credentials in the shell session where you initialize astrobase

```sh
export AZURE_SUBSCRIPTION_ID=<AZURE_SUBSCRIPTION_ID>
export AZURE_CLIENT_ID=<AZURE_CLIENT_ID>
export AZURE_CLIENT_SECRET=<AZURE_CLIENT_SECRET>
export AZURE_TENANT_ID=<AZURE_TENANT_ID>
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

Make sure to run this where you've authenticated to Azure

```sh
astrobase server
```

Create the file `aks-cluster.yaml`

```yaml
---
cluster:
  name: astrobase-quickstart
  provider: azure
  location: eastus
  dns_prefix: ab-quickstart
  agent_pool_profiles:
    - name: default
      mode: System
      count: 1
      min_count: 1
      max_count: 3
```

### Deploy the cluster!

```sh
astrobase cluster aks create \
--resource-group-name astrobase \
--file aks-cluster.yaml
```

### Cleaning up!

```sh
astrobase cluster aks delete \
--resource-group-name astrobase \
--file aks-cluster.yaml
```
