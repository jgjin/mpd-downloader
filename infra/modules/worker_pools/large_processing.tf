# TODO: review resource sizing here
resource "aws_ecs_task_definition" "large_processing" {
  family                   = "temporal-worker-large-processing"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 2048
  memory                   = 4096
  execution_role_arn       = aws_iam_role.temporal_worker_execution_role.arn
  task_role_arn            = aws_iam_role.temporal_worker_task_role.arn

  container_definitions = jsonencode([
    {
      name  = "worker"
      image = var.worker_image
      environment = [
        { name = "TEMPORAL_HOST", value = "dns:///frontend.temporal.internal:7233" },
        { name = "TASK_QUEUE", value = "large-processing-queue" }
      ],
      secrets = [
        { name = "CLEARKEY_ID", value_from = "${aws_secretsmanager_secret.clearkey.arn}:clearkey_id::" },
        { name = "CLEARKEY_VALUE", value_from = "${aws_secretsmanager_secret.clearkey.arn}:clearkey_value::" }
      ],
      log_configuration = {
        log_driver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/temporal-worker"
          "awslogs-region"        = data.aws_region.current.id
          "awslogs-stream-prefix" = "large-processing"
          "awslogs-create-group"  = "true"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "large_processing" {
  name            = "worker-large-processing"
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.large_processing.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = [aws_security_group.temporal_worker.id]
    assign_public_ip = true
  }
}
