import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import LETTER
from openai import OpenAI
from datetime import datetime

# OpenAI API 키 설정
client = OpenAI(api_key = '')

# 프롬프트 생성 함수
def create_prompt(question, answer):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "너는 훌륭한 조수야. 다른 말은 하지말고 아래의 답변 형식에 맞게 답변만 작성해줘"},
      {"role": "user", "content": f"회사 서류 자기소개서를 작성 중이야. '{question}'라는 항목의 질문에 대해 '{answer}'이라는 답을 적어봤는데 '{answer}'만 내용과 맞춤법을 다듬어서 똑같은 형식으로 다른 말하지 않고 출력해줘."}
    ]
  )
  return response.choices[0].message.content

# 질문과 답변을 저장할 리스트
qa_list = []

# 글자 수 제한
QUESTION_CHAR_LIMIT = 55
ANSWER_CHAR_LIMIT = 300

def check_char_limit(event, text_widget, limit):
  content = text_widget.get("1.0", "end-1c")
  if len(content) > limit:
    text_widget.delete(f"1.{limit}", "end")

def add_qa_fields():
  # 새로운 질문과 답변 입력란을 담을 프레임 생성
  frame = tk.Frame(input_frame)
  frame.pack(pady=10)
  qa_frames.append(frame)  # 프레임 리스트에 추가
  
  # 새로운 질문과 답변 입력란 생성
  tk.Label(frame, text=f"질문{len(questions_vars)+1} (최대 55자)").pack(pady=(10,0))
  q_text = tk.Text(frame, height=2, width=40)
  q_text.pack()
  q_text.bind("<KeyRelease>", lambda event: check_char_limit(event, q_text, QUESTION_CHAR_LIMIT))
  questions_vars.append(q_text)
  
  tk.Label(frame, text=f"답변{len(answers_vars)+1} (최대 300자)").pack(pady=(10,0))
  a_text = tk.Text(frame, height=5, width=40)
  a_text.pack()
  a_text.bind("<KeyRelease>", lambda event: check_char_limit(event, a_text, ANSWER_CHAR_LIMIT))
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
    # info[f"a{i}"] = create_prompt(question, answer) # gpt 학습
    info[f"a{i}"] = answer

  interval = 57   # 줄바꿈 추가 간격
  for key, value in info.items():
    info[key] = add_newlines(value, interval)

  # print(info)
  save_to_pdf(info)

  messagebox.showinfo("저장 성공", "자기소개서가 성공적으로 저장되었습니다.")

# info 줄바꿈 구현
def add_newlines(s, interval):
  """주어진 문자열에 특정 간격마다 줄바꿈을 추가합니다."""
  return '\n'.join(s[i:i+interval] for i in range(0, len(s), interval))

def save_to_pdf(info):
  pdfmetrics.registerFont(TTFont("MalgunGothic", "malgun.ttf"))
  pdfmetrics.registerFont(TTFont("MalgunGothic-Bold", "malgunbd.ttf"))

  name = info["name"]
  title = name+"의 자기소개서"
  c = canvas.Canvas(f"{name}_자기소개서.pdf", pagesize=LETTER)

  title_width = c.stringWidth(title, "MalgunGothic", 16)
  width, height = LETTER

  c.setFont("MalgunGothic", 16)
  c.drawString((width//2) - (title_width//2), 750, title)
  c.setLineWidth(0.3)
  c.line(30, 730, 580, 730)
  c.line(30, 733, 580, 733)
  c.setFont("MalgunGothic", 11)

  y = 700
  for i in range(1, (len(info) - 1) // 2 + 1):
    q = info[f"q{i}"]
    a = info[f"a{i}"]
    # 질문 출력
    lines = q.split('\n')
    c.setFont("MalgunGothic-Bold", 12)
    c.drawString(40, y, f"질문")
    y -= 20
    for line in lines:
      c.setFont("MalgunGothic", 11)
      c.drawString(40, y, f"{line}")
      y -= 20

    # 답변 출력
    lines = a.split('\n')
    c.setFont("MalgunGothic-Bold", 12)
    c.drawString(40, y, f"답변")
    y -= 20
    for line in lines:
      c.setFont("MalgunGothic", 11)
      c.drawString(40, y, f"{line}")
      y -= 20

    # 각 질문과 답변 사이에 추가 공간 추가
    if i != (len(info) - 1) // 2 :
      c.setLineWidth(0.3)
      c.line(40, y+11, 570, y+11)
      y -= 10

  today = datetime.today()
  c.drawString(340, y-30, f"위 기재 사항은 사실과 틀림없음을 확인합니다.")
  c.drawString(340, y-55, f"{today.year}년   {today.month}월   {today.day}일    지원자 :  {name}   (서명)")

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
