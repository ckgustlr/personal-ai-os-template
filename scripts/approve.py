import os

def approve(task_path):
    open(os.path.join(task_path, "APPROVED.flag"), "w").close()
    print("✅ 승인 완료")

if __name__ == "__main__":
    task_path = input("Task 경로 입력: ")
    approve(task_path)
