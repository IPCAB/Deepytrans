import tkinter as tk
from tkinter import filedialog
import requests
import time  # 导入 time 模块以便使用 sleep 函数

def translate_text(text):
    url = "http://127.0.0.1:1188/translate"  # 请确保这是正确的URL
    payload = {
        "text": text,
        "source_lang": "auto",
        "target_lang": "ZH"
    }
    headers = {
        'Content-Type': 'application/json'
    }

    # 发送POST请求
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # 这会在HTTP请求错误时抛出异常
    except requests.RequestException as e:
        return f"Error: There was a problem with the request: {e}"

    try:
        response_json = response.json()
    except ValueError:
        # JSON解析失败
        return f"Error: JSON decode error with response: {response.text}"
    
    # 检查JSON响应内容
    if 'data' in response_json:
        return response_json['data']
    else:
        # 响应中没包含预期的字段
        return f"Error: Received an unexpected response format: {response.text}"

def chunk_text(text, size=4500):
    punctuations = ['.', ',']
    chunks = []
    while len(text) > size:
        last_valid_index = -1
        for punctuation in punctuations:
            last_index = text.rfind(punctuation, 0, size)
            if last_index > last_valid_index:
                last_valid_index = last_index
        if last_valid_index == -1:
            last_valid_index = size - 1
        chunks.append(text[:last_valid_index + 1])
        text = text[last_valid_index + 1:].strip()  # Strip leading whitespace from the next chunk
    chunks.append(text)
    return chunks

def translate_and_output_chunks(chunks):
    translated_chunks = []
    for i, chunk in enumerate(chunks):
        if i > 0:  
            time.sleep(3)  # 在每次翻译之间暂停3秒钟
        translated_content = translate_text(chunk)
        translated_chunks.append(translated_content)
    return "\n".join(translated_chunks)

def save_translation_to_file(translated_content):
    # 直接将翻译内容保存到根目录的 results.txt 文件
    with open('results.txt', 'w', encoding='utf-8') as file:
        file.write(translated_content)
    print("The translated content has been saved to 'results.txt'.")

def select_and_translate_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if not content.strip():
                    messagebox.showerror("Empty File", "The selected file is empty.")
                    return
                else:
                    if len(content) > 4500:
                        chunks = chunk_text(content)
                        translated_content = translate_and_output_chunks(chunks)
                    else:
                        translated_content = translate_text(content)
                    save_translation_to_file(translated_content)
        except IOError as e:
            messagebox.showerror("Error", f"Error reading file {file_path}: {e}")

# 创建主窗口实例
root = tk.Tk()
root.withdraw()  # 隐藏主窗口

# 选择文件，开始翻译流程
select_and_translate_file()

# 启动主循环，等待事件
root.mainloop()

input("Press Enter to exit...")