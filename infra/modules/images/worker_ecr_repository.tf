resource "aws_ecr_repository" "mpd_downloader_worker" {
  name                 = "mpd-downloader-worker"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
