import json
from config.get_s3_dynamodb import *
from scripts.upload_file import *
from config.get_s3_dynamodb import *
from decimal import Decimal 

# Initialize DynamoDB client
dynamodb = get_dynamodb_resource()
table = dynamodb.Table('student_performance')

def export_table(file_name):
    response = table.scan()
    data = response['Items']

    # Handle pagination if table is large
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    # Write to JSON file
    with open(file_name , 'w') as f:
        json.dump(data, f, indent=4, default=lambda x: float(x) if isinstance(x, Decimal) else x)

    print("Export completed!")
    return file_name

if __name__ == "__main__":
    json_file = export_table("student_performance_export.json")
    upload_file_to_s3(json_file, S3_BUCKET_NAME, f"exports/{json_file}")