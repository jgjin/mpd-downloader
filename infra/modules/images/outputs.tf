output "ecr_repository_url" {
  value = aws_ecr_repository.mpd_downloader.repository_url
}

output "docker_hub_pull_through_cache_url" {
  value = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com/${aws_ecr_pull_through_cache_rule.docker_hub.ecr_repository_prefix}"
}
