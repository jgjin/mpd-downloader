# TODO: use "aws_default_vpc"?
data "aws_vpc" "default" {
  default = true
}

# TODO: use "aws_default_subnet"?
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}
