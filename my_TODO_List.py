import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkcalendar import DateEntry

todo_index = None

#목록 관리 함수
def add_todo():
    todo = entry_todo.get()
    priority = priority_var.get()
    due_date = date_picker.get_date()

    if not todo:
        messagebox.showwarning("입력 오류", "할일을 입력해주세요.")
        return

    todo_text = f"[미완료] [{priority}] {due_date} {todo}"

    listbox_todo.insert(tk.END, todo_text)

    entry_todo.delete(0, tk.END)
    sort_todo()

def delete_todo():
    selected = listbox_todo.curselection()
    if selected:
        answer = messagebox.askyesno("할일 삭제", "이 할일을 삭제하시겠습니까?")

        if answer:
            listbox_todo.delete(selected[0])

    else:
        messagebox.showwarning("선택 오류", "삭제할 할일을 선택해주세요.")
        return
    sort_todo()

def start_edit(event=None):
    global todo_index

    selected = listbox_todo.curselection()
    todo_index = selected[0]
    selected_todo = listbox_todo.get(todo_index)

    todo_name = selected_todo.split(" ")[-1]
    todo_priority = selected_todo[7:9]

    entry_todo.delete(0, tk.END)
    entry_todo.insert(0, todo_name)
    priority_var.set(todo_priority)
    sort_todo()

def edit_todo():
    global todo_index
    selected = listbox_todo.curselection()
    todo = entry_todo.get()
    priority = priority_var.get()
    due_date = date_picker.get_date()

    if not todo:
        messagebox.showwarning("입력 오류", "할일을 입력해주세요.")
        return

    if not selected:
        messagebox.showwarning("선택 오류", "수정할 할일을 선택해주세요.")

    todo_text = f"[미완료] [{priority}] {due_date} {todo}"
    listbox_todo.delete(todo_index)
    listbox_todo.insert(todo_index, todo_text)

    entry_todo.delete(0, tk.END)
    todo_index = None
    sort_todo()

def done_todo():
    global todo_index
    not_yet = "[미완료]"
    job_done = "[완료함]"
    selected = listbox_todo.curselection()

    todo_index = selected[0]
    selected_todo = listbox_todo.get(todo_index)
    todo_status = selected_todo[:5]
    
    if todo_status == not_yet:
        selected_todo = job_done+selected_todo[5:]
        listbox_todo.delete(selected[0])
        listbox_todo.insert(selected[0], selected_todo)
    
    else:
        selected_todo = not_yet+selected_todo[5:]
        listbox_todo.delete(selected[0])
        listbox_todo.insert(selected[0], selected_todo)

    sort_todo()


def sort_todo():
    todo_items = list(listbox_todo.get(0, tk.END))

   
    def get_due(item):
        parts = item.split(" ")
        due = parts[2]
        return due

    todo_items.sort(key=get_due)

    listbox_todo.delete(0, tk.END)

    for item in todo_items:
        listbox_todo.insert(tk.END, item)


#메뉴바 함수
def new_list():
    if listbox_todo.size() == 0:
        return

    answer = messagebox.askyesno("새 목록", "새 목록을 만드시겠습니까? \n 현재 목록은 저장되지 않습니다.")

    if answer:
        listbox_todo.delete(0, tk.END)

def save_list():
    filepath = filedialog.asksaveasfilename(
        parent=window,
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        initialfile="todolist"
    )
    if filepath:
        todolist = listbox_todo.get(0, tk.END)
    with open(filepath, "w", encoding="utf-8") as file:
        for item in todolist:
            file.write(item + "\n")

def load_list():
    if not listbox_todo.size() == 0:
        answer = messagebox.askyesno("불러오기", "목록을 불러오시겠습니까? \n 현재 목록은 저장되지 않습니다.")
        if not answer:
            return

    filepath = filedialog.askopenfilename(
        parent=window,
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if filepath:
        with open(filepath, 'r', encoding='utf-8') as file:
            todolist = file.read().splitlines()

        listbox_todo.delete(0, tk.END)

        for todo in todolist:
            listbox_todo.insert(tk.END, todo)

    sort_todo()

def exit_program():
    answer = messagebox.askyesno("종료", "프로그램을 종료하시겠습니까?")

    if answer:
        window.destroy()

def about():
    msg = '''나의 TO-DO List ver.1.0
    제작자: 김승환
    날짜: 2026.09.30'''
    label = messagebox.showinfo("About", msg)

###
window = tk.Tk()
window.title("나의 TO-DO List")
window.geometry("500x500")

#메뉴바
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="파일", menu=file_menu)

file_menu.add_command(label="새 목록", command=new_list)
file_menu.add_command(label="저장", command=save_list)
file_menu.add_command(label="불러오기", command=load_list)
file_menu.add_separator()
file_menu.add_command(label="종료", command=exit_program)

help_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="도움말", menu=help_menu)

help_menu.add_command(label="프로그램 정보", command=about)


#등록된 할일 목록 프레임
label_list = tk.Label(window, text="할일 목록")
label_list.pack()

frame_list = tk.Frame(window)
frame_list.pack(padx=20, pady=5, fill="both", expand=True)

scrollbar = tk.Scrollbar(frame_list)
scrollbar.pack(side="right", fill="y")

listbox_todo = tk.Listbox(
    frame_list,
    width=50,
    height=10,
    yscrollcommand=scrollbar.set
)
listbox_todo.pack(fill="both", expand=True)
listbox_todo.bind("<Double-Button-1>", start_edit)
scrollbar.config(command=listbox_todo.yview)

#버튼
frame_buttons = tk.Frame(window)
frame_buttons.pack(padx=20, pady=5)

button_done = tk.Button(frame_buttons, text="완료 표시", command=done_todo)
button_done.pack(side="top", padx=5, pady=5, ipadx=50)

button_add = tk.Button(frame_buttons, text="추가", command=add_todo)
button_add.pack(side="left", padx=5, pady=5)

button_edit = tk.Button(frame_buttons, text="수정", command=edit_todo)
button_edit.pack(side="left", padx=5, pady=5)

button_delete = tk.Button(frame_buttons, text="삭제", command=delete_todo)
button_delete.pack(side="left", padx=5, pady=5)


#할일 입력 프레임
frame_input = tk.Frame(window)
frame_input.pack(pady=20)

label_todo = tk.Label(frame_input, text="할일")
label_todo.grid(row=0, column=1, columnspan=3)

entry_todo = tk.Entry(frame_input, width=30)
entry_todo.grid(row=1, column=1, columnspan=3, pady=10)


label_priority = tk.Label(frame_input, text="우선순위")
label_priority.grid(row=2, column=1)

priority_var = tk.StringVar()
priority_var.set("보통")

tk.Radiobutton(frame_input, text="높음", value="높음", variable=priority_var).grid(row=3, column=1)

tk.Radiobutton(frame_input, text="보통", value="보통", variable=priority_var).grid(row=4, column=1)

tk.Radiobutton(frame_input, text="낮음", value="낮음", variable=priority_var).grid(row=5, column=1)

label_priority = tk.Label(frame_input, text="마감일")
label_priority.grid(row=2, column=3)

date_picker = DateEntry(frame_input, width=12, background='grey', foreground='darkblue', borderwidth=2, date_pattern='yyyy-mm-dd')
date_picker.grid(row=3, column=3)



window.mainloop()