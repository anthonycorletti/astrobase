<p align="center">
  <a href="https://astrobase.cloud"><img src="https://github.com/astrobase/brand/blob/main/logos/space-logo.png?raw=true" alt="Astrobase"></a>
</p>
<p align="center">
    <em>Astrobase; simple multi-cloud Kubernetes cluster management.</em>
</p>
<p align="center">
<a href="https://github.com/astrobase/astrobase/actions?query=workflow%3Atest" target="_blank">
    <img src="https://github.com/astrobase/astrobase/workflows/test/badge.svg" alt="Test">
</a>
<a href="https://github.com/astrobase/astrobase/actions?query=workflow%3Apublish" target="_blank">
    <img src="https://github.com/astrobase/astrobase/workflows/publish/badge.svg" alt="publish">
</a>
<a href="https://codecov.io/gh/astrobase/astrobase" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/astrobase/astrobase?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/astrobasecloud" target="_blank">
    <img src="https://img.shields.io/pypi/v/astrobasecloud?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

---

**Documentation**: <a href="https://docs.astrobase.cloud" target="_blank">https://docs.astrobase.cloud</a>

**Source Code**: <a href="https://github.com/astrobase/astrobase" target="_blank">https://github.com/astrobase/astrobase</a>

---

Astrobase is great for developers that create and manage Kubernetes clusters across one or many cloud providers as well as on bare metal kubernetes solutions.

The key features are:

* **API First**: Unlike most other infrastructure management tools, Astrobase is an API-First service; meaning you can write any code you like to create your Kubernetes clusters.
* **Kubernetes First**: Astrobase only supports Kubernetes so you and your team can focus on streamlining the same application deployment story across any provider envrionment you might need to run your applications on.
* **Easy to use**: It's easy to use! Cluster creation definitions are short and simple, and you don't have to spend hours learning a domain specific language or
* **Start simple**: Astrobase's simplest example takes about 5 minutes to complete.
* **Scale across clouds**: If you're using Astrobase, and shipping your software to customers that use different cloud providers, you can test your deployments seamlessly and take advantage of over **$300,000** in cloud provider credits.

## Requirements

Python 3.7+

Alternatively, you can run Astrobase as a docker container incase you arent using python.

## Installation

```sh
pip install astrobasecloud
```

## A Quick Example! 🚀

### The absolute minimum

Create a file `gke-cluster.yaml` with:

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

### Deploy

Start the astrobase server in one terminal session

```sh
astrobase server
```

In another session, setup your GCP project and deploy your cluster!

```sh
astrobase provider setup gcp \
--project-id $(gcloud config get-value project) \
--service-name "container.googleapis.com"
```

```sh
astrobase cluster gke create \
--project-id $(gcloud config get-value project) \
--file "gke-cluster.yaml"
```

Done!

## ☁️ Going Multi-Cloud ☁️

### Two clusters, different clouds

Let's see what it takes to deploy onto two environments using Astrobase. Let's use GCP and AWS for this example.

Create a file `gke-cluster.yaml` with:

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

Now create a file `eks-cluster.yaml` with:

```yaml
---
cluster:
  name: astrobase-quickstart
  provider: eks
  region: us-east-1
  nodegroups:
    - nodegroupName: default
      scalingConfig:
        desiredSize: 1
        minSize: 1
        maxSize: 3
```

### Deploy

Start the astrobase server in one terminal session

```sh
astrobase server
```

In another session, setup your GCP project and deploy your cluster!

```sh
astrobase provider setup gcp \
--project-id $(gcloud config get-value project) \
--service-name "container.googleapis.com"
```

```sh
astrobase cluster gke create \
--project-id $(gcloud config get-value project) \
--file "gke-cluster.yaml"
```

Then deploy your AWS EKS cluster!

```sh
astrobase cluster eks create \
--kubernetes-control-plane-arn=$(aws iam list-roles | jq -r '.Roles[] | select(.RoleName == "AstrobaseEKSRole") | .Arn') \
--cluster-subnet-id=$(aws ec2 describe-subnets --query 'Subnets[].SubnetId[]' | jq -r '.[0]') \
--cluster-subnet-id=$(aws ec2 describe-subnets --query 'Subnets[].SubnetId[]' | jq -r '.[1]') \
--cluster-security-group-id=$(aws ec2 describe-security-groups --query 'SecurityGroups[].GroupId' | jq -r '.[0]') \
--nodegroup-noderole-mapping="default=$(aws iam list-roles | jq -r '.Roles[] | select(.RoleName == "AstrobaseEKSNodegroupRole") | .Arn')" \
--file "eks-cluster.yaml"
```

Deploying your EKS cluster requires a little extra setup. Checkout the [AWS user guide section](./tutorial/aws/intro) for more details.


## Recap

In summary, Astrobase makes it incredibly simple to create multiple kubernetes environments in different cloud providers.

You don't have to learn a new language, can extend the api if you need, deploy Astrobase into your cloud architecture, or simply run it locally.

For a more complete example including more features and detail, see the <a href="https://docs.astrobase.cloud/tutorial/">Tutorial - User Guide</a>.

## License

This project is licensed under the [Apache 2.0 License](https://github.com/astrobase/astrobase/blob/main/LICENSE).
