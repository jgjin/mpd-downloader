# TODO: move into worker_pools module?
resource "aws_iam_role_policy" "worker_s3_access" {
  name   = "worker-s3-access"
  role   = var.worker_task_role_name
  policy = data.aws_iam_policy_document.worker_s3_access.json
}
