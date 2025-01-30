import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox, ttk
import threading
import ctypes
from ctypes import wintypes
import os
import shutil
import sys
import webbrowser
from tkinter import Toplevel, Text
from PIL import Image, ImageTk
import requests
import zipfile
import subprocess


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Me緩存12.23")
        self.root.geometry("600x700")
        self.root.config(bg="#323232")
        self.root.resizable(True, True)
        self.set_title_bar_color('#323232')
        self.center_window()

        self.current_version = "v1.0.0"  # 当前版本号
        self.config_folders = {
            "强力（本人用的这个）": self.get_resource_path("Config_op"),
            "人性化（不容易被踢）": self.get_resource_path("Config_human"),
            "强力（2K分辨率）": self.get_resource_path("Config_op-2K"),
            "人性化（2K分辨率）": self.get_resource_path("Config_human-2K")
        }

        self.selected_path = None
        self.setup_ui()
        self.start_log_clear_timer()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.check_for_updates()  # 启动时检查更新

    def center_window(self):
        window_width, window_height = 850, 700
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = (screen_height - window_height) // 2
        position_right = (screen_width - window_width) // 2
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    def get_resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def setup_ui(self):
        # 创建第一个按钮框架
        top_button_frame = tk.Frame(self.root, bg="#323232")
        top_button_frame.pack(anchor=tk.CENTER, pady=15)

        first_buttons = [("金币号", self.open_gold_coin_link, "点击打开金币号链接"),
                         ("一手黑号", self.open_qukapu_link, "点击打开一手黑号链接,买的号有问题打开网页上面的售后地址联系客服处理"),
                         ("更新地址", self.update_url, "点击打开更新地址网页"),
                         ("软件使用说明", self.show_usage, "查看使用说明"),
                         ("BOT更新日志", self.show_update_log, "查看BOT更新日志"),
                         ("BOT推荐英雄", self.show_recommended_heroes, "查看BOT推荐英雄"),
                         ("Me群", self.open_Qqun_link, "点击加入Me缓存交流群,群号692856687")]

        for i, (text, command, message) in enumerate(first_buttons):
            self.create_button(top_button_frame, text, command, message, i)

        # 创建第二个按钮框架（BOT相关）
        bot_button_frame = tk.Frame(self.root, bg="#323232")
        bot_button_frame.pack(anchor=tk.CENTER, pady=15)

        bot_other_buttons = [("选择BOT位置", self.select_path, "选择Hanbot位置，位置应该是 xxxxx/league of legends"),
                             ("导入BOT缓存", self.import_cache, "导入BOT缓存")]

        for j, (text, command, message) in enumerate(bot_other_buttons):
            self.create_button(bot_button_frame, text, command, message, j)

        bot_dropdown_frame = tk.Frame(self.root, bg="#323232")
        bot_dropdown_frame.pack(anchor=tk.CENTER, pady=0)

        self.cache_choice = tk.StringVar(value="请选择BOT缓存类型")
        self.cache_dropdown = ttk.Combobox(bot_dropdown_frame, textvariable=self.cache_choice,
                                           values=list(self.config_folders.keys()), state="readonly")
        self.cache_dropdown.pack()

        self.message_label = tk.Label(self.root, text="", fg="#ffffff", bg="#323232")
        self.message_label.pack()
        self.path_label = tk.Label(self.root, text="未选择", fg="#ffffff", bg="#323232")
        self.path_label.pack()
        self.log_area = scrolledtext.ScrolledText(self.root, width=90, height=40, bg="#1e1e1e", fg="#ffffff",
                                                   insertbackground="white")
        self.log_area.pack()

    def set_title_bar_color(self, color):
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(ctypes.c_int(2)),
                                                   ctypes.sizeof(ctypes.c_int()))
        hbrush = ctypes.windll.gdi32.CreateSolidBrush(wintypes.COLORREF(int(color[1:], 16)))
        ctypes.windll.user32.SetClassLongPtrW(hwnd, -10, hbrush)

    def create_button(self, parent, text, command, message, column):
        button = tk.Button(parent, text=text, command=command, bd=0, width=10, height=2, bg="#5e5e5e", fg="#ffffff",
                           font=("Microsoft YaHei", 12, "bold"))
        button.grid(row=0, column=column, padx=5, pady=5)
        button.bind("<Enter>", lambda event: self.message_label.config(text=message))
        button.bind("<Leave>", lambda event: self.message_label.config(text=""))

    def log(self, message):
        self.log_area.insert(tk.END, message + '\n')
        self.log_area.see(tk.END)

    def open_gold_coin_link(self):
        webbrowser.open("https://www.liyan666.com/shop/CE33E79C")

    def update_url(self):
        webbrowser.open("https://share.feijipan.com/s/3xCZwlHZ")

    def open_qukapu_link(self):
        webbrowser.open("https://www.yuque.com/medaxia-4sbtu/dmb9ah/qz2hgob1bcoer3yy")

    def open_Qqun_link(self):
        webbrowser.open("https://qm.qq.com/q/3fgEPk64VO")

    def select_path(self):
        self.selected_path = filedialog.askdirectory()
        if self.selected_path and self.validate_path(self.selected_path):
            self.path_label.config(text=f"缓存位置: {self.selected_path}")
            self.log("选择成功！")
        else:
            self.path_label.config(text="错误，请重新选择正确的位置。")
            self.log("位置应该是 xxxxx/league of legends，如果你确定你选的是正确的目录直接导入即可")
            messagebox.showerror("错误", "请选择正确的缓存位置。")

    def import_cache(self):
        if self.selected_path:
            self.clear_cache(self.selected_path)
            self.copy_config(self.selected_path)
        else:
            messagebox.showerror("错误", "请先选择正确的Hanbot文件位置")
            self.log("错误: 请先选择正确的Hanbot文件位置")

    def clear_cache(self, path):
        try:
            self.log("(1/4)导入缓存中...")

            saves_folder = os.path.join(path, "saves")
            for item in os.listdir(saves_folder):
                item_path = os.path.join(saves_folder, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)

            for file in ["config.ini", "hc.dat"]:
                file_path = os.path.join(path, file)
                if os.path.exists(file_path):
                    os.remove(file_path)

            self.log("(2/4)导入缓存中...")
        except Exception as e:
            self.log(f"错误: 导入缓存失败 {str(e)}")

    def copy_config(self, path):
        try:
            self.log("(3/4)导入缓存中...")
            config_folder = self.config_folders.get(self.cache_choice.get())

            if not config_folder:
                self.log("请选择缓存类型。")
                return

            self.log("(4/4)导入缓存中...")

            for item in os.listdir(config_folder):
                s = os.path.join(config_folder, item)
                d = os.path.join(path, item)
                if item in ['config.ini', 'hc.dat', 'shards.json']:
                    # 删除旧的文件，复制新的文件
                    if os.path.exists(d):
                        os.remove(d)
                    shutil.copy2(s, d)

                elif item == 'saves':
                    # 删除saves文件夹中的所有文件，复制新的文件
                    if os.path.exists(d):
                        for file in os.listdir(d):
                            file_path = os.path.join(d, file)
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                    if not os.path.exists(d):
                        os.makedirs(d)
                    for save_item in os.listdir(s):
                        save_s = os.path.join(s, save_item)
                        save_d = os.path.join(d, save_item)
                        if os.path.isdir(save_s):
                            shutil.copytree(save_s, save_d)
                        else:
                            shutil.copy2(save_s, save_d)

                elif item == 'shards':
                    # 直接复制新的shards文件夹中的内容，不删除旧的内容
                    if not os.path.exists(d):
                        os.makedirs(d)
                    for shard_item in os.listdir(s):
                        shard_s = os.path.join(s, shard_item)
                        shard_d = os.path.join(d, shard_item)
                        if os.path.isdir(shard_s):
                            if not os.path.exists(shard_d):
                                shutil.copytree(shard_s, shard_d)
                            else:
                                for sub_item in os.listdir(shard_s):
                                    sub_s = os.path.join(shard_s, sub_item)
                                    sub_d = os.path.join(shard_d, sub_item)
                                    if os.path.isdir(sub_s):
                                        shutil.copytree(sub_s, sub_d)
                                    else:
                                        shutil.copy2(sub_s, sub_d)
                        else:
                            shutil.copy2(shard_s, shard_d)

                self.log("缓存导入成功！")
        except Exception as e:
            self.log(f"错误: 导入缓存失败 {str(e)}")

    def validate_path(self, path):
        if os.path.exists(os.path.join(path, "saves")):
            return True
        self.log("错误: 位置应该是 xxxxx/league of legends 里面应该要有saves文件夹。")
        return False

    def start_log_clear_timer(self):
        self.root.after(3600000, self.clear_log_every_hour)

    def clear_log_every_hour(self):
        self.log_area.delete('1.0', tk.END)
        self.log("已清除日志")
        self.start_log_clear_timer()

    def on_closing(self):
        self.root.destroy()

    def show_update_log(self):
        log_window = Toplevel(self.root)
        log_window.title("更新日志")
        text_area = Text(log_window, wrap=tk.WORD, bg="#1e1e1e", fg="#ffffff", insertbackground="white",
                         font=("Helvetica", 18))
        text_area.pack(fill=tk.BOTH, expand=True)
        try:
            # 获取当前脚本所在目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # 构建更新日志文件的完整路径
            update_log_path = os.path.join(script_dir, "更新日志.txt")
            with open(update_log_path, "r", encoding="utf-8") as f:
                update_log_text = f.read()
        except FileNotFoundError:
            update_log_text = "未找到更新日志文件。"
        text_area.insert(tk.END, update_log_text)
        text_area.configure(state='disabled')

        def center_update_log_window():
            log_window.update_idletasks()
            window_width = log_window.winfo_reqwidth()
            window_height = log_window.winfo_reqheight()
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            position_top = (screen_height - window_height) // 2
            position_right = (screen_width - window_width) // 2
            log_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        center_update_log_window()

    def show_usage(self):
        usage_window = Toplevel(self.root)
        usage_window.title("软件使用说明")

        # 获取当前脚本的绝对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(script_dir, "软件使用说明.png")
        img = Image.open(img_path)
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(usage_window, image=img_tk)
        label.image = img_tk
        label.pack()

    def show_recommended_heroes(self):
        heroes_window = Toplevel(self.root)
        heroes_window.title("推荐英雄")

        # 获取当前脚本的绝对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(script_dir, "推荐英雄.png")
        img = Image.open(img_path)
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(heroes_window, image=img_tk)
        label.image = img_tk
        label.pack()

    def check_for_updates(self):
        """检查是否有新版本"""
        try:
            repo_url = "https://api.github.com/repos/你的用户名/你的仓库名/releases/latest"
            response = requests.get(repo_url)
            if response.status_code == 200:
                latest_release = response.json()
                latest_version = latest_release['tag_name']
                if latest_version != self.current_version:
                    self.log(f"发现新版本: {latest_version}")
                    if messagebox.askyesno("更新", f"发现新版本 {latest_version}，是否立即更新？"):
                        self.download_and_install_update(latest_release)
                else:
                    self.log("当前已是最新版本。")
            else:
                self.log("无法检查更新，请检查网络连接。")
        except Exception as e:
            self.log(f"检查更新时出错: {str(e)}")

    def download_and_install_update(self, latest_release):
        """下载并安装更新"""
        try:
            # 获取下载链接
            asset_url = latest_release['assets'][0]['browser_download_url']
            self.log(f"正在下载更新: {asset_url}")

            # 下载文件
            local_filename = "update.zip"
            with requests.get(asset_url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            # 解压文件
            self.log("正在安装更新...")
            with zipfile.ZipFile(local_filename, 'r') as zip_ref:
                zip_ref.extractall(".")

            # 删除临时文件
            os.remove(local_filename)
            self.log("更新安装完成，即将重启程序。")

            # 重启程序
            self.restart_program()
        except Exception as e:
            self.log(f"更新失败: {str(e)}")

    def restart_program(self):
        """重启程序"""
        python = sys.executable
        os.execl(python, python, *sys.argv)


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()