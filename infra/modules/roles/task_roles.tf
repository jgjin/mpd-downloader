resource "aws_iam_role" "temporal_server_task_role" {
  name               = "temporal-server-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume_role.json
}

resource "aws_iam_role" "temporal_worker_task_role" {
  name               = "temporal-worker-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume_role.json
}

output "server_task_role_arn" {
  value = aws_iam_role.temporal_server_task_role.arn
}

output "worker_task_role_arn" {
  value = aws_iam_role.temporal_worker_task_role.arn
}

output "worker_task_role_name" {
  value = aws_iam_role.temporal_worker_task_role.name
}
