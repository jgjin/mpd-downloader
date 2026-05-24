variable "deploy_temporal_services" {
  description = "Whether to deploy the Temporal services (central server, worker pools, and traffic configuration)"
  type        = bool
  default     = false
}

variable "docker_hub_username" {
  description = "Docker Hub username for pull through cache"
  type        = string
}

variable "docker_hub_access_token" {
  description = "Docker Hub personal access token for pull through cache"
  type        = string
  sensitive   = true
}

variable "clearkey_id" {
  description = "ClearKey ID for decryption"
  type        = string
  sensitive   = true
}

variable "clearkey_value" {
  description = "ClearKey value for decryption"
  type        = string
  sensitive   = true
}

variable "my_ip" {
  description = "My public IP address for restricted access to the Temporal web UI"
  type        = string
}
