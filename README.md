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
