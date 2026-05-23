# Motivation
This document describes the deployment of the Temporal workflow defined in this repo.

# Goals
1. Learn about deploying a medium-scale Temporal workflow for a single user (me)
2. Learn about using large language models (LLMs) to learn about a new topic
3. Download some videos

# Out of scope
- Learn about deploying a very large-scale Temporal workflow for multiple users
- Learn about Kubernetes internals

# Requirements
The deployment should consist of:
- A central Temporal server to coordinate work for workflow executions
- A pool of Temporal workers per task queue
- Storage for the input MPD files and output video files, as well as intermediate files

# Implementation
Let's use Terraform, an industry standard, to deploy on Amazon Web Services (AWS), an industry standard.

## Central Temporal server
### Data layer
Let's use PostgreSQL. For medium scale, we can use Amazon RDS for PostgreSQL.

### Compute layer
Let's use an Amazon ECS service launched on AWS Fargate. The Amazon ECS service's task definition will have 2 containers:
1. `temporalio/auto-setup` connects to the database, sets up the database, then runs the server - note auto-setup works well for servers with one node and doesn't work well for servers with multiple nodes
2. `temporalio/ui` connects to the server then provides the Temporal web UI

## Temporal worker pools
### Data layer
See "Storage".

### Compute layer
Let's use Amazon ECS services launched on AWS Fargate. I will build a single worker image parameterized by task queue and upload it to Amazon ECR. Then I will configure an Amazon ECS service per task queue using that worker image.

## Storage
### Buckets
Let's use Amazon S3. We'll use 3 buckets:
1. `mpds` for input MPD files
2. `segments` for intermediate files
3. `videos` for output video files

### Permissions
Temporal workers will need to read and write objects in those Amazon S3 buckets, depending on their task queue. Therefore, we'll need to allow the worker Amazon ECS service's task IAM role to read and write objects in certain buckets, depending on its task queue.

## Network
### Allowed traffic
We use security groups to allow only certain traffic to and from each layer.

The server data layer security group allows traffic from the server compute layer.

The server compute layer security group allows traffic to the server data layer and to the public internet via HTTPS, not via HTTP. It also allows traffic from the workers to the server and from my local machine to the Temporal web UI.

The worker compute layer security group allows traffic to the server compute layer and to the public internet via HTTPS, not via HTTP.

For simplicity, tasks in the compute layers will get their own public IP addresses to make HTTPS requests to the public internet.

### Service discovery
Let's use AWS Cloud Map. We'll create the `temporal.internal` namespace in the default virtual private cloud (VPC). Then we'll create the `frontend` service within `temporal.internal`. When we use that service's Amazon Resource Name (ARN) as the server's Amazon ECS service's service registry, then the server will register its IP address(es) under `frontend.temporal.internal`.

Now when workers in the same VPC query `dns:///frontend.temporal.internal`, it will resolve to the server's IP address(es).

## Authentication
The server compute layer will need to authenticate into the server PostgreSQL database. Let's use AWS Secrets Manager to keep the database username and password secret. Then in the server compute layer task definition we can use the secrets from AWS Secrets Manager. To resolve secrets in the task definition, we'll need to allow the task execution IAM role to get the values of those secrets.
