from scripts.crud_operations import *
from config.get_s3_dynamodb import *
from scripts.csv_to_json import *
from scripts.upload_file import *
import json
import random

def generate_students_csv(output_file="students_200.csv", num_records=200):
    grades = ["A", "B", "C", "D"]
    fieldnames = [
        "student_id",
        "weekly_self_study_hours",
        "attendance_percentage",
        "class_participation",
        "total_score",
        "grade",
        "performance_category"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, num_records + 1):
            score = round(random.uniform(40, 100), 1)
            student = {
                "student_id": str(1000000 + i),
                "weekly_self_study_hours": str(round(random.uniform(1, 20), 1)),
                "attendance_percentage": str(round(random.uniform(60, 100), 1)),
                "class_participation": str(round(random.uniform(1, 10), 1)),
                "total_score": str(score),
                "grade": random.choice(grades),
                "performance_category": calculate_performance(score)
            }
            writer.writerow(student)

    print(f"{output_file} created with {num_records} records.")

def process_and_upload_file(local_file, bucket, s3_key):
    ext = os.path.splitext(local_file)[1].lower()
    
    # If CSV → convert to JSON
    if ext == ".csv":
        json_file = local_file.replace(".csv", ".json")
        convert_csv_to_json(local_file, json_file)
        file_to_upload = json_file
    elif ext == ".json":
        file_to_upload = local_file
    else:
        raise ValueError("Unsupported file type. Only CSV or JSON allowed.")
    
    # Upload to S3 (triggers Lambda)
    upload_file_to_s3(file_to_upload, bucket, s3_key)

# Example usage
if __name__ == "__main__":
    # Step 1: Generate the CSV file
    local_csv_file = "students_200.csv"
    generate_students_csv(output_file=local_csv_file, num_records=200)

    # Step 2: Upload the file to S3 (will convert CSV → JSON if needed)
    s3_key = "uploads/students_200.json"
    process_and_upload_file(local_csv_file, S3_BUCKET_NAME, s3_key)