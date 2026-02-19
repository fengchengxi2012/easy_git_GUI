import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import webbrowser
import pyperclip


def showmenu(event):
    menu.post(event.x_root, event.y_root)

def set_side(value):
    global side
    side = value
    entry.configure(placeholder=f"{side} Repo")
    
def confirm():
    global side
    global entry2
    real = side
    repo = entry.get()
    if not repo:
        messagebox.showwarning("Warning", "Please enter repository name")
        return
        
    if side == "gitlab":
        real = 'about.gitlab'
    
    webadress = f"https://{real}.com/{repo}"
    
    # Update the second entry
    entry2.delete(0, tk.END)
    entry2.insert(0, webadress)
        
def last():
    global a
    url = entry2.get()
    if not url:
        messagebox.showwarning("Warning", "URL is empty")
        return
        
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            messagebox.showinfo("Success", "✅ URL is valid!")
            a = 1
        else:
            messagebox.showwarning("Warning", f"❌ URL not found (Status: {response.status_code})")
            a = 0
    except requests.ConnectionError:
        messagebox.showerror("Error", "❌ Cannot connect to server")
    except requests.Timeout:
        messagebox.showerror("Error", "❌ Connection timeout")
    except Exception as e:
        messagebox.showerror("Error", f"❌ {str(e)}")
        
def copy_url():
    """Copy URL to clipboard"""
    url = entry2.get()
    if not url:
        messagebox.showwarning("Warning", "No URL to copy")
        return
    
    try:
        pyperclip.copy(url)
        messagebox.showinfo("Success", "✅ URL copied to clipboard!")
    except:
        # Fallback method
        root.clipboard_clear()
        root.clipboard_append(url)
        messagebox.showinfo("Success", "✅ URL copied to clipboard!")
    
def download_repo():
    """Open download link in browser"""
    url = entry2.get()
    if not url:
        messagebox.showwarning("Warning", "Please generate a URL first")
        return
    
    # Convert to download URL
    if "github.com" in url:
        # GitHub: Add /archive/refs/heads/main.zip
        download_url = url + "/archive/refs/heads/main.zip"
    elif "gitlab.com" in url:
        # GitLab: Add /-/archive/main/
        download_url = url + "/-/archive/main/" + url.split('/')[-1] + "-main.zip"
    elif "gitee.com" in url:
        # Gitee: Add /repository/archive/main.zip
        download_url = url + "/repository/archive/main.zip"
    else:
        download_url = url
    
    # Open in browser
    webbrowser.open(download_url)
    messagebox.showinfo("Download", "Opening download link in browser...")

root = tk.Tk()
root.title("Easy Git GUI")
side = 'github'
root.geometry("450x600")

# Menu
menu = tk.Menu(root, tearoff=0)
menu.add_command(label="github", command=lambda: set_side('github'))
menu.add_command(label="gitlab", command=lambda: set_side('gitlab'))
menu.add_command(label="gitee", command=lambda: set_side('gitee'))
menu.add_command(label="gitcode", command=lambda: set_side('gitcode'))
menu.add_separator()

# Title
title_label = ttk.Label(root, text="Git Repository URL Generator", font=("Arial", 12, "bold"))
title_label.place(x=20, y=20)

# Platform selection
platform_label = ttk.Label(root, text="Current platform:")
platform_label.place(x=20, y=60)

platform_value = ttk.Label(root, text=side, foreground="blue")
platform_value.place(x=130, y=60)

# Choose button
btn = ttk.Button(root, text="CHOOSE PLATFORM ↓")
btn.place(x=250, y=55)
btn.bind("<Button-1>", showmenu)

# First entry - repo name
repo_label = ttk.Label(root, text="Repository (user/repo):")
repo_label.place(x=20, y=100)

entry = ttk.Entry(root, width=40)
entry.place(x=20, y=125)
entry.insert(0, "username/repository")  # Example

# Confirm button
btn2 = ttk.Button(root, text="GENERATE URL", width=15, command=confirm)
btn2.place(x=280, y=122)

# Separator
ttk.Separator(root, orient='horizontal').place(x=20, y=170, width=400)

# Result section
result_label = ttk.Label(root, text="Generated URL:", font=("Arial", 10, "bold"))
result_label.place(x=20, y=190)

# Second entry - generated URL
entry2 = ttk.Entry(root, width=50)
entry2.place(x=20, y=220)

# Check URL button
btn3 = ttk.Button(root, text="CHECK URL", width=15, command=last)
btn3.place(x=320, y=218)

# Action buttons frame
actions_label = ttk.Label(root, text="Actions:", font=("Arial", 10, "bold"))
actions_label.place(x=20, y=270)

# COPY button
btn_copy = ttk.Button(root, text="📋 COPY URL", width=20, command=copy_url)
btn_copy.place(x=20, y=300)

# DOWNLOAD button
btn_download = ttk.Button(root, text="⬇️ DOWNLOAD", width=20, command=download_repo)
btn_download.place(x=200, y=300)

# Status section
status_label = ttk.Label(root, text="Status:", font=("Arial", 10, "bold"))
status_label.place(x=20, y=360)

# Status display
status_frame = ttk.Frame(root, relief="solid", borderwidth=1)
status_frame.place(x=20, y=390, width=400, height=60)

status_text = tk.StringVar()
status_text.set("Ready. Generate a URL and click CHECK URL")
status_display = ttk.Label(status_frame, textvariable=status_text, wraplength=380)
status_display.place(x=10, y=10)

# Instructions
instructions = """Instructions:
1. Choose platform (github/gitlab/gitee/gitcode)
2. Enter repository path (e.g., mherrmann/helium)
3. Click GENERATE URL
4. Click CHECK URL to verify
5. COPY URL or DOWNLOAD the repository"""
inst_label = ttk.Label(root, text=instructions, justify="left", foreground="gray")
inst_label.place(x=20, y=470)

root.mainloop()