data "aws_iam_policy_document" "ecs_tasks_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "temporal_worker_execution_secrets" {
  statement {
    actions   = ["secretsmanager:GetSecretValue"]
    resources = [aws_secretsmanager_secret.clearkey.arn]
  }
}

data "aws_iam_policy_document" "worker_s3_access" {
  statement {
    actions = ["s3:ListBucket", "s3:GetObject", "s3:PutObject"]
    resources = [
      var.mpds_bucket_arn,
      "${var.mpds_bucket_arn}/*",
      var.segments_bucket_arn,
      "${var.segments_bucket_arn}/*",
      var.videos_bucket_arn,
      "${var.videos_bucket_arn}/*"
    ]
  }
}

data "aws_region" "current" {}
