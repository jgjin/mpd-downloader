variable "vpc_id" {
  type = string
}

variable "worker_image" {
  type = string
}

variable "clearkey_id" {
  type = string
}

variable "clearkey_value" {
  type = string
}

variable "cluster_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "mpds_bucket_arn" {
  type = string
}

variable "segments_bucket_arn" {
  type = string
}

variable "videos_bucket_arn" {
  type = string
}
