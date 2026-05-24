resource "aws_secretsmanager_secret" "clearkey" {
  name                    = "temporal-worker-clearkey"
  description             = "ClearKey for Temporal workers to use for decryption"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "clearkey" {
  secret_id = aws_secretsmanager_secret.clearkey.id
  secret_string = jsonencode({
    clearkey_id    = var.clearkey_id
    clearkey_value = var.clearkey_value
  })
}
