# TODO: review resource sizing here
resource "aws_db_instance" "temporal" {
  identifier             = "temporal-db"
  allocated_storage      = 20
  storage_type           = "gp3"
  engine                 = "postgres"
  engine_version         = "16.3"
  instance_class         = "db.t4g.small"
  username               = random_pet.db_username.id
  password               = random_password.db_password.result
  skip_final_snapshot    = true
  vpc_security_group_ids = [aws_security_group.temporal_database.id]
  publicly_accessible    = false
}
