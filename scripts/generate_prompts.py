import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

def generate_prompts(task_path):
    define = read_file(os.path.join(task_path, "01_define.md"))
    design = read_file(os.path.join(task_path, "02_design.md"))

    system_prompt = """
You are a senior AI architect designing prompts for a multi-stage software pipeline.

Generate THREE outputs:

1) Nemotron Prompt (code generation)
2) ClineSR Review Prompt
3) Validation Prompt

Each must be production-grade, explicit, and structured.
"""

    user_prompt = f"""
[DEFINE]
{define}

[DESIGN]
{design}

Generate:

=== NEMOTRON PROMPT ===
- Step-by-step logic
- Input/output spec
- Edge cases
- Error handling
- Final instruction: generate Python code

=== REVIEW PROMPT (ClineSR) ===
- Role: senior reviewer
- Compare code vs design
- Find bugs, structure issues
- Suggest improvements
- Output format fixed

=== VALIDATION PROMPT ===
- How to test correctness
- Edge case verification
- Output SUCCESS / FAIL

Return clearly separated sections.
"""

    # ✅ 핵심 수정
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    # ✅ 안정적인 텍스트 추출
    output = response.output_text

    # 🔥 파싱
    sections = {
        "nemotron": "",
        "review": "",
        "validation": ""
    }

    current = None
    for line in output.splitlines():
        if "NEMOTRON" in line.upper():
            current = "nemotron"
            continue
        elif "REVIEW" in line.upper():
            current = "review"
            continue
        elif "VALIDATION" in line.upper():
            current = "validation"
            continue

        if current:
            sections[current] += line + "\n"

    # 🔥 파일 저장
    write_file(os.path.join(task_path, "03_prompt_nemotron.md"), sections["nemotron"])
    write_file(os.path.join(task_path, "05_review_prompt_clinesr.md"), sections["review"])
    write_file(os.path.join(task_path, "06_validation_prompt.md"), sections["validation"])

    print("✅ 3종 프롬프트 생성 완료")


if __name__ == "__main__":
    task_path = input("Task 경로 입력 (예: tasks/T001): ")
    generate_prompts(task_path)