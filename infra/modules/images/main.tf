resource "aws_ecr_repository" "mpd_downloader" {
  name                 = "mpd-downloader"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_secretsmanager_secret" "docker_hub_credentials" {
  name        = "docker-hub-credentials"
  description = "Docker Hub credentials for ECR pull through cache"
}

resource "aws_ecr_pull_through_cache_rule" "docker_hub" {
  ecr_repository_prefix = "docker-hub"
  upstream_registry_url = "registry-1.docker.io"
  credential_arn        = aws_secretsmanager_secret.docker_hub_credentials.arn
}

output "ecr_repository_url" {
  value = aws_ecr_repository.mpd_downloader.repository_url
}
