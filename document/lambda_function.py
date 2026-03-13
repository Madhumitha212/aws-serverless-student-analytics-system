import boto3
import json
from decimal import Decimal

s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("student_performance")


def calculate_performance_category(total_score):
      if total_score >= 90:
          return "Excellent"
      elif 75 <= total_score <= 89:
          return "Good"
      elif 60 <= total_score <= 74:
          return "Average"
      else:
          return "Poor"


def lambda_handler(event, context):

    print("Lambda triggered")

    for record in event['Records']:

        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        print(f"Processing file: {key}")

        response = s3_client.get_object(Bucket=bucket, Key=key)

        content = response['Body'].read().decode('utf-8')
        student_records = json.loads(content)

        print("Before parsing: ")
        print("Total records in file:", len(student_records))


          # Batch insert to DynamoDB
        with table.batch_writer() as batch:
            for student in student_records:
                total_score = float(student["total_score"])
                student["performance_category"] = calculate_performance_category(total_score)

                for field in ["weekly_self_study_hours", "attendance_percentage", "class_participation", "total_score"]:
                    if field in student:
                        student[field] = Decimal(str(student[field]))

                if "student_id" in student:
                    student["student_id"] = int(student["student_id"])

                batch.put_item(Item=student)

    print("Lambda execution completed")

    return {
        'statusCode':200,
        'body': json.dumps('Data inserted into DynamoDB successfully!')
      }