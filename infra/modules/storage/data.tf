data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "worker_s3_access" {
  statement {
    actions = ["s3:ListBucket", "s3:GetObject", "s3:PutObject"]
    resources = [
      aws_s3_bucket.mpds.arn,
      "${aws_s3_bucket.mpds.arn}/*",
      aws_s3_bucket.segments.arn,
      "${aws_s3_bucket.segments.arn}/*",
      aws_s3_bucket.videos.arn,
      "${aws_s3_bucket.videos.arn}/*"
    ]
  }
}
