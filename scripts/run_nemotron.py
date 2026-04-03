import requests
import os

NEMOTRON_ENDPOINT = "http://your-nemotron-endpoint/api/generate"

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

def run_nemotron(task_path, version=None):
    files = os.listdir(task_path)

    prompts = sorted([f for f in files if "prompt_nemotron" in f])

    if not prompts:
        print("❌ Nemotron prompt 없음")
        return

    prompt_file = prompts[-1] if version is None else f"prompt_nemotron_v{version}.md"

    prompt = read_file(os.path.join(task_path, prompt_file))

    payload = {
        "prompt": prompt,
        "max_tokens": 2000,
        "temperature": 0.2
    }

    response = requests.post(NEMOTRON_ENDPOINT, json=payload)

    if response.status_code != 200:
        print("❌ Nemotron 호출 실패")
        return

    result = response.json()["output"]

    output_path = os.path.join(task_path, "04_result.py")
    write_file(output_path, result)

    print("✅ 코드 생성 완료 (Nemotron)")
