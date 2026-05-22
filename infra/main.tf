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

# TODO: move roles into their specific modules
module "roles" {
  source                    = "./modules/roles"
  db_credentials_secret_arn = module.databases.db_credentials_secret_arn
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
  source = "./modules/central_server"

  vpc_id                            = module.network.vpc_id
  docker_hub_pull_through_cache_url = module.images.docker_hub_pull_through_cache_url
  db_address                        = module.databases.db_address
  db_credentials_secret_arn         = module.databases.db_credentials_secret_arn
  cluster_id                        = module.clusters.temporal_cluster_id
  subnet_ids                        = module.network.subnet_ids
  service_discovery_arn             = module.network.frontend_service_discovery_arn
}

module "storage" {
  source                = "./modules/storage"
  worker_task_role_name = module.roles.worker_task_role_name
}

# module "worker_pools" {
#   source = "./modules/worker_pools"

#   vpc_id                   = module.network.vpc_id
#   server_security_group_id = module.central_server.temporal_server_sg_id
#   cluster_id               = module.clusters.temporal_cluster_id
#   subnet_ids               = module.network.subnet_ids
#   security_group_id        = module.network.temporal_worker_sg_id
#   execution_role_arn       = module.roles.task_execution_role_arn
#   worker_task_role_arn     = module.roles.worker_task_role_arn
#   worker_image             = "${module.images.ecr_repository_url}:latest"
#   clearkey_id              = var.clearkey_id
#   clearkey_value           = var.clearkey_value
# }

module "traffic" {
  source = "./modules/traffic"

  temporal_database_sg_id = module.databases.temporal_database_sg_id
  temporal_server_sg_id   = module.central_server.temporal_server_sg_id
  temporal_worker_sg_id   = module.network.temporal_worker_sg_id
  my_ip                   = var.my_ip
}
