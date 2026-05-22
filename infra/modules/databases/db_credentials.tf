resource "random_pet" "db_username" {
  separator = "_"
}

resource "random_password" "db_password" {
  length  = 24
  special = false
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
