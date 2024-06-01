import tkinter as tk
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import LETTER

# 질문과 답변을 저장할 리스트
qa_list = []

def add_qa_fields():
  # 새로운 질문과 답변 입력란을 담을 프레임 생성
  frame = tk.Frame(input_frame)
  frame.pack(pady=10)
  qa_frames.append(frame)  # 프레임 리스트에 추가
  
  # 새로운 질문과 답변 입력란 생성
  tk.Label(frame, text=f"질문{len(questions_vars)+1}").pack(pady=(10,0))
  q_text = tk.Text(frame, height=2, width=40)
  q_text.pack()
  questions_vars.append(q_text)
  
  tk.Label(frame, text=f"답변{len(answers_vars)+1}").pack(pady=(10,0))
  a_text = tk.Text(frame, height=5, width=40)
  a_text.pack()
  answers_vars.append(a_text)

def delete_qa_fields():
  if qa_frames:
    # 가장 마지막에 추가된 질문과 답변의 프레임 삭제
    frame_to_delete = qa_frames.pop()
    frame_to_delete.destroy()
    # 마지막 질문과 답변 삭제
    questions_vars.pop()
    answers_vars.pop()


def save_info():
  info = {
    "name": name_var.get(),
  }
  # 질문과 답변을 딕셔너리에 추가
  for i, (q_text, a_text) in enumerate(zip(questions_vars, answers_vars), 1):
    question = q_text.get("1.0", "end-1c")  # 텍스트 위젯에서 텍스트 가져오기
    answer = a_text.get("1.0", "end-1c")  # 텍스트 위젯에서 텍스트 가져오기
    info[f"q{i}"] = question
    info[f"a{i}"] = answer
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
qa_frames = []  # 질문과 답변 세트를 담을 프레임을 저장할 리스트

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

add_qa_button = tk.Button(root, text="질문 추가", command=add_qa_fields)
add_qa_button.pack()

delete_qa_button = tk.Button(root, text="질문 삭제", command=delete_qa_fields)
delete_qa_button.pack()

save_button = tk.Button(root, text="정보 저장", command=save_info)
save_button.pack()

root.mainloop()