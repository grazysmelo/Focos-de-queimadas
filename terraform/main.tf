terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.54.1"
    }
  }
}
# Criação do Data Lake (bucket) que irá conter as camadas bronze, silver e gold no s3

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "data_lake" {
  bucket        = var.bucket_name
  force_destroy = true

  tags = {
    Enviroment = var.enviroment
    Project    = "Pipeline-queimadas"
  }
}

# Bloquear acesso público
resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket = aws_s3_bucket.data_lake.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "folder_bronze" {
  bucket = aws_s3_bucket.data_lake.id
  key = "bronze/nasa_firms/"
}

resource "aws_s3_object" "folder_silver" {
  bucket = aws_s3_bucket.data_lake.id
  key = "silver/"
}

resource "aws_s3_object" "folder_gold" {
  bucket = aws_s3_bucket.data_lake.id
  key = "gold/"
}