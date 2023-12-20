import tkinter as tk


def encrypt_text(e):
    t = ["", "g", "h", "i"]
    i = "wx3cba883abac619bb"
    a = ""
    n = 0
    for s in range(len(e)):
        r = ord(e[s]) + 2
        if n >= len(i):
            n = 0
        r += ord(i[n])
        o = format(r, 'x')
        if len(o) < 4:
            h = t[4 - len(o)]
            o = h + o
        a += o.lower()
        n += 1
    return a


def encrypt_and_display():
    input_text = input_textbox.get("1.0", "end-1c")
    encrypted_text = encrypt_text(input_text)
    output_textbox.delete("1.0", "end")
    output_textbox.insert("1.0", encrypted_text)

    # 获取目标URL
    url_prefix = "https://zwqd.ayit.edu.cn/Seatresv/SeatOrder.asp?"

    # 创建完整的加密URL
    full_url = url_prefix + encrypted_text
    target_url_textbox.delete("1.0", "end")
    target_url_textbox.insert("1.0", full_url)


# 创建主窗口
window = tk.Tk()
window.title("文本加密工具")

# 获取屏幕宽度和高度
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# 设置窗口的大小和位置
window_width = 520
window_height = 450
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# 创建一个网格布局
window.grid_rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

# 创建"加密前"标签
input_label = tk.Label(window, text="加密前：")
input_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# 创建输入文本框
input_textbox = tk.Text(window, height=6, width=50)
input_textbox.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

# 创建"加密后"标签
output_label = tk.Label(window, text="加密后：")
output_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

# 创建显示加密后文本的文本框
output_textbox = tk.Text(window, height=10, width=60)
output_textbox.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

# 创建"目标URL"标签
target_url_label = tk.Label(window, text="目标URL：")
target_url_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

# 创建目标URL文本框
target_url_textbox = tk.Text(window, height=10, width=60)
target_url_textbox.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

# 创建加密按钮
encrypt_button = tk.Button(window, text="加密文本", command=encrypt_and_display, width=55, height=1, bg="#91B859")
encrypt_button.grid(row=3, column=1, pady=5)

# 运行主循环
window.mainloop()
