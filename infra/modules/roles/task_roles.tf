# TODO: move into central_server module?
resource "aws_iam_role" "temporal_server_task_role" {
  name               = "temporal-server-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume_role.json
}

# TODO: move into worker_pools module?
resource "aws_iam_role" "temporal_worker_task_role" {
  name               = "temporal-worker-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume_role.json
}
