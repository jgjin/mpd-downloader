resource "aws_ecr_repository" "mpd_downloader_worker" {
  name                 = "mpd-downloader-worker"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_lifecycle_policy" "mpd_downloader_worker" {
  repository = aws_ecr_repository.mpd_downloader_worker.name

  policy = jsonencode({
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
        description  = "Keeps only the last 3 images"
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
