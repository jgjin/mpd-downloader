output "frontend_service_discovery_arn" {
  value = aws_service_discovery_service.frontend.arn
}

output "temporal_server_sg_id" {
  value = aws_security_group.temporal_server.id
}

output "temporal_worker_sg_id" {
  value = aws_security_group.temporal_worker.id
}

output "vpc_id" {
  value = data.aws_vpc.default.id
}

output "subnet_ids" {
  value = data.aws_subnets.default.ids
}
