variable "docker_hub_username" {
  description = "Docker Hub username for pull through cache"
  type        = string
}

variable "docker_hub_access_token" {
  description = "Docker Hub personal access token for pull through cache"
  type        = string
  sensitive   = true
}
