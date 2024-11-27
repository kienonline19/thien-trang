import tkinter as tk
from tkinter import messagebox
import pygame
import os
from PIL import Image, ImageTk
import random
import json
import time


class ChineseGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("中文学习游戏")
        self.root.geometry("1024x768")
        self.root.configure(bg='#E8F4FF')

        self.score = 0
        self.current_question = 0
        self.wrong_attempts = 0

        # Define rewards as class attribute
        self.rewards = [
            ("flower.png", "🌹 玫瑰花"),
            ("teddy.png", "🧸 玩具熊"),
            ("watch.png", "⌚ 手表")
        ]

        pygame.mixer.init()
        self.load_sounds()
        self.load_questions()

    def load_questions(self):
        try:
            with open('questions.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.questions = data['questions']
        except Exception as e:
            print(f"Error loading questions: {e}")

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
            print(f"Error loading sounds: {e}")

    def load_image(self, image_name, size=(450, 300)):
        try:
            image = Image.open(os.path.join("images", image_name))
            image = image.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image {image_name}: {e}")
            return None

    def show_welcome_screen(self):
        self.clear_screen()

        main_frame = tk.Frame(self.root, bg='#E8F4FF')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        title = tk.Label(
            main_frame,
            text="欢迎来到中文学习游戏",
            font=('Arial', 32, 'bold'),
            fg='#2E4053',
            bg='#E8F4FF',
            pady=20
        )
        title.pack(pady=30)

        form_frame = tk.Frame(main_frame, bg='#E8F4FF', padx=30)
        form_frame.pack(pady=20)

        entry_style = {
            'width': 25,
            'font': ('Arial', 14),
            'bg': 'white',
            'fg': '#2E4053',
            'relief': 'flat',
            'bd': 0,
        }

        # Name input
        name_frame = tk.Frame(form_frame, bg='#E8F4FF', pady=10)
        name_frame.pack(fill='x')

        name_label = tk.Label(
            name_frame,
            text="👤 名字",
            font=('Arial', 16, 'bold'),
            bg='#E8F4FF',
            fg='#2E4053'
        )
        name_label.pack(anchor='w', pady=(0, 5))

        name_entry_frame = tk.Frame(
            name_frame,
            bg='white',
            highlightthickness=1,
            highlightbackground='#BDC3C7',
            highlightcolor='#3498DB'
        )
        name_entry_frame.pack(fill='x')
        self.name_entry = tk.Entry(name_entry_frame, **entry_style)
        self.name_entry.pack(pady=8, padx=10, fill='x')

        # Age input
        age_frame = tk.Frame(form_frame, bg='#E8F4FF', pady=10)
        age_frame.pack(fill='x')

        age_label = tk.Label(
            age_frame,
            text="🎂 年龄",
            font=('Arial', 16, 'bold'),
            bg='#E8F4FF',
            fg='#2E4053'
        )
        age_label.pack(anchor='w', pady=(0, 5))

        age_entry_frame = tk.Frame(
            age_frame,
            bg='white',
            highlightthickness=1,
            highlightbackground='#BDC3C7',
            highlightcolor='#3498DB'
        )
        age_entry_frame.pack(fill='x')
        self.age_entry = tk.Entry(age_entry_frame, **entry_style)
        self.age_entry.pack(pady=8, padx=10, fill='x')

        # Start button
        button_frame = tk.Frame(main_frame, bg='#E8F4FF')
        button_frame.pack(pady=30)

        start_button = tk.Button(
            button_frame,
            text="开始游戏",
            command=self.start_game,
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#3498DB',
            activebackground='#2980B9',
            width=15,
            height=2,
            relief='flat',
            cursor='hand2'
        )
        start_button.pack()

        def on_enter(e):
            start_button['background'] = '#2980B9'

        def on_leave(e):
            start_button['background'] = '#3498DB'

        start_button.bind('<Enter>', on_enter)
        start_button.bind('<Leave>', on_leave)

        def on_entry_focus_in(event, frame):
            frame.configure(highlightbackground='#3498DB')

        def on_entry_focus_out(event, frame):
            frame.configure(highlightbackground='#BDC3C7')

        self.name_entry.bind(
            '<FocusIn>', lambda e: on_entry_focus_in(e, name_entry_frame))
        self.name_entry.bind(
            '<FocusOut>', lambda e: on_entry_focus_out(e, name_entry_frame))
        self.age_entry.bind(
            '<FocusIn>', lambda e: on_entry_focus_in(e, age_entry_frame))
        self.age_entry.bind(
            '<FocusOut>', lambda e: on_entry_focus_out(e, age_entry_frame))

        try:
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Error playing music: {e}")

    def start_game(self):
        if not self.name_entry.get() or not self.age_entry.get():
            messagebox.showwarning("警告", "请输入名字和年龄！")
            return
        self.wrong_attempts = 0
        random.shuffle(self.questions)
        self.show_question()

    def show_question(self):
        self.clear_screen()
        question = self.questions[self.current_question]

        main_frame = tk.Frame(self.root, bg='#E8F4FF')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)

        score_frame = tk.Frame(main_frame, bg='#E8F4FF')
        score_frame.pack(fill='x')

        tk.Label(
            score_frame,
            text=f"分数: {self.score}",
            font=('Arial', 16, 'bold'),
            fg='#2E4053',
            bg='#E8F4FF'
        ).pack(side='left')

        tk.Label(
            score_frame,
            text=f"剩余机会: {3 - self.wrong_attempts}",
            font=('Arial', 16, 'bold'),
            fg='#2E4053',
            bg='#E8F4FF'
        ).pack(side='right')

        tk.Label(
            main_frame,
            text=question['question'],
            font=('Arial', 24, 'bold'),
            fg='#2E4053',
            bg='#E8F4FF'
        ).pack(pady=20)

        image_photo = self.load_image(question["image"])
        if image_photo:
            image_label = tk.Label(main_frame, image=image_photo, bg='#E8F4FF')
            image_label.image = image_photo
            image_label.pack(pady=20)

        options_frame = tk.Frame(main_frame, bg='#E8F4FF')
        options_frame.pack(pady=20)

        button_style = {
            'font': ('Arial', 16),
            'width': 20,
            'height': 2,
            'fg': 'white',
            'bg': '#3498DB',
            'activebackground': '#2980B9',
            'relief': 'flat',
            'cursor': 'hand2'
        }

        for i, option in enumerate(question["options"]):
            row = i // 2
            col = i % 2
            button = tk.Button(
                options_frame,
                text=option,
                command=lambda x=option: self.check_answer(x),
                **button_style
            )
            button.grid(row=row, column=col, padx=10, pady=5)

            button.bind('<Enter>', lambda e,
                        btn=button: btn.configure(bg='#2980B9'))
            button.bind('<Leave>', lambda e,
                        btn=button: btn.configure(bg='#3498DB'))

    def check_answer(self, answer):
        correct = self.questions[self.current_question]["correct"]
        if answer == correct:
            self.score += 10
            try:
                self.sounds["correct"].play()
            except:
                pass
            messagebox.showinfo(
                "", self.questions[self.current_question]["encouragement"])
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
            self.wrong_attempts += 1
            if self.wrong_attempts >= 3:
                self.show_game_over()
            else:
                messagebox.showwarning("", f"答错了！还有{3-self.wrong_attempts}次机会")

    def show_rewards(self):
        self.clear_screen()

        main_frame = tk.Frame(self.root, bg='#E8F4FF')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)

        tk.Label(
            main_frame,
            text="🎉 恭喜！选择你的奖励",
            font=('Arial', 24, 'bold'),
            fg='#2E4053',
            bg='#E8F4FF'
        ).pack(pady=20)

        # Random reward button
        random_button = tk.Button(
            main_frame,
            text="🎲 随机选择",
            command=self.random_reward,
            font=('Arial', 16),
            width=20,
            fg='white',
            bg='#E74C3C',
            activebackground='#C0392B',
            relief='flat',
            cursor='hand2'
        )
        random_button.pack(pady=10)

        # Add hover effect for random button
        random_button.bind(
            '<Enter>', lambda e: random_button.configure(bg='#C0392B'))
        random_button.bind(
            '<Leave>', lambda e: random_button.configure(bg='#E74C3C'))

        rewards_frame = tk.Frame(main_frame, bg='#E8F4FF')
        rewards_frame.pack(pady=20)

        button_style = {
            'font': ('Arial', 14),
            'width': 20,
            'fg': 'white',
            'bg': '#3498DB',
            'activebackground': '#2980B9',
            'relief': 'flat',
            'cursor': 'hand2'
        }

        for i, (img, chinese) in enumerate(self.rewards):
            reward_frame = tk.Frame(rewards_frame, bg='#E8F4FF')
            reward_frame.grid(row=0, column=i, padx=20)

            image = Image.open(os.path.join("images/rewards", img))
            image = image.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            label = tk.Label(reward_frame, image=photo, bg='#E8F4FF')
            label.image = photo
            label.pack(padx=10, pady=5)

            button = tk.Button(
                reward_frame,
                text=chinese,
                command=lambda x=chinese, z=img: self.select_reward(x, z),
                **button_style
            )
            button.pack(pady=5)

            button.bind('<Enter>', lambda e,
                        btn=button: btn.configure(bg='#2980B9'))
            button.bind('<Leave>', lambda e,
                        btn=button: btn.configure(bg='#3498DB'))

    def random_reward(self):
        # Show loading animation
        temp_frame = tk.Frame(self.root, bg='#E8F4FF')
        temp_frame.place(relx=0.5, rely=0.5, anchor='center')

        loading_label = tk.Label(
            temp_frame,
            text="🎲 正在选择...",
            font=('Arial', 24, 'bold'),
            fg='#2E4053',
            bg='#E8F4FF'
        )
        loading_label.pack()

        # Update GUI
        self.root.update()

        # Wait for animation
        time.sleep(1)

        # Choose random reward
        img, chinese = random.choice(self.rewards)

        # Remove loading animation
        temp_frame.destroy()

        # Show selected reward
        self.select_reward(chinese, img)

    def select_reward(self, chinese, image_name):
        self.clear_screen()

        main_frame = tk.Frame(self.root, bg='#E8F4FF')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)

        tk.Label(
            main_frame,
            text=f"恭喜你获得{chinese}！",
            font=('Arial', 24, 'bold'),
            fg='#2E4053',
            bg='#E8F4FF'
        ).pack(pady=20)

        image = Image.open(os.path.join("images/rewards", image_name))
        image = image.resize((300, 300), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(main_frame, image=photo, bg='#E8F4FF')
        label.image = photo
        label.pack(pady=20)

        try:
            self.sounds["win"].play()
        except:
            pass

        button = tk.Button(
            main_frame,
            text="结束游戏",
            command=self.show_game_over,
            font=('Arial', 16),
            width=20,
            fg='white',
            bg='#3498DB',
            activebackground='#2980B9',
            relief='flat',
            cursor='hand2'
        )
        button.pack(pady=20)

        button.bind('<Enter>', lambda e: button.configure(bg='#2980B9'))
        button.bind('<Leave>', lambda e: button.configure(bg='#3498DB'))

    def show_game_over(self):
        self.clear_screen()

        main_frame = tk.Frame(self.root, bg='#E8F4FF')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)

        tk.Label(
            main_frame,
            text=f"游戏结束\n最终分数: {self.score}",
            font=('Arial', 24, 'bold'),
            fg='#2E4053',
            bg='#E8F4FF',
            justify='center'
        ).pack(pady=20)

        button = tk.Button(
            main_frame,
            text="🔄 再玩一次",
            command=self.restart_game,
            font=('Arial', 16),
            width=20,
            fg='white',
            bg='#3498DB',
            activebackground='#2980B9',
            relief='flat',
            cursor='hand2'
        )
        button.pack(pady=20)

        button.bind('<Enter>', lambda e: button.configure(bg='#2980B9'))
        button.bind('<Leave>', lambda e: button.configure(bg='#3498DB'))

    def restart_game(self):
        self.score = 0
        self.current_question = 0
        self.wrong_attempts = 0
        random.shuffle(self.questions)
        self.show_welcome_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.show_welcome_screen()
        self.root.mainloop()


if __name__ == "__main__":
    try:
        game = ChineseGame()
        game.run()
    except Exception as e:
        print(f"Critical error: {e}")
