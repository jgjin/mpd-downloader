resource "aws_db_instance" "temporal" {
  identifier = "temporal-db"

  engine         = "postgres"
  engine_version = "16.6"

  instance_class = "db.t4g.small"

  storage_type      = "gp3"
  allocated_storage = 20

  username = random_pet.db_username.id
  password = random_password.db_password.result

  vpc_security_group_ids = [aws_security_group.temporal_database.id]

  skip_final_snapshot = true
}
