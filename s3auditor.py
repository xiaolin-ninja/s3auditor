import argparse
import boto3
import os


def parse_args():
    """
    Parse command line options
    """
    parser = argparse.ArgumentParser(
        description="Enumerate and automatically secure AWS S3 buckets with public access."
    )
    parser.add_argument('-r', '--region', type=str,
                        help="AWS region, default='*'")
    parser.add_argument('--auto-configure', default=False, action="store_true",
                        help="Automatically reconfigure S3 buckets, default=False")
    args = parser.parse_args()
    return args


def pprint(arr):
    for e in arr:
        print(e)
    print("\n")


def audit(args):
    """
    Outputs list of S3 buckets that allow public access.
    Automatically reconfigures buckets if `--auto-configure` flag set.
    """
    s3 = get_s3_client()

    print("Scanning S3 buckets for settings that allow public access...\n")
    buckets = get_public_buckets(s3, args.region)
    if not buckets:
        print("No vulnerable buckets detected! :)")
        return

    print(len(buckets), "vulnerable buckets:")
    pprint(buckets)

    if args.auto_configure:
        print("Automatically reconfiguring S3 buckets to block public access...")
        auto_configure_s3(s3, buckets)


def get_s3_client():
    """
    Gets and returns S3 client using AWS SDK boto3.
    """
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID') or input(
        "Enter AWS access key ID: ")
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY') or input(
        "Enter AWS secret access key: ")

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    return s3


def get_public_buckets(s3, region):
    """
    Returns a list of S3 buckets that do not block public access in a given region.
    """
    buckets = s3.list_buckets()['Buckets']
    vulnerable = []

    for b in buckets:
        name = b["Name"]

        try:
            location = get_bucket_location(s3, name)
            if region and region != location:
                continue

            setting = get_bucket_access_setting(s3, name)
            if False in setting.values():  # If any public access is allowed in policies
                vulnerable.append(
                    {
                        "name": name,
                        "region": location,
                    }
                )
        except:
            print("Unable to get bucket access setting for bucket {}".format(name))
            pass  # don't exit out the program if we have trouble with one bucket

    return vulnerable


def get_bucket_location(s3, bucket):
    """
    Returns the location of a given S3 bucket.
    """
    l = s3.get_bucket_location(Bucket=bucket)
    l.pop('ResponseMetadata')
    # If `='LocationConstraint' is None, it defaults to 'us-east-1'
    location = l['LocationConstraint'] or "us-east-1"
    return location


def get_bucket_access_setting(s3, bucket):
    """
    Returns the 'Block public access' settings of a given S3 bucket.
    """
    p = s3.get_public_access_block(Bucket=bucket)
    p.pop('ResponseMetadata')
    s = p['PublicAccessBlockConfiguration']
    return s


def auto_configure_s3(s3, buckets):
    """
    Programmatically configures a given S3 bucket to block all public access.
    """
    public_access_block_config = {
        "BlockPublicAcls": True,
        "IgnorePublicAcls": True,
        "BlockPublicPolicy": True,
        "RestrictPublicBuckets": True
    }

    total = len(buckets)
    success = 0

    for b in buckets:
        name = b["name"]
        s3.put_public_access_block(
            Bucket=name, PublicAccessBlockConfiguration=public_access_block_config)

        updated_config = s3.get_public_access_block(Bucket=name)['PublicAccessBlockConfiguration']
        if updated_config == public_access_block_config:
            print("[Success] {}, {}.".format(name, b["region"]))
            success += 1
        else:
            print("[FAILURE] {}, {}.".format(name, b["region"]))

    print("\n{} of {} vulnerable buckets reconfigured.".format(success, total))


if __name__ == '__main__':
    args = parse_args()
    try:
        audit(args)
    except Exception as e:
        print(e)
