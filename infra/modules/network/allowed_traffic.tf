# TODO: move into central_server module?
resource "aws_security_group" "temporal_server" {
  name        = "temporal-server"
  description = "Security group for Temporal server"
  vpc_id      = data.aws_vpc.default.id
}

# TODO: move into worker_pools module?
resource "aws_security_group" "temporal_worker" {
  name        = "temporal-worker"
  description = "Security group for Temporal workers"
  vpc_id      = data.aws_vpc.default.id
}
