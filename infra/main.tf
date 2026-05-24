terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.45.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.9.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}

module "network" {
  source = "./modules/network"
}

module "databases" {
  source = "./modules/databases"

  vpc_id = module.network.vpc_id
}

module "images" {
  source = "./modules/images"
}

module "clusters" {
  source = "./modules/clusters"
}

module "central_server" {
  count  = var.deploy_temporal_services ? 1 : 0
  source = "./modules/central_server"

  vpc_id = module.network.vpc_id

  docker_hub_pull_through_cache_url = module.images.docker_hub_pull_through_cache_url

  db_address                = module.databases.db_address
  db_credentials_secret_arn = module.databases.db_credentials_secret_arn

  cluster_id = module.clusters.temporal_cluster_id
  subnet_ids = module.network.subnet_ids
}

module "storage" {
  source = "./modules/storage"
}

module "worker_pools" {
  count  = var.deploy_temporal_services ? 1 : 0
  source = "./modules/worker_pools"

  vpc_id = module.network.vpc_id

  worker_image = "${module.images.worker_ecr_repository_url}:latest"

  clearkey_id    = var.clearkey_id
  clearkey_value = var.clearkey_value

  cluster_id = module.clusters.temporal_cluster_id
  subnet_ids = module.network.subnet_ids

  mpds_bucket_arn     = module.storage.mpds_bucket_arn
  segments_bucket_arn = module.storage.segments_bucket_arn
  videos_bucket_arn   = module.storage.videos_bucket_arn
}

module "traffic" {
  count  = var.deploy_temporal_services ? 1 : 0
  source = "./modules/traffic"

  temporal_database_sg_id = module.databases.temporal_database_sg_id
  temporal_server_sg_id   = var.deploy_temporal_services ? module.central_server[0].temporal_server_sg_id : null
  temporal_worker_sg_id   = var.deploy_temporal_services ? module.worker_pools[0].temporal_worker_sg_id : null

  my_ip = var.my_ip
}
