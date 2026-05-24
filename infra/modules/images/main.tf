resource "aws_ecr_repository" "mpd_downloader_worker" {
  name                 = "mpd-downloader-worker"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_secretsmanager_secret" "docker_hub_credentials" {
  name                    = "ecr-pullthroughcache/docker-hub-credentials"
  description             = "Docker Hub credentials for ECR pull through cache"
  recovery_window_in_days = 0
}

resource "aws_ecr_pull_through_cache_rule" "docker_hub" {
  ecr_repository_prefix = "docker-hub"
  upstream_registry_url = "registry-1.docker.io"
  credential_arn        = aws_secretsmanager_secret.docker_hub_credentials.arn
}
