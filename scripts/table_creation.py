from config.get_s3_dynamodb import *

def create_student_performance_table():
    """
    Creates a DynamoDB table 'student_performance' with:
    - Primary key: student_id
    """
    dynamodb = get_dynamodb_client()
    table_name = "student_performance"

    try:
        response = dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {'AttributeName': 'student_id', 'AttributeType': 'N'},  # Partition key
            ],
            KeySchema=[
                {'AttributeName': 'student_id', 'KeyType': 'HASH'},  # Primary key
            ],
            BillingMode = "PAY_PER_REQUEST"
        )

        print(f"Creating table '{table_name}'...")
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName=table_name)
        print(f"Table '{table_name}' created successfully!")

    except dynamodb.exceptions.ResourceInUseException:
        print(f"Table '{table_name}' already exists.")
    except Exception as e:
        print("Error creating table:", e)


if __name__ == "__main__":
    create_student_performance_table()