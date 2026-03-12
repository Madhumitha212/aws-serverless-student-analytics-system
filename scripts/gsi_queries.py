from config.get_s3_dynamodb import *
from boto3.dynamodb.conditions import Key

dynamodb = get_dynamodb_resource()
table = dynamodb.Table("student_performance")

def get_top_students():
    response = table.query(
        IndexName = "grade-score-index",
        KeyConditionExpression = Key("grade").eq("A"),
        ProjectionExpression = "student_id, total_score, grade",
        ScanIndexForward = False,
        Limit = 10
    )

    items = response["Items"]

    for item in items:
        print(item)

def student_highest_score():
    response = table.query(
        IndexName = "grade-score-index",
        KeyConditionExpression = Key("grade").eq("A"),
        ScanIndexForward = False
    )

    highest_score = response["Items"][0]["total_score"]

    while True:
        for item in response["Items"]:
            if item["total_score"] == highest_score:
                print(item)
            else:
                return

        if "LastEvaluatedKey" not in response:
            break

        response = table.query(
            IndexName="grade-score-index",
            KeyConditionExpression=Key("grade").eq("A"),
            ScanIndexForward=False,
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )


if __name__ == "__main__":
    get_top_students()
    student_highest_score()
