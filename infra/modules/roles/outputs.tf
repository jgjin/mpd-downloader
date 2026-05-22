output "task_execution_role_arn" {
  value = aws_iam_role.ecs_task_execution_role.arn
}

output "task_execution_role_name" {
  value = aws_iam_role.ecs_task_execution_role.name
}

output "worker_task_role_arn" {
  value = aws_iam_role.temporal_worker_task_role.arn
}

output "worker_task_role_name" {
  value = aws_iam_role.temporal_worker_task_role.name
}
