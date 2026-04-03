import subprocess
import os
from datetime import datetime

def log(task_path, msg):
    log_path = os.path.join(task_path, "validate.log")
    line = f"[{datetime.now()}] {msg}\n"
    print(line)

    with open(log_path, "a") as f:
        f.write(line)


def validate(task_path):
    file_path = os.path.join(task_path, "04_result.py")

    log(task_path, "🚀 VALIDATE START")

    if not os.path.exists(file_path):
        log(task_path, "❌ 결과 코드 없음")
        return False

    try:
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True
        )

        log(task_path, f"STDOUT:\n{result.stdout}")
        log(task_path, f"STDERR:\n{result.stderr}")
        log(task_path, f"RETURN CODE: {result.returncode}")

        return result.returncode == 0

    except Exception as e:
        log(task_path, f"❌ 실행 실패: {str(e)}")
        return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("❌ task_path 필요")
    else:
        validate(sys.argv[1])