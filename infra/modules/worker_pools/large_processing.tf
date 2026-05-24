resource "aws_ecs_task_definition" "large_processing" {
  family = "temporal-worker-large-processing"

  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"

  cpu    = 1024
  memory = 2048

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "ARM64"
  }

  execution_role_arn = aws_iam_role.temporal_worker_execution_role.arn
  task_role_arn      = aws_iam_role.temporal_worker_task_role.arn

  container_definitions = jsonencode([
    {
      name  = "worker"
      image = var.worker_image
      environment = [
        { name = "TEMPORAL_HOST", value = "dns:///frontend.temporal.internal:7233" },
        { name = "TASK_QUEUE", value = "large-processing-queue" },
        { name = "S3_BUCKET_SUFFIX", value = data.aws_caller_identity.current.account_id }
      ],
      secrets = [
        { name = "CLEARKEY_ID", valueFrom = "${aws_secretsmanager_secret.clearkey.arn}:clearkey_id::" },
        { name = "CLEARKEY_VALUE", valueFrom = "${aws_secretsmanager_secret.clearkey.arn}:clearkey_value::" }
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
  name = "worker-large-processing"

  cluster = var.cluster_id

  task_definition = aws_ecs_task_definition.large_processing.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = [aws_security_group.temporal_worker.id]
    assign_public_ip = true
  }
}
