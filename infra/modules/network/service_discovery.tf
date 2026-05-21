resource "aws_service_discovery_private_dns_namespace" "temporal" {
  name        = "temporal.internal"
  description = "Private DNS for Temporal"
  vpc         = data.aws_vpc.default.id
}

resource "aws_service_discovery_service" "frontend" {
  name = "frontend"

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.temporal.id

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_config {
    failure_threshold = 1
  }
}

output "frontend_service_discovery_arn" {
  value = aws_service_discovery_service.frontend.arn
}
