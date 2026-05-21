resource "aws_s3_bucket" "mpds" {
  bucket = "mpds-${data.aws_caller_identity.current.account_id}"
}

resource "aws_s3_bucket_lifecycle_configuration" "mpds" {
  bucket = aws_s3_bucket.mpds.id

  rule {
    id     = "expire-after-7-days"
    status = "Enabled"

    expiration {
      days = 7
    }
  }
}
