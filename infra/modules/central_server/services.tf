# TODO: review resource sizing here
resource "aws_ecs_task_definition" "temporal_server" {
  family                   = "temporal-server"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 512
  memory                   = 1024
  execution_role_arn       = aws_iam_role.temporal_server_execution_role.arn
  task_role_arn            = aws_iam_role.temporal_server_task_role.arn

  container_definitions = jsonencode([
    {
      name  = "temporal-server"
      image = "${var.docker_hub_pull_through_cache_url}/temporalio/auto-setup:1.29.6"
      environment = [
        { name = "DB", value = "postgres12" },
        { name = "DB_PORT", value = "5432" },
        { name = "POSTGRES_SEEDS", value = var.db_address },
      ],
      secrets = [
        { name = "POSTGRES_USER", value_from = "${var.db_credentials_secret_arn}:username::" },
        { name = "POSTGRES_PWD", value_from = "${var.db_credentials_secret_arn}:password::" }
      ],
      port_mappings = [
        { containerPort = 7233, hostPort = 7233, protocol = "tcp" }
      ],
      log_configuration = {
        log_driver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/temporal-server"
          "awslogs-region"        = data.aws_region.current.id
          "awslogs-stream-prefix" = "server"
          "awslogs-create-group"  = "true"
        }
      }
    },
    {
      name  = "temporal-ui"
      image = "${var.docker_hub_pull_through_cache_url}/temporalio/ui:2.50.0"
      environment = [
        { name = "TEMPORAL_ADDRESS", value = "localhost:7233" }
      ],
      port_mappings = [
        { containerPort = 8080, hostPort = 8080, protocol = "tcp" }
      ],
      log_configuration = {
        log_driver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/temporal-server"
          "awslogs-region"        = data.aws_region.current.id
          "awslogs-stream-prefix" = "ui"
          "awslogs-create-group"  = "true"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "temporal_server" {
  name            = "temporal-server"
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.temporal_server.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = [aws_security_group.temporal_server.id]
    assign_public_ip = true
  }

  service_registries {
    registry_arn = aws_service_discovery_service.frontend.arn
  }
}
