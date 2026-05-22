resource "aws_security_group" "temporal_worker" {
  name        = "temporal-worker"
  description = "Security group for Temporal workers"
  vpc_id      = var.vpc_id
}
