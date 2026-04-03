import subprocess
import os

def validate(task_path):
    file_path = os.path.join(task_path, "04_result.py")

    if not os.path.exists(file_path):
        print("❌ 결과 코드 없음")
        return False

    try:
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True
        )

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        return result.returncode == 0

    except Exception as e:
        print("❌ 실행 실패:", e)
        return False


if __name__ == "__main__":
    task_path = input("Task 경로 입력 (예: tasks/T001): ")
    success = validate(task_path)

    if success:
        print("✅ VALIDATION SUCCESS")
    else:
        print("❌ VALIDATION FAILED")
