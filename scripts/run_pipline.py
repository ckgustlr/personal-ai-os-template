import os
from datetime import datetime

TASKS_PATH = "tasks"

def log_global(msg):
    print(f"[{datetime.now()}] {msg}")

def run_pipeline():
    log_global("🚀 PIPELINE START")

    if not os.path.exists(TASKS_PATH):
        log_global("❌ tasks 폴더 없음")
        return

    tasks = os.listdir(TASKS_PATH)
    log_global(f"📂 발견된 tasks: {tasks}")

    for task in tasks:
        task_path = os.path.join(TASKS_PATH, task)

        if not os.path.isdir(task_path):
            continue

        log_global(f"➡️ 검사중: {task}")

        files = os.listdir(task_path)
        log_global(f"📁 파일 목록: {files}")

        if "APPROVED.flag" not in files:
            log_global(f"⏭️ SKIP (승인 없음): {task}")
            continue

        log_global(f"🔥 실행 시작: {task}")

        os.system(f"python scripts/run_nemotron.py {task_path}")
        os.system(f"python scripts/validate.py {task_path}")

    log_global("🏁 PIPELINE END")


if __name__ == "__main__":
    run_pipeline()
