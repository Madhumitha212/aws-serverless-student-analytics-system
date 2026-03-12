from config.get_s3_dynamodb import *

def add_grade_score_index():
    dynamodb = get_dynamodb_client()
    table_name = "student_performance"

    try:
        response = dynamodb.update_table(
            TableName=table_name,

            AttributeDefinitions=[
                {'AttributeName': 'grade', 'AttributeType': 'S'},
                {'AttributeName': 'total_score', 'AttributeType': 'N'}
            ],

            GlobalSecondaryIndexUpdates=[
                {
                    'Create': {
                        'IndexName': 'grade-score-index',

                        'KeySchema': [
                            {'AttributeName': 'grade', 'KeyType': 'HASH'},
                            {'AttributeName': 'total_score', 'KeyType': 'RANGE'}
                        ],

                        'Projection': {
                            'ProjectionType': 'ALL'
                        }
                    }
                }
            ]
        )

        print("Global Secondary Index creation started.")

    except Exception as e:
        print("Error creating GSI:", e)


if __name__ == "__main__":
    add_grade_score_index()