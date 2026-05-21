resource "aws_security_group" "temporal_database" {
  name        = "temporal-database"
  description = "Security group for Temporal database"
  vpc_id      = data.aws_vpc.default.id
}

resource "aws_security_group" "temporal_server" {
  name        = "temporal-server"
  description = "Security group for Temporal server"
  vpc_id      = data.aws_vpc.default.id
}

resource "aws_security_group" "temporal_worker" {
  name        = "temporal-worker"
  description = "Security group for Temporal workers"
  vpc_id      = data.aws_vpc.default.id
}

resource "aws_vpc_security_group_ingress_rule" "database_from_server" {
  security_group_id            = aws_security_group.temporal_database.id
  referenced_security_group_id = aws_security_group.temporal_server.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "server_to_database" {
  security_group_id            = aws_security_group.temporal_server.id
  referenced_security_group_id = aws_security_group.temporal_database.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "server_https" {
  security_group_id = aws_security_group.temporal_server.id
  from_port         = 443
  to_port           = 443
  ip_protocol       = "tcp"
  cidr_ipv4         = "0.0.0.0/0"
}

resource "aws_vpc_security_group_ingress_rule" "server_from_worker" {
  security_group_id            = aws_security_group.temporal_server.id
  referenced_security_group_id = aws_security_group.temporal_worker.id
  from_port                    = 7233
  to_port                      = 7233
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "server_from_my_ip" {
  security_group_id = aws_security_group.temporal_server.id
  from_port         = 8080
  to_port           = 8080
  ip_protocol       = "tcp"
  cidr_ipv4         = "${var.my_ip}/32"
}

resource "aws_vpc_security_group_egress_rule" "worker_to_server" {
  security_group_id            = aws_security_group.temporal_worker.id
  referenced_security_group_id = aws_security_group.temporal_server.id
  from_port                    = 7233
  to_port                      = 7233
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "worker_https" {
  security_group_id = aws_security_group.temporal_worker.id
  from_port         = 443
  to_port           = 443
  ip_protocol       = "tcp"
  cidr_ipv4         = "0.0.0.0/0"
}

output "temporal_database_sg_id" {
  value = aws_security_group.temporal_database.id
}

output "temporal_server_sg_id" {
  value = aws_security_group.temporal_server.id
}

output "temporal_worker_sg_id" {
  value = aws_security_group.temporal_worker.id
}
