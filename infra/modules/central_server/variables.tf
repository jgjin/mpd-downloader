variable "vpc_id" {
  type = string
}

variable "docker_hub_pull_through_cache_url" {
  type = string
}

variable "db_address" {
  type = string
}

variable "db_credentials_secret_arn" {
  type = string
}

variable "cluster_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}
