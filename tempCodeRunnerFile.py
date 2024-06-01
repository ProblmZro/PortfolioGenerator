import tkinter as tk
from tkinter import simpledialog
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import LETTER

# 질문과 답변을 저장할 리스트
qa_list = []

def add_qa_fields():
    # 새로운 질문과 답변 입력란 생성
    q_var = tk.StringVar()
    a_var = tk.StringVar()
    questions_vars.append(q_var)
    answers_vars.append(a_var)
  
    tk.Label(input_frame, text=f"질문{len(questions_vars)}").pack()
    tk.Entry(input_frame, textvariable=q_var).pack()
    tk.Label(input_frame, text=f"답변{len(answers_vars)}").pack()
    tk.Entry(input_frame, textvariable=a_var).pack()

def save_info():
    info = {
        "name": name_var.get(),
    }
    # 질문과 답변을 딕셔너리에 추가
    for i in range(len(questions_vars)):
        info[f"q{i+1}"] = questions_vars[i].get()
        info[f"a{i+1}"] = answers_vars[i].get()
    print(info)
    save_to_pdf(info)

def save_to_pdf(info):
    pdfmetrics.registerFont(TTFont("MalgunGothic", "malgun.ttf"))
    name = info["name"]
    c = canvas.Canvas(f"{name}_자기소개서.pdf", pagesize=LETTER)
    width, height = LETTER
    c.setFont("MalgunGothic", 16)
    c.drawString(100, 800, f"{name}의 자기소개서")
    y = 780
    for i in range(1, (len(info) - 1) // 2 + 1):
        q = info[f"q{i}"]
        a = info[f"a{i}"]
        c.drawString(100, y, f"질문: {q}")
        y -= 20
        c.drawString(100, y, f"답변: {a}")
        y -= 30
    c.save()

# GUI 설정
root = tk.Tk()
root.title("자기소개서 제작기")

name_var = tk.StringVar()
questions_vars = []
answers_vars = []

# 이름 입력란
top_frame = tk.Frame(root)
top_frame.pack()
tk.Label(top_frame, text="이름").pack(side=tk.LEFT)
tk.Entry(top_frame, textvariable=name_var).pack(side=tk.LEFT)

# 질문과 답변 입력란을 담을 프레임
input_frame = tk.Frame(root)
input_frame.pack()

# 처음 3개의 질문과 답변 입력란
for _ in range(3):
    add_qa_fields()

# 질문 추가 버튼
add_qa_button = tk.Button(root, text="질문 추가", command=add_qa_fields)
add_qa_button.pack()

save_button = tk.Button(root, text="정보 저장", command=save_info)
save_button.pack()

root.mainloop()