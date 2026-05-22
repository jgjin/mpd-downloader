resource "aws_security_group" "temporal_server" {
  name        = "temporal-server"
  description = "Security group for Temporal server"
  vpc_id      = var.vpc_id
}
