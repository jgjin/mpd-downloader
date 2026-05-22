resource "aws_vpc_security_group_ingress_rule" "database_from_server" {
  security_group_id            = var.temporal_database_sg_id
  referenced_security_group_id = var.temporal_server_sg_id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
}
