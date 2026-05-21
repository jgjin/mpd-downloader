resource "random_pet" "db_username" {
  length = 1
}

resource "random_password" "db_password" {
  length  = 24
  special = true
}

resource "aws_secretsmanager_secret" "db_credentials" {
  name        = "temporal-db-credentials"
  description = "Temporal database credentials"
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id     = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = random_pet.db_username.id
    password = random_password.db_password.result
  })
}

output "db_credentials_secret_arn" {
  value = aws_secretsmanager_secret.db_credentials.arn
}

output "db_username" {
  value = random_pet.db_username.id
}

output "db_password" {
  value     = random_password.db_password.result
  sensitive = true
}
