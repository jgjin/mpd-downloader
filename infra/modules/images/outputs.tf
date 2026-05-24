output "worker_ecr_repository_url" {
  value = aws_ecr_repository.mpd_downloader_worker.repository_url
}

output "docker_hub_pull_through_cache_url" {
  value = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.id}.amazonaws.com/${aws_ecr_pull_through_cache_rule.docker_hub_pull_through_cache.ecr_repository_prefix}"
}
