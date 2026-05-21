terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
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

module "roles" {
  source = "./modules/roles"
}

module "network" {
  source = "./modules/network"
  my_ip  = var.my_ip
}

module "images" {
  source = "./modules/images"
}

module "authentication" {
  source = "./modules/authentication"
}

# module "storage" {
#   source                = "./modules/storage"
#   worker_task_role_name = module.roles.worker_task_role_name
# }

# module "central_server" {
#   source = "./modules/central_server"

#   subnet_ids                = module.network.subnet_ids
#   security_group_id         = module.network.temporal_server_sg_id
#   db_security_group_id      = module.network.temporal_database_sg_id
#   db_username               = module.authentication.db_username
#   db_password               = module.authentication.db_password
#   db_credentials_secret_arn = module.authentication.db_credentials_secret_arn
#   service_discovery_arn     = module.network.frontend_service_discovery_arn
#   execution_role_arn        = module.roles.task_execution_role_arn
#   server_task_role_arn      = module.roles.server_task_role_arn
# }

# module "worker_pools" {
#   source = "./modules/worker_pools"

#   vpc_id                   = module.network.vpc_id
#   server_security_group_id = module.network.temporal_server_sg_id
#   cluster_id               = module.central_server.cluster_id
#   subnet_ids               = module.network.subnet_ids
#   security_group_id        = module.network.temporal_worker_sg_id
#   execution_role_arn       = module.roles.task_execution_role_arn
#   worker_task_role_arn     = module.roles.worker_task_role_arn
#   worker_image             = "${module.images.ecr_repository_url}:latest"
#   bucket_names             = module.storage.bucket_names
#   clearkey_id              = var.clearkey_id
#   clearkey_value           = var.clearkey_value
# }
