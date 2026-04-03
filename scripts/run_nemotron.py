import requests
import os
from datetime import datetime

NEMOTRON_ENDPOINT = "http://10.240.250.37:11434/api/generate"


def read_file(path):
    with open(path, "r") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)


def log(task_path, message):
    log_path = os.path.join(task_path, "run.log")
    with open(log_path, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")


def run_nemotron(task_path):
    try:
        files = os.listdir(task_path)
        prompts = sorted([f for f in files if "prompt_nemotron" in f])

        if not prompts:
            log(task_path, "❌ prompt 없음")
            return

        prompt_file = prompts[-1]
        prompt = read_file(os.path.join(task_path, prompt_file))

        payload = {
            "prompt": prompt,
            "max_tokens": 2000,
            "temperature": 0.2
        }

        log(task_path, f"🚀 Nemotron 호출: {prompt_file}")

        response = requests.post(NEMOTRON_ENDPOINT, json=payload, timeout=60)

        if response.status_code != 200:
            log(task_path, f"❌ API 오류: {response.status_code}")
            return

        result = response.json().get("output", "")

        if not result:
            log(task_path, "❌ 결과 없음")
            return

        output_path = os.path.join(task_path, "04_result.py")
        write_file(output_path, result)

        log(task_path, "✅ 코드 생성 성공")

    except Exception as e:
        log(task_path, f"❌ Exception: {str(e)}")


if __name__ == "__main__":
    task_path = input("Task 경로 입력 (예: tasks/T001): ")
    run_nemotron(task_path)