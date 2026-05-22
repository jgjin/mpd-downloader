resource "aws_security_group" "temporal_database" {
  name        = "temporal-database"
  description = "Security group for Temporal database"
  vpc_id      = var.vpc_id
}
