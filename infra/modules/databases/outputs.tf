output "db_address" {
  value = aws_db_instance.temporal.address
}

output "db_credentials_secret_arn" {
  value = aws_secretsmanager_secret.db_credentials.arn
}

output "temporal_database_sg_id" {
  value = aws_security_group.temporal_database.id
}
