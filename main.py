import tkinter as tk
from tkinter import ttk, messagebox
import pygame
import os
from PIL import Image, ImageTk
import random


class ChineseGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chinese Learning Game")
        self.root.geometry("1024x768")
        self.root.configure(bg='#f0f8ff')

        self.style = ttk.Style()
        self.style.configure('Game.TFrame', background='#f0f8ff')
        self.style.configure(
            'Game.TLabel', background='#f0f8ff', font=('Arial', 14))
        self.style.configure(
            'Title.TLabel', background='#f0f8ff', font=('Arial', 24, 'bold'))
        self.style.configure('Option.TButton', font=('Arial', 14), padding=10)

        self.score = 0
        self.current_question = 0

        pygame.mixer.init()
        self.load_sounds()

        self.questions = [
            {
                "question": "這是什麼動物？",
                "image": "panda.png",
                "options": ["熊貓", "貓", "猴子", "夠"],
                "correct": "熊貓",
                "translation": "Đây là con gì?"
            },
            {
                "question": "這是什麼動物？",
                "image": "rabbit.png",
                "options": ["龍", "雞腿", "老虎", "兔子"],
                "correct": "兔子",
                "translation": "Đây là con gì?"
            },
            {
                "question": "這是什麼東西？",
                "image": "computer.png",
                "options": ["手機", "電腦", "鞋子", "背包"],
                "correct": "電腦",
                "translation": "Đây là cái gì?"
            },
            {
                "question": "這是什麼東西？",
                "image": "tv.png",
                "options": ["桌子", "椅子", "電視", "掃把"],
                "correct": "電視",
                "translation": "Đây là cái gì?"
            },
            {
                "question": "這是什麼東西？",
                "image": "eraser.png",
                "options": ["手錶", "橡皮", "書包", "尺子"],
                "correct": "橡皮",
                "translation": "Đây là cái gì?"
            },
            {
                "question": "小美現在在哪裡？",
                "image": "kitchen.png",
                "options": ["廚房", "臥室", "客廳", "洗手間"],
                "correct": "廚房",
                "translation": "Tiểu Mỹ đang ở đâu?"
            },
            {
                "question": "小華覺得不舒服，他應該去哪？",
                "image": "hospital.png",
                "options": ["銀行", "醫院", "公園", "動物園"],
                "correct": "醫院",
                "translation": "Tiểu Hoa không khỏe, cậu ấy nên đi đâu?"
            },
            {
                "question": "是什麼水果？",
                "image": "apple.png",
                "options": ["香蕉", "橙子", "榴蓮", "蘋果"],
                "correct": "蘋果",
                "translation": "Đây là quả gì?"
            },
            {
                "question": "媽媽在做什麼？",
                "image": "phone.png",
                "options": ["打電話", "掃地", "洗衣服", "上課"],
                "correct": "打電話",
                "translation": "Mẹ đang làm gì?"
            },
            {
                "question": "他做什麼工作？",
                "image": "police.png",
                "options": ["警察", "護士", "醫生", "老師"],
                "correct": "警察",
                "translation": "Anh ấy làm nghề gì?"
            }
        ]

        self.show_welcome_screen()

    def load_sounds(self):
        try:
            self.sounds = {
                "correct": pygame.mixer.Sound(os.path.join("sounds", "correct.mp3")),
                "wrong": pygame.mixer.Sound(os.path.join("sounds", "wrong.mp3")),
                "win": pygame.mixer.Sound(os.path.join("sounds", "win.mp3"))
            }
            pygame.mixer.music.load(os.path.join("sounds", "background.mp3"))
            pygame.mixer.music.set_volume(0.3)
            for sound in self.sounds.values():
                sound.set_volume(0.5)
        except Exception as e:
            print(f"Cannot load sounds: {e}")

    def load_image(self, image_name, size=(450, 300)):
        try:
            image = Image.open(os.path.join("images", image_name))
            image = image.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Cannot load image {image_name}: {e}")
            return None

    def show_welcome_screen(self):
        self.clear_screen()

        main_frame = ttk.Frame(self.root, style='Game.TFrame')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)

        title = ttk.Label(
            main_frame,
            text="歡迎來到中文學習遊戲\nChào mừng đến với trò chơi học tiếng Trung",
            style='Title.TLabel',
            justify='center'
        )
        title.pack(pady=20)

        form_frame = ttk.Frame(main_frame, style='Game.TFrame')
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="👤 名字 / Tên:",
                  style='Game.TLabel').grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=30, font=('Arial', 12))
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="🎂 年齡 / Tuổi:",
                  style='Game.TLabel').grid(row=1, column=0, padx=5, pady=5)
        self.age_entry = ttk.Entry(form_frame, width=30, font=('Arial', 12))
        self.age_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(
            main_frame,
            text="開始遊戲 / Bắt đầu",
            command=self.start_game,
            style='Option.TButton'
        ).pack(pady=20)

        try:
            pygame.mixer.music.play(-1)
        except:
            pass

    def start_game(self):
        if not self.name_entry.get() or not self.age_entry.get():
            messagebox.showwarning(
                "警告 / Cảnh báo", "請輸入名字和年齡！\nVui lòng nhập tên và tuổi!")
            return
        random.shuffle(self.questions)
        self.show_question()

    def show_question(self):
        self.clear_screen()
        question = self.questions[self.current_question]

        main_frame = ttk.Frame(self.root, style='Game.TFrame')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)

        score_frame = ttk.Frame(main_frame, style='Game.TFrame')
        score_frame.pack(fill='x', padx=20)
        ttk.Label(
            score_frame,
            text=f"分數 / Điểm: {self.score}",
            style='Game.TLabel'
        ).pack(side='left')

        ttk.Label(
            main_frame,
            text=f"{question['question']}\n{question['translation']}",
            style='Title.TLabel',
            justify='center'
        ).pack(pady=20)

        image_frame = ttk.Frame(main_frame, style='Game.TFrame')
        image_frame.pack(pady=20)

        image_photo = self.load_image(question["image"])
        if image_photo:
            label = ttk.Label(image_frame, image=image_photo)
            label.image = image_photo
            label.pack()

        options_frame = ttk.Frame(main_frame, style='Game.TFrame')
        options_frame.pack(pady=30)

        for i, option in enumerate(question["options"]):
            row = i // 2
            col = i % 2
            ttk.Button(
                options_frame,
                text=option,
                command=lambda x=option: self.check_answer(x),
                style='Option.TButton',
                width=20
            ).grid(row=row, column=col, padx=10, pady=5)

    def check_answer(self, answer):
        correct = self.questions[self.current_question]["correct"]
        if answer == correct:
            self.score += 10
            try:
                self.sounds["correct"].play()
            except:
                pass
            if self.score >= 100:
                self.show_rewards()
            else:
                self.current_question += 1
                if self.current_question < len(self.questions):
                    self.show_question()
                else:
                    self.show_rewards()
        else:
            try:
                self.sounds["wrong"].play()
            except:
                pass
            self.show_game_over()

    def show_rewards(self):
        self.clear_screen()

        main_frame = ttk.Frame(self.root, style='Game.TFrame')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)

        ttk.Label(
            main_frame,
            text="🎉 恭喜！選擇你的獎勵\nChúc mừng! Hãy chọn phần thưởng của bạn",
            style='Title.TLabel',
            justify='center'
        ).pack(pady=20)

        rewards_frame = ttk.Frame(main_frame, style='Game.TFrame')
        rewards_frame.pack(fill='x', padx=50)

        rewards = [
            ("flower.png", "🌹 玫瑰花", "Hoa hồng"),
            ("teddy.png", "🧸 玩具熊", "Gấu bông"),
            ("watch.png", "⌚ 手錶", "Đồng hồ")
        ]

        for i, (img, chinese, vietnamese) in enumerate(rewards):
            reward_frame = ttk.Frame(rewards_frame, style='Game.TFrame')
            reward_frame.grid(row=0, column=i, padx=20, pady=20)

            image = Image.open(os.path.join("images/rewards", img))
            image = image.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            label = ttk.Label(reward_frame, image=photo)
            label.image = photo
            label.pack(padx=10, pady=5)

            ttk.Button(
                reward_frame,
                text=f"{chinese}\n{vietnamese}",
                command=lambda x=chinese, y=vietnamese, z=img: self.select_reward(
                    x, y, z),
                style='Option.TButton'
            ).pack(pady=5)

    def select_reward(self, chinese, vietnamese, image_name):
        self.clear_screen()

        main_frame = ttk.Frame(self.root, style='Game.TFrame')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)

        ttk.Label(
            main_frame,
            text=f"恭喜你獲得{chinese}！\nChúc mừng bạn nhận được {vietnamese}!",
            style='Title.TLabel',
            justify='center'
        ).pack(pady=20)

        image = Image.open(os.path.join("images/rewards", image_name))
        image = image.resize((300, 300), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label = ttk.Label(main_frame, image=photo)
        label.image = photo
        label.pack(pady=20)

        try:
            self.sounds["win"].play()
        except:
            pass

        ttk.Button(
            main_frame,
            text="結束 / Kết thúc",
            command=self.show_game_over,
            style='Option.TButton'
        ).pack(pady=20)

    def show_game_over(self):
        self.clear_screen()

        main_frame = ttk.Frame(self.root, style='Game.TFrame')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)

        ttk.Label(
            main_frame,
            text=f"遊戲結束 / Trò chơi kết thúc\n最終分數 / Điểm số cuối cùng: {self.score}",
            style='Title.TLabel',
            justify='center'
        ).pack(pady=20)

        ttk.Button(
            main_frame,
            text="🔄 再玩一次 / Chơi lại",
            command=self.restart_game,
            style='Option.TButton'
        ).pack(pady=20)

    def restart_game(self):
        self.score = 0
        self.current_question = 0
        random.shuffle(self.questions)
        self.show_welcome_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = ChineseGame()
    print(len(game.questions))
    game.run()
