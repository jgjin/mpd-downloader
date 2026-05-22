resource "aws_vpc_security_group_egress_rule" "worker_to_server" {
  security_group_id            = var.temporal_worker_sg_id
  referenced_security_group_id = var.temporal_server_sg_id
  from_port                    = 7233
  to_port                      = 7233
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "worker_https" {
  security_group_id = var.temporal_worker_sg_id
  from_port         = 443
  to_port           = 443
  ip_protocol       = "tcp"
  cidr_ipv4         = "0.0.0.0/0"
}
