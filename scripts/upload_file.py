from botocore.exceptions import NoCredentialsError, ClientError
from config.get_s3_dynamodb import *
from .csv_to_json import convert_csv_to_json

def upload_file_to_s3(local_file, bucket, s3_key):
    """Upload a file to S3."""
    s3 = get_s3_client()
    try:
        s3.upload_file(local_file, bucket, s3_key)
        print(f"Uploaded {local_file} to s3://{bucket}/{s3_key}")

    except FileNotFoundError:
        print("Local file not found.")

    except NoCredentialsError:
        print("AWS credentials not available.")

    except ClientError as e:
        print(f"Upload failed: {e}")

if __name__ == "__main__":
    # Input/output files
    csv_file = "dataset/student_performance.csv"
    json_file = "student_performance.json"
    s3_key = "student_performance.json"

    # Step 1: Convert CSV → JSON
    converted_file = convert_csv_to_json(csv_file, json_file)

    # Step 2: Upload JSON to S3
    upload_file_to_s3(converted_file, S3_BUCKET_NAME, s3_key)