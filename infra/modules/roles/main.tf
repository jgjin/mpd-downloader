data "aws_iam_policy_document" "ecs_tasks_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "ecs-task-execution-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume_role.json
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "temporal_server_task_role" {
  name               = "temporal-server-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume_role.json
}

resource "aws_iam_role" "temporal_worker_task_role" {
  name               = "temporal-worker-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume_role.json
}

output "task_execution_role_arn" {
  value = aws_iam_role.ecs_task_execution_role.arn
}

output "task_execution_role_name" {
  value = aws_iam_role.ecs_task_execution_role.name
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
