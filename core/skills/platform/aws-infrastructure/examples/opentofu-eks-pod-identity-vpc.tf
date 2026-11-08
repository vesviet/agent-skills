terraform {
  required_version = ">= 1.8.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.75"
    }
  }

  # Client-side State KMS Encryption Block (OpenTofu v1.13+)
  encryption {
    key_provider "aws_kms" "primary" {
      kms_key_id = "arn:aws:kms:us-east-1:123456789012:key/3a8f7c19-b2e0-4d88-e7b5-1f0923a10582"
      region     = "us-east-1"
      key_spec   = "AES_256"
    }
    method "aes_gcm" "state_encryption" {
      keys = key_provider.aws_kms.primary
    }
    state {
      method   = method.aes_gcm.state_encryption
      enforced = true
    }
    plan {
      method   = method.aes_gcm.state_encryption
      enforced = true
    }
  }
}

provider "aws" {
  region = "us-east-1"
  default_tags {
    tags = {
      Environment = "production"
      Team        = "platform-engineering"
      Service     = "eks-core"
      CostCenter  = "cc-9812"
    }
  }
}

# 1. Zero-Trust VPC Topology (Private Subnets with VPC Endpoints)
resource "aws_vpc" "main" {
  cidr_block           = "10.100.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "prod-eks-vpc"
  }
}

# 2. IAM Role for EKS Pod Identity
resource "aws_iam_role" "s3_access_role" {
  name = "order-processing-s3-access"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "pods.eks.amazonaws.com"
        }
        Action = [
          "sts:AssumeRole",
          "sts:TagSession"
        ]
      }
    ]
  })
}

# 3. Scoped Least-Privilege Policy
resource "aws_iam_policy" "s3_order_receipts" {
  name = "order-receipts-s3-bucket-access"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject"]
        Resource = "arn:aws:s3:::prod-order-receipts-2026/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_s3" {
  role       = aws_iam_role.s3_access_role.name
  policy_arn = aws_iam_policy.s3_order_receipts.arn
}

# 4. EKS Pod Identity Association
resource "aws_eks_pod_identity_association" "order_service" {
  cluster_name    = "prod-core-eks"
  namespace       = "production"
  service_account = "order-service-sa"
  role_arn        = aws_iam_role.s3_access_role.arn
}
