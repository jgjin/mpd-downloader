resource "aws_vpc_security_group_egress_rule" "server_to_database" {
  security_group_id            = var.temporal_server_sg_id
  referenced_security_group_id = var.temporal_database_sg_id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "server_https" {
  security_group_id = var.temporal_server_sg_id
  from_port         = 443
  to_port           = 443
  ip_protocol       = "tcp"
  cidr_ipv4         = "0.0.0.0/0"
}

resource "aws_vpc_security_group_ingress_rule" "server_from_worker" {
  security_group_id            = var.temporal_server_sg_id
  referenced_security_group_id = var.temporal_worker_sg_id
  from_port                    = 7233
  to_port                      = 7233
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "server_from_my_ip" {
  security_group_id = var.temporal_server_sg_id
  from_port         = 8080
  to_port           = 8080
  ip_protocol       = "tcp"
  cidr_ipv4         = "${var.my_ip}/32"
}
