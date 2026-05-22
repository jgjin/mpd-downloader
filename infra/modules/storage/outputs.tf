output "mpds_bucket_arn" {
  value = aws_s3_bucket.mpds.arn
}

output "segments_bucket_arn" {
  value = aws_s3_bucket.segments.arn
}

output "videos_bucket_arn" {
  value = aws_s3_bucket.videos.arn
}
