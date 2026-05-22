resource "aws_iam_role" "temporal_worker_execution_role" {
  name               = "ecs-task-execution-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume_role.json
}

resource "aws_iam_role_policy_attachment" "temporal_worker_execution_role_policy" {
  role       = aws_iam_role.temporal_worker_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "temporal_worker_execution_secrets" {
  name   = "ecs-execution-secrets"
  role   = aws_iam_role.temporal_worker_execution_role.id
  policy = data.aws_iam_policy_document.temporal_worker_execution_secrets.json
}

resource "aws_iam_role" "temporal_worker_task_role" {
  name               = "temporal-worker-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume_role.json
}

resource "aws_iam_role_policy" "worker_s3_access" {
  name   = "worker-s3-access"
  role   = aws_iam_role.temporal_worker_task_role.name
  policy = data.aws_iam_policy_document.worker_s3_access.json
}
