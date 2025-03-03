from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import os

# 定义函数将文件名和密码保存到密码本TXT文件中
def save_password_to_book(file_name, password):
    password_book_path = 'password_book.txt'  # 设置密码本文件路径
    try:
        file_basename = os.path.basename(file_name)  # 获取文件名部分
        # 确保文件存在，如果不存在则创建文件
        if not os.path.exists(password_book_path):
            with open(password_book_path, 'w', encoding='utf-8') as file:
                file.write("Password Book\n\n")  # 写入文件头部
        
        # 打开文件并追加内容
        with open(password_book_path, 'a', encoding='utf-8') as file:
            file.write(f"File: {file_basename}, Password: {password}\n")  # 写入文件名和密码
        print(f"保存文件名和密码到 {password_book_path}")  # 调试信息
    except Exception as e:
        print(f"保存密码本时出现错误: {str(e)}")  # 错误信息

# 定义函数解析HTML文件
def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    return str(soup)

def encrypt_code(code, password):
    key = password.ljust(32)[:32].encode('utf-8')  # 密钥填充或截断到32字节
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_code = cipher.encrypt(pad(code.encode('utf-8'), AES.block_size))
    return base64.b64encode(encrypted_code).decode('utf-8')

def create_encrypted_html(encrypted_code):
    decrypt_script = f"""
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.0.0/crypto-js.min.js"></script>
    <script>
    function decrypt() {{
        var encrypted_code = "{encrypted_code}";
        var password = document.getElementById('password_entry').value;
        try {{
            var key = CryptoJS.enc.Utf8.parse(password.padEnd(32, ' '));  // 密钥填充到32字节
            var decrypted = CryptoJS.AES.decrypt(encrypted_code, key, {{
                mode: CryptoJS.mode.ECB,
                padding: CryptoJS.pad.Pkcs7
            }});
            var decryptedText = decrypted.toString(CryptoJS.enc.Utf8);
            if (!decryptedText) {{
                throw new Error("解密失败");
            }}
            document.open();
            document.write(decryptedText);
            document.close();
        }} catch (e) {{
            alert("解密失败，请检查密码是否正确。");
        }}
    }}
    function togglePassword() {{
        var passwordInput = document.getElementById('password_entry');
        var eyeIcon = document.getElementById('eye_icon');
        if (passwordInput.type === 'password') {{
            passwordInput.type = 'text';
            eyeIcon.textContent = '🔒';
        }} else {{
            passwordInput.type = 'password';
            eyeIcon.textContent = '👁️';
        }}
    }}
    </script>
    <style>
    body {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: #f0f0f0;
        font-family: Arial, sans-serif;
        margin: 0;
    }}
    .container {{
        text-align: center;
        width: 100%;
        max-width: 450px;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        background: #fff;
        border-radius: 8px;
    }}
    .button-container {{
        margin-top: 20px;
    }}
    button {{
        width: 100%;
        padding: 20px;
        font-size: 20px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    @media only screen and (max-width: 600px) {{
        button {{
            padding: 15px;
            font-size: 18px;
        }}
    }}
    button:hover {{
        background-color: #0056b3;
    }}
    .password-container {{
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .password-entry {{
        width: calc(100% - 30px);
        padding: 12px;
        font-size: 18px;
        border: 1px solid #ccc;
        border-radius: 5px 0 0 5px;
        outline: none;
    }}
    .eye-icon {{
        padding: 12px;
        cursor: pointer;
        background: #ccc;
        border: 1px solid #ccc;
        border-radius: 0 5px 5px 0;
    }}
    </style>
    <div class="container">
        <div class="password-container">
            <input type="password" class="password-entry" id="password_entry" placeholder="输入密码...">
            <span class="eye-icon" id="eye_icon" onclick="togglePassword()">👁️</span>
        </div>
        <div class="button-container">
            <button onclick="decrypt()">🔓 解密页面</button>
        </div>
    </div>
    """
    return decrypt_script

def save_html(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("HTML 文件", "*.html")])
    if file_path:
        input_file_entry.delete(0, tk.END)
        input_file_entry.insert(0, file_path)

def toggle_password(entry, button):
    if entry['show'] == '*':
        entry['show'] = ''
        button.config(text='🔒')  # 更新按钮文本为眼睛关闭状态
    else:
        entry['show'] = '*'
        button.config(text='👁️')  # 更新按钮文本为眼睛开启状态

def encrypt_html():
    input_html = input_file_entry.get()
    output_html = input_html.replace(".html", "🔒.html")
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if not input_html:
        messagebox.showerror("错误", "请选择输入HTML文件。")
        return

    if not password or not confirm_password:
        messagebox.showerror("错误", "请输入密码并确认密码。")
        return

    if password != confirm_password:
        messagebox.showerror("错误", "密码和确认密码不匹配，请重新输入。")
        return

    try:
        html_code = parse_html(input_html)
        encrypted_code = encrypt_code(html_code, password)
        decrypt_script = create_encrypted_html(encrypted_code)
        encrypted_html_content = f"<html><body>{decrypt_script}</body></html>"
        save_html(output_html, encrypted_html_content)
        save_password_to_book(output_html, password)  # 保存文件名和密码到密码本
        messagebox.showinfo("完成", "HTML 文件已成功加密并保存。")
    except Exception as e:
        messagebox.showerror("错误", f"加密过程中出现错误: {str(e)}")

app = tk.Tk()
app.title("🔒 HTML 加密工具")

frame = tk.Frame(app, padx=10, pady=10)
frame.pack(padx=10, pady=10)

input_file_label = tk.Label(frame, text="选择要加密的HTML文件:")
input_file_label.grid(row=0, column=0, sticky='e')

input_file_entry = tk.Entry(frame, width=40)
input_file_entry.grid(row=0, column=1)

browse_button = tk.Button(frame, text="浏览", command=select_file)
browse_button.grid(row=0, column=2, padx=5)

password_label = tk.Label(frame, text="设置密码:")
password_label.grid(row=1, column=0, sticky='e')

# 在创建密码输入框和小眼睛按钮时，确保初始状态正确
password_entry = tk.Entry(frame, width=40, show='*')
password_entry.grid(row=1, column=1)

toggle_password_button = tk.Button(frame, text='👁️', command=lambda: toggle_password(password_entry, toggle_password_button))
toggle_password_button.grid(row=1, column=2, padx=5)

confirm_password_label = tk.Label(frame, text="确认密码:")
confirm_password_label.grid(row=2, column=0, sticky='e')

confirm_password_entry = tk.Entry(frame, width=40, show='*')
confirm_password_entry.grid(row=2, column=1)

toggle_confirm_password_button = tk.Button(frame, text='👁️', command=lambda: toggle_password(confirm_password_entry, toggle_confirm_password_button))
toggle_confirm_password_button.grid(row=2, column=2, padx=5)

encrypt_button = tk.Button(frame, text="加密 HTML", command=encrypt_html)
encrypt_button.grid(row=3, columnspan=3, pady=10)

app.mainloop()
