# S3 Bucket Auditor

The S3 Bucket Auditor identifies S3 buckets with public access in a specified region for a given AWS account. It also has the option to automatically block all public access to the bucket and objects. The program outputs a list of vulnerable or auto-reconfigured buckets.

## Usage

1. Set AWS environment variables locally:

	```
export $AWS_ACCESS_KEY_ID="<aws_secret_key_id>"
export $AWS_SECRET_ACCESS_KEY="<aws_secret_access_key>"
	```

2. Execute program:

	`python s3auditor.py [-region <region>] [--auto-secure]` 

	Specify region with the `--region` flag, or omit to include all S3 buckets with public access in the account.

	Include the `--auto-secure` flag to automatically block public access to vulnerable S3 buckets.

## Why use this program?

AWS's ["Security best practices for Amazon S3"](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html) user guide states that, "Unless you explicitly require anyone on the internet to be able to read or write to your S3 bucket, you should ensure that your S3 bucket is not public."

## How can an attacker exploit a public Amazon S3 bucket?

Public access to Amazon S3 buckets can lead to huge financial loss and reputation damage for the company. 

The most obvious damage is a data breach, but a cheeky attacker could add files to a public bucket and incur charges on our AWS account. A sneaky snake could delete or modify log files stored in S3 to cover their tracks after unauthorized access to our AWS account, or delete backup and research data which would cost tremendous engineering hours and dollars to remediate. Or worse, they could leak the episodes of "The Last of Us" out of order! People *hate* spoilers, think of the angry Twitter memes.

## How can we prevent this vulnerability from occuring?

Luckily, starting April 2023, [Amazon S3 will change default settings for all new S3 buckets to block public access and disable ACLS.](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-faq.html). Running this program regularly should reconfigure existing buckets to eliminate this vulnerability and detect improper configuration for new buckets. Please read the [AWS Security best practices documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html). Thanks team! :)