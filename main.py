import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import webbrowser
import pyperclip

# ========== 配置颜色主题 ==========
COLORS = {
    'bg': '#f0f2f5',           # 背景色
    'primary': '#2d7a9e',       # 主色调（深蓝）
    'secondary': '#4a9ec1',     # 次要色（浅蓝）
    'success': '#28a745',       # 成功绿色
    'warning': '#ffc107',        # 警告黄色
    'danger': '#dc3545',         # 危险红色
    'text': '#1e1e2f',           # 文字颜色
    'text_light': '#6c757d',     # 浅色文字
    'card_bg': '#ffffff',        # 卡片背景
    'border': '#dee2e6'          # 边框颜色
}

# 先定义全局变量
side = 'github'

def showmenu(event):
    menu.post(event.x_root, event.y_root)

def set_side(value):
    global side
    side = value
    entry.configure(placeholder=f"{side} Repo")
    platform_value.config(text=side)
    
def confirm():
    global side
    global entry2
    real = side
    repo = entry.get().strip()
    if not repo or repo == "username/repository":
        messagebox.showwarning("Warning", "Please enter repository name")
        return
        
    if side == "gitlab":
        real = 'about.gitlab'
    
    webadress = f"https://{real}.com/{repo}"
    
    entry2.delete(0, tk.END)
    entry2.insert(0, webadress)
    status_text.set("✅ URL generated! Click CHECK URL to verify")
    
def last():
    url = entry2.get()
    if not url:
        messagebox.showwarning("Warning", "URL is empty")
        return
        
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            messagebox.showinfo("Success", "✅ URL is valid!")
            status_text.set("✅ URL is valid and accessible")
        else:
            messagebox.showwarning("Warning", f"❌ URL not found (Status: {response.status_code})")
            status_text.set(f"❌ URL returned status {response.status_code}")
    except requests.ConnectionError:
        messagebox.showerror("Error", "❌ Cannot connect to server")
        status_text.set("❌ Connection failed - check your internet")
    except requests.Timeout:
        messagebox.showerror("Error", "❌ Connection timeout")
        status_text.set("❌ Connection timeout - server too slow")
    except Exception as e:
        messagebox.showerror("Error", f"❌ {str(e)}")
        status_text.set(f"❌ Error: {str(e)[:30]}...")
        
def copy_url():
    url = entry2.get()
    if not url:
        messagebox.showwarning("Warning", "No URL to copy")
        return
    
    try:
        pyperclip.copy(url)
        messagebox.showinfo("Success", "✅ URL copied to clipboard!")
        status_text.set("✅ URL copied to clipboard")
    except:
        root.clipboard_clear()
        root.clipboard_append(url)
        messagebox.showinfo("Success", "✅ URL copied to clipboard!")
        status_text.set("✅ URL copied to clipboard")
    
def download_repo():
    url = entry2.get()
    if not url:
        messagebox.showwarning("Warning", "Please generate a URL first")
        return
    
    # Show download options dialog
    download_window = tk.Toplevel(root)
    download_window.title("Download Options")
    download_window.geometry("300x200")
    download_window.configure(bg=COLORS['card_bg'])
    download_window.resizable(False, False)
    
    # Center the window
    download_window.transient(root)
    download_window.grab_set()
    
    x = root.winfo_x() + (root.winfo_width() // 2) - 150
    y = root.winfo_y() + (root.winfo_height() // 2) - 100
    download_window.geometry(f"+{x}+{y}")
    
    ttk.Label(download_window, text="Choose branch:", 
              font=("Arial", 10, "bold")).pack(pady=10)
    
    branch_var = tk.StringVar(value="main")
    ttk.Radiobutton(download_window, text="main", variable=branch_var, 
                   value="main").pack()
    ttk.Radiobutton(download_window, text="master", variable=branch_var, 
                   value="master").pack()
    
    def start_download():
        branch = branch_var.get()
        download_window.destroy()
        
        if "github.com" in url:
            download_url = f"{url}/archive/refs/heads/{branch}.zip"
        elif "gitlab.com" in url:
            repo_name = url.split('/')[-1]
            download_url = f"{url}/-/archive/{branch}/{repo_name}-{branch}.zip"
        elif "gitee.com" in url:
            download_url = f"{url}/repository/archive/{branch}.zip"
        else:
            download_url = url
        
        webbrowser.open(download_url)
        status_text.set(f"⬇️ Downloading {branch} branch...")
        messagebox.showinfo("Download", f"Opening {branch} branch download link...")
    
    ttk.Button(download_window, text="Download", command=start_download).pack(pady=20)

# ========== 创建主窗口 ==========
root = tk.Tk()
root.title("Easy Git GUI - Repository Manager")
root.geometry("500x650")
root.configure(bg=COLORS['bg'])
root.resizable(False, False)

# 设置样式
style = ttk.Style()
style.theme_use('clam')

# 配置自定义样式
style.configure('Primary.TButton', 
                background=COLORS['primary'],
                foreground='white',
                borderwidth=0,
                focuscolor='none',
                font=('Arial', 9, 'bold'))
style.map('Primary.TButton',
          background=[('active', COLORS['secondary'])])

style.configure('Success.TButton',
                background=COLORS['success'],
                foreground='white',
                borderwidth=0,
                font=('Arial', 9, 'bold'))

style.configure('Card.TFrame', 
                background=COLORS['card_bg'],
                relief='solid',
                borderwidth=1)

style.configure('Title.TLabel',
                font=('Arial', 14, 'bold'),
                foreground=COLORS['primary'],
                background=COLORS['bg'])

style.configure('Heading.TLabel',
                font=('Arial', 10, 'bold'),
                background=COLORS['bg'])

# ========== 创建菜单 ==========
menu = tk.Menu(root, tearoff=0, bg=COLORS['card_bg'], fg=COLORS['text'])
menu.add_command(label="github", command=lambda: set_side('github'))
menu.add_command(label="gitlab", command=lambda: set_side('gitlab'))
menu.add_command(label="gitee", command=lambda: set_side('gitee'))
menu.add_command(label="gitcode", command=lambda: set_side('gitcode'))
menu.add_separator()

# ========== 标题区域 ==========
title_frame = ttk.Frame(root, style='Card.TFrame')
title_frame.place(x=20, y=20, width=460, height=60)

title_label = ttk.Label(title_frame, text="📦 Git Repository URL Generator", 
                        style='Title.TLabel')
title_label.place(x=20, y=15)

# ========== 平台选择卡片 ==========
platform_card = ttk.Frame(root, style='Card.TFrame')
platform_card.place(x=20, y=90, width=460, height=80)

platform_label = ttk.Label(platform_card, text="Current Platform:", 
                          style='Heading.TLabel')
platform_label.place(x=15, y=15)

# 修复：这里语法错误，应该用 textvariable 或 text 参数
platform_value = ttk.Label(platform_card, text=side, 
                          font=("Arial", 11, "bold"),
                          foreground=COLORS['primary'],
                          background=COLORS['card_bg'])
platform_value.place(x=130, y=15)

btn = ttk.Button(platform_card, text="▼ CHOOSE PLATFORM", 
                style='Primary.TButton', width=20)
btn.place(x=250, y=10)
btn.bind("<Button-1>", showmenu)

# ========== 仓库输入卡片 ==========
repo_card = ttk.Frame(root, style='Card.TFrame')
repo_card.place(x=20, y=180, width=460, height=100)

repo_label = ttk.Label(repo_card, text="Repository (user/repo):", 
                      style='Heading.TLabel')
repo_label.place(x=15, y=15)

entry = ttk.Entry(repo_card, width=35, font=("Arial", 10))
entry.place(x=15, y=40)
entry.insert(0, "username/repository")

btn2 = ttk.Button(repo_card, text="GENERATE URL", 
                 style='Primary.TButton', width=15, command=confirm)
btn2.place(x=300, y=38)

# ========== URL显示卡片 ==========
url_card = ttk.Frame(root, style='Card.TFrame')
url_card.place(x=20, y=290, width=460, height=100)

url_label = ttk.Label(url_card, text="Generated URL:", 
                     style='Heading.TLabel')
url_label.place(x=15, y=15)

entry2 = ttk.Entry(url_card, width=42, font=("Arial", 9))
entry2.place(x=15, y=40)

btn3 = ttk.Button(url_card, text="CHECK URL", 
                 style='Primary.TButton', width=12, command=last)
btn3.place(x=340, y=38)

# ========== 操作按钮卡片 ==========
action_card = ttk.Frame(root, style='Card.TFrame')
action_card.place(x=20, y=400, width=460, height=80)

action_label = ttk.Label(action_card, text="Actions:", 
                        style='Heading.TLabel')
action_label.place(x=15, y=10)

btn_copy = ttk.Button(action_card, text="📋 COPY URL", 
                     style='Success.TButton', width=20, command=copy_url)
btn_copy.place(x=15, y=35)

btn_download = ttk.Button(action_card, text="⬇️ DOWNLOAD", 
                         style='Primary.TButton', width=20, command=download_repo)
btn_download.place(x=240, y=35)

# ========== 状态卡片 ==========
status_card = ttk.Frame(root, style='Card.TFrame')
status_card.place(x=20, y=490, width=460, height=80)

status_label = ttk.Label(status_card, text="Status:", 
                        style='Heading.TLabel')
status_label.place(x=15, y=10)

status_text = tk.StringVar()
status_text.set("👋 Ready to generate repository URLs")
status_display = ttk.Label(status_card, textvariable=status_text, 
                          font=("Arial", 9), wraplength=420,
                          background=COLORS['card_bg'])
status_display.place(x=15, y=35)

# ========== 底部装饰 ==========
footer_frame = tk.Frame(root, bg=COLORS['bg'], height=30)
footer_frame.place(x=0, y=580, width=500, height=30)

footer_text = tk.Label(footer_frame, 
                       text="Easy Git GUI v1.0 • Made with ❤️", 
                       bg=COLORS['bg'], fg=COLORS['text_light'],
                       font=("Arial", 8))
footer_text.pack(pady=5)

# ========== 运行主循环 ==========
root.mainloop()