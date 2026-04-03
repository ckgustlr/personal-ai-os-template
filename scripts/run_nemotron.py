import requests
import os
from datetime import datetime

#modify

NEMOTRON_ENDPOINT = "http://your-nemotron-endpoint/api/generate"
MODEL = "nemotron-cascade-2"


def log(task_path, message):
    log_path = os.path.join(task_path, "run.log")
    with open(log_path, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")

def is_valid_python(code):
    try:
        compile(code, "<string>", "exec")
        return True
    except:
        return False


def run_nemotron(task_path):
    try:
        files = os.listdir(task_path)
        prompts = sorted([f for f in files if "prompt_nemotron" in f])

        if not prompts:
            log(task_path, "❌ 프롬프트 파일 없음")
            return

        prompt_file = prompts[-1]
        prompt_path = os.path.join(task_path, prompt_file)

        with open(prompt_path, "r") as f:
            prompt = f.read()

        payload = {
            "model": MODEL,
            "prompt": prompt,
            "max_tokens": 2000,
            "temperature": 0.2
        }

        log(task_path, f"🚀 Nemotron 호출 시작: {prompt_file}")

        response = requests.post(NEMOTRON_ENDPOINT, json=payload)

        if response.status_code != 200:
            log(task_path, f"❌ API 오류: {response.text}")
            return

        data = response.json()

        # 🔥 핵심: 결과 조합
        result_text = ""

        # 케이스 1: 일반 응답
        if "output" in data:
            raw_text = data["output"]
            result_text = extract_code(raw_text)

        elif "tokens" in data:
            raw_text = "".join(data["tokens"])
            result_text = extract_code(raw_text)

        elif isinstance(data, list):
            raw_text = ""
            for item in data:
                if "token" in item:
                    raw_text += item["token"]
            result_text = extract_code(raw_text)

        if not is_valid_python(result_text):
            log(task_path, "❌ Python 코드 아님")
            return

        if not result_text.strip():
            log(task_path, "❌ 생성된 코드가 비어 있음")
            return

        # 🔥 결과 파일 저장
        output_path = os.path.join(task_path, "04_result.py")
        with open(output_path, "w") as f:
            f.write(result_text)

        log(task_path, "✅ 코드 생성 완료")

        # 🔥 콘솔 출력 (가독성 좋게)
        print("\n================ 생성된 코드 ================\n")
        print(result_text[:1000])  # 너무 길면 자름
        print("\n==========================================\n")

    except Exception as e:
        log(task_path, f"❌ 예외 발생: {str(e)}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("❌ task_path 필요")
    else:
        run_nemotron(sys.argv[1])