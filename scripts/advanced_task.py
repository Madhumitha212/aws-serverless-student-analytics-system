from concurrent.futures import ThreadPoolExecutor
from config.get_s3_dynamodb import *

# Connect to DynamoDB
dynamodb = get_dynamodb_resource()
table = dynamodb.Table('student_performance')

# --- Task 1: Update at_risk in parallel ---
def process_segment(segment, total_segments):
    last_key = None
    updated = 0

    while True:
        scan_args = {"Segment": segment, "TotalSegments": total_segments, "Limit": 1000}
        if last_key:
            scan_args["ExclusiveStartKey"] = last_key

        response = table.scan(**scan_args)
        items = response.get("Items", [])
        if not items:
            break

        # Batch write updates
        with table.batch_writer() as batch:
            for student in items:
                attendance = student.get("attendance_percentage", 0)
                score = student.get("total_score", 0)

                # Risk detection rule
                student["at_risk"] = (attendance < 60 or score < 50)

                batch.put_item(Item=student)
                updated += 1

        last_key = response.get("LastEvaluatedKey")
        if not last_key:
            break

    return updated

def update_at_risk_parallel(total_segments=10):
    with ThreadPoolExecutor(max_workers=total_segments) as executor:
        results = list(executor.map(lambda seg: process_segment(seg, total_segments), range(total_segments)))
    print("Updated at_risk for", sum(results), "students.")

# --- Task 2: Top 10 performers---
def top_10():
    response = table.query(
        IndexName = "grade-score-index",
        KeyConditionExpression="grade = :g",
        ExpressionAttributeValues={":g": "A"},
        ScanIndexForward=False,  # highest scores first
        Limit=10
    )
    print("\nTop 10 performers:")
    for i, s in enumerate(response["Items"], 1):
        print(f"{i}. {s['student_id']} | Score: {s['total_score']} | "
              f"Attendance: {s.get('attendance_percentage', 'N/A')} | At Risk: {s.get('at_risk', False)}")

# --- Run both tasks ---
if __name__ == "__main__":
    update_at_risk_parallel(total_segments=10)
    top_10()
