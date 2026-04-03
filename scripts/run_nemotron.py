import requests
import os
from datetime import datetime

NEMOTRON_ENDPOINT = "http://10.240.250.37:11434/api/generate"

def log(task_path, msg):
    log_path = os.path.join(task_path, "run.log")
    line = f"[{datetime.now()}] {msg}\n"
    print(line)

    with open(log_path, "a") as f:
        f.write(line)


def run_nemotron(task_path):
    log(task_path, "🚀 START run_nemotron")

    try:
        if not os.path.exists(task_path):
            print("❌ task_path 없음")
            return

        files = os.listdir(task_path)
        log(task_path, f"📂 파일 목록: {files}")

        prompts = sorted([f for f in files if "prompt_nemotron" in f])

        if not prompts:
            log(task_path, "❌ prompt_nemotron 없음")
            return

        prompt_file = prompts[-1]
        log(task_path, f"📄 선택된 prompt: {prompt_file}")

        prompt_path = os.path.join(task_path, prompt_file)

        with open(prompt_path, "r") as f:
            prompt = f.read()

        log(task_path, f"🧠 prompt 길이: {len(prompt)}")

        payload = {
            "prompt": prompt,
            "max_tokens": 2000,
            "temperature": 0.2
        }

        log(task_path, f"🌐 API 호출 시작: {NEMOTRON_ENDPOINT}")

        response = requests.post(
            NEMOTRON_ENDPOINT,
            json=payload,
            timeout=60
        )

        log(task_path, f"📡 status_code: {response.status_code}")

        if response.status_code != 200:
            log(task_path, f"❌ API 실패: {response.text}")
            return

        try:
            data = response.json()
            log(task_path, f"📦 응답 JSON keys: {list(data.keys())}")
        except Exception as e:
            log(task_path, f"❌ JSON 파싱 실패: {response.text}")
            return

        result = data.get("output")

        if not result:
            log(task_path, "❌ output 없음 (응답 구조 확인 필요)")
            log(task_path, f"RAW RESPONSE: {data}")
            return

        output_path = os.path.join(task_path, "04_result.py")

        with open(output_path, "w") as f:
            f.write(result)

        log(task_path, "✅ 코드 생성 완료")

    except Exception as e:
        log(task_path, f"❌ EXCEPTION: {str(e)}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("❌ task_path 필요")
    else:
        run_nemotron(sys.argv[1])