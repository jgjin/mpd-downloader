variable "my_ip" {
  description = "My public IP address for restricted access to the Temporal web UI"
  type        = string
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
