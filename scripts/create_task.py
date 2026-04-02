import os
import shutil
from datetime import datetime

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
TASKS_PATH = os.path.join(BASE_PATH, "tasks")
TEMPLATES_PATH = os.path.join(BASE_PATH, "templates")


def get_next_task_id():
    existing = os.listdir(TASKS_PATH)
    nums = [int(x[1:]) for x in existing if x.startswith("T") and x[1:].isdigit()]
    next_id = max(nums) + 1 if nums else 1
    return f"T{str(next_id).zfill(3)}"


def create_task(title):
    task_id = get_next_task_id()
    task_path = os.path.join(TASKS_PATH, task_id)

    os.makedirs(task_path, exist_ok=True)

    for file in os.listdir(TEMPLATES_PATH):
        src = os.path.join(TEMPLATES_PATH, file)

        if file == "meta.json":
            dst = os.path.join(task_path, file)
            with open(src, "r") as f:
                content = f.read()

            content = content.replace('"task_id": ""', f'"task_id": "{task_id}"')
            content = content.replace('"title": ""', f'"title": "{title}"')
            content = content.replace('"created_at": ""', f'"created_at": "{datetime.now()}"')

            with open(dst, "w") as f:
                f.write(content)
        else:
            dst = os.path.join(task_path, file)
            shutil.copy(src, dst)

    print(f"✅ Task 생성 완료: {task_id}")


if __name__ == "__main__":
    title = input("Task 제목 입력: ")
    create_task(title)
