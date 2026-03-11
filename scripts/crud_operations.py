from config.get_s3_dynamodb import *
from decimal import Decimal

def calculate_performance(total_score):
    if total_score >= 90:
        return "Excellent"
    elif 75 <= total_score <= 89:
        return "Good"
    elif 60 <= total_score <= 74:
        return "Average"
    else:
        return "Poor"

def insert_item(s_id, percentage, participation, grade, score, study_hours):
    table.put_item(
        Item = {
            "student_id" : s_id,
            "attendance_percentage" : Decimal(percentage),
            "class_participation" : Decimal(participation),
            "grade" : grade,
            "performance_category" : calculate_performance(Decimal(score)),
            "total_score" :  Decimal(score), 
            "weekly_self_study_hours" : Decimal(study_hours)
        }
    )
    print("Item inserted")

def read_item(s_id):
    response = table.get_item(
        Key = {
            "student_id" : s_id
        }
    )
    item = response.get("Item")
    print(item)
    print("Retrieved an item")

def update_item(s_id):
    table.update_item(
        Key = {
            "student_id" : s_id
        },
        UpdateExpression = "SET total_score = :s",
        ExpressionAttributeValues = {
            ":s" : "98"
        }
    )
    print("updated item")

def delete_record(s_id):
    table.delete_item(
        Key = {
            "student_id" : s_id
        }
    )
    print("Item deleted")


if __name__ == "__main__":
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table("student_performance")
    insert_item(1000001, "85.5", "5.5", "C", "70.2", "7.8")
    read_item(1)
    update_item(1)
    delete_record(1000001)
