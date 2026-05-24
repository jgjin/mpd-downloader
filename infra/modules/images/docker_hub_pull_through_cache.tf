resource "aws_secretsmanager_secret" "docker_hub_credentials" {
  name                    = "ecr-pullthroughcache/docker-hub-credentials"
  description             = "Docker Hub credentials for pull through cache"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "docker_hub_credentials" {
  secret_id = aws_secretsmanager_secret.docker_hub_credentials.id
  secret_string = jsonencode({
    username    = var.docker_hub_username
    accessToken = var.docker_hub_access_token
  })
}

resource "aws_ecr_pull_through_cache_rule" "docker_hub_pull_through_cache" {
  ecr_repository_prefix = "docker-hub"
  upstream_registry_url = "registry-1.docker.io"
  credential_arn        = aws_secretsmanager_secret.docker_hub_credentials.arn
}

resource "aws_ecr_repository_creation_template" "docker_hub_pull_through_cache" {
  prefix      = "docker-hub"
  description = "Template for Docker Hub pull through cache repositories"
  applied_for = ["PULL_THROUGH_CACHE"]

  lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Expires all images older than 7 days"
        selection = {
          tagStatus   = "any"
          countType   = "sinceImagePushed"
          countNumber = 7
          countUnit   = "days"
        }
        action = {
          type = "expire"
        }
      },
      {
        rulePriority = 2
        description  = "Keeps only the last 3 images per repository"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 3
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}
