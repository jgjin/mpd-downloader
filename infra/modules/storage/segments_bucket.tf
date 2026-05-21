resource "aws_s3_bucket" "segments" {
  bucket = "segments-${data.aws_caller_identity.current.account_id}"
}

resource "aws_s3_bucket_lifecycle_configuration" "segments" {
  bucket = aws_s3_bucket.segments.id

  rule {
    id     = "expire-after-7-days"
    status = "Enabled"

    expiration {
      days = 7
    }
  }
}
