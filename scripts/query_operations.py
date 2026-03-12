from config.get_s3_dynamodb import *
from boto3.dynamodb.conditions import Attr

# Connect to DynamoDB
dynamodb = get_dynamodb_resource()
table = dynamodb.Table('student_performance')

# Query 1: Students with attendance_percentage > 90
def query_high_attendance():
    response = table.scan(
        FilterExpression=Attr('attendance_percentage').gt(90)
    )

    print("\nStudents with attendance > 90%:")
    for item in response['Items']:
        print(item)


# Query 2: Students with weekly_self_study_hours > 10
def query_high_study_hours():
    response = table.scan(
        FilterExpression=Attr('weekly_self_study_hours').gt(10)
    )

    print("\nStudents with weekly study hours > 10:")
    for item in response['Items']:
        print(item)


# Query 3: Students with Excellent performance
def query_excellent_students():
    response = table.scan(
        FilterExpression=Attr('performance_category').eq("Excellent")
    )

    print("\nStudents with Excellent performance:")
    for item in response['Items']:
        print(item)

if __name__ == "__main__":
    query_high_attendance()
    # query_high_study_hours()
    # query_excellent_students()