import os
import webbrowser

def open_chrome():
    webbrowser.open(r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    print(">>> 已打开 Chrome 浏览器")

def open_vscode():
    vscode_path = r'C:\Users\admin\AppData\Local\Programs\Microsoft VS Code\Code.exe'
    try:
        if os.path.exists(vscode_path):
            os.startfile(vscode_path)
            print(">>> 已打开 Visual Studio Code")
        else:
            alternative_paths = [
                r'C:\Program Files\Microsoft VS Code\Code.exe',
                r'C:\Program Files (x86)\Microsoft VS Code\Code.exe',
            ]
            found = False
            for path in alternative_paths:
                if os.path.exists(path):
                    os.startfile(path)
                    print(f">>> 已打开 Visual Studio Code (从 {path})")
                    found = True
                    break
            if not found:
                print(f">>> 错误：未找到 VS Code，请检查路径: {vscode_path}")
    except Exception as e:
        print(f">>> 打开 VS Code 时出错: {e}")

def open_temp_folder():
    os.startfile(r'c:\temp')
    print(">>> 已打开 c:\\temp 文件夹")

def open_hkt_command_file():
    os.startfile(
        r'C:\Users\admin\Documents\BaiduSyncdisk\思维\HKT\常用命令.txt'
    )
    print(">>> 已打开 HKT 常用命令.txt")