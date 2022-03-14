### Running Astrobase and deploying an EKS Cluster

_**Note:** In order for Astrobase to work properly, you should authenticate to all cloud providers you wish to use in the same runtime as the astrobase server. Astrobase does not store or manage any provider credentials. Astrobase Enterprise and Astrobase Cloud do support cross-cloud and cross-account authentication and authorization._

For this example we'll deploy a cluster to Amazon Elastic Kubernetes Engine.

There are a few values in there that we have to specify on the command line to pass into this cluster definition, namely ...

```sh
SUBNET_ID_0 # we need atleast 2 subnets to run EKS, but can add more
SUBNET_ID_1
SECURITY_GROUP # we need atleast 1 security group to run EKS, but can add more
CLUSTER_ROLE_ARN
NODE_ROLE_ARN
```

To deploy the cluster into your default VPC use the following. For your own VPCs you'll need to specify those yourself. Note that these variables can be named whatever you like and aren't tied to a schema.

```sh
export SUBNET_ID_0=$(aws ec2 describe-subnets --query 'Subnets[].SubnetId[]' | jq -r '.[0]')
export SUBNET_ID_1=$(aws ec2 describe-subnets --query 'Subnets[].SubnetId[]' | jq -r '.[1]')
export SECURITY_GROUP=$(aws ec2 describe-security-groups --query 'SecurityGroups[].GroupId' | jq -r '.[0]')
```

Now for the ARNs. You'll need an ARN for the cluster and another for each nodegroup you want to create.

#### CLUSTER_ROLE_ARN

1. Create an IAM role, call it whatever you like. For documentation's sake, we'll call it `AstrobaseEKSRole`.
1. Attach the AWS managed policy, titled `AmazonEKSClusterPolicy`.
1. Set it in your environment:

    `export CLUSTER_ROLE_ARN=arn:aws:iam::account_id:role/AstrobaseEKSRole`

#### NODE_ROLE_ARN

1. Create an IAM role, call it whatever you like. For documentation's sake, we'll call it `AstrobaseEKSNodegroupRole`.
1. Attach the following AWS managed policies, titled: `AmazonEKSWorkerNodePolicy`, `AmazonEC2ContainerRegistryReadOnly`, `AmazonEKS_CNI_Policy`
1. Set it in your environment:

    `export NODE_ROLE_ARN=arn:aws:iam::account_id:role/AstrobaseEKSNodegroupRole`

#### AWS Configure

Make sure you can complete the `aws configure` login flow.

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

Make sure to run this where you've authenticated to AWS

```sh
astrobase server
```

Create the file `eks-cluster.yaml`

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

### Deploy the cluster!

```sh
astrobase cluster eks create \
--kubernetes-control-plane-arn=$CLUSTER_ROLE_ARN \
--cluster-subnet-id=$SUBNET_ID_0 \
--cluster-subnet-id=$SUBNET_ID_1 \
--cluster-security-group-id=$SECURITY_GROUP \
--nodegroup-noderole-mapping="default=$NODE_ROLE_ARN" \
--file "eks-cluster.yaml"
```

### Cleaning up!

```sh
astrobase cluster eks delete \
--kubernetes-control-plane-arn=$CLUSTER_ROLE_ARN \
--cluster-subnet-id=$SUBNET_ID_0 \
--cluster-subnet-id=$SUBNET_ID_1 \
--cluster-security-group-id=$SECURITY_GROUP \
--nodegroup-noderole-mapping="default=$NODE_ROLE_ARN" \
--file "eks-cluster.yaml"
```
