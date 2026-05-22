resource "aws_iam_role" "temporal_server_execution_role" {
  name               = "temporal-server-execution-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume_role.json
}

resource "aws_iam_role_policy_attachment" "temporal_server_execution_role_policy" {
  role       = aws_iam_role.temporal_server_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "temporal_server_execution_secrets" {
  name   = "temporal-server-execution-secrets"
  role   = aws_iam_role.temporal_server_execution_role.name
  policy = data.aws_iam_policy_document.temporal_server_execution_secrets.json
}

resource "aws_iam_role" "temporal_server_task_role" {
  name               = "temporal-server-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume_role.json
}
