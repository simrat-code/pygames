import tkinter as tk
import random
import os
from dotenv import load_dotenv

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
# print(f"script_path: {script_path}, dir: {script_dir}")

env_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path=env_path)

score_threshold = int(os.getenv('score_threshold', '5'))
operator_list = os.getenv('operator_list', "+,-,*").split(',')
var_a = int(os.getenv('var_a', '10'))
var_b = int(os.getenv('var_b', '10'))
# print(operator_list)

class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)  # Fullscreen
        self.root.configure(bg="lightblue")

        self.question_count = 0
        self.score = 0
        self.total_questions = 5
        self.retry_flag = 0

        self.score_label = tk.Label(root, text="Correct Answers: 0 / 5", font=("Arial", 32, "bold"), bg="lightblue", fg="darkblue")
        self.score_label.pack(pady=20)

        self.question_label = tk.Label(root, text="", font=("Arial", 48), bg="lightblue")
        self.question_label.pack(pady=100)

        self.answer_entry = tk.Entry(root, font=("Arial", 36), justify='center')
        self.answer_entry.pack()

        self.feedback_label = tk.Label(root, text="", font=("Arial", 32), bg="lightblue")
        self.feedback_label.pack(pady=20)

        self.submit_button = tk.Button(root, text="Submit", font=("Arial", 28), command=self.check_answer)
        self.submit_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", font=("Arial", 24), command=self.exit_app)
        self.exit_button.pack(pady=10)

        self.generate_question()

    def update_score_label(self):
        self.score_label.config(text=f"Correct Answers: {self.score} / {self.total_questions}")

    def generate_question(self):
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")

        self.num1 = random.randint(1, var_a)
        self.num2 = random.randint(1, var_b)
        self.operator = random.choice(operator_list)

        # Ensure subtraction doesn't go negative
        if self.operator == "-" and self.num1 < self.num2:
            self.num1, self.num2 = self.num2, self.num1

        if self.operator == "*" and (self.num1 > 10 or self.num2 > 10):
            self.num1 = self.num1 % 10 if self.num1 > 10 else self.num1
            self.num2 = self.num2 % 10 if self.num2 > 10 else self.num2

        self.correct_answer = eval(f"{self.num1} {self.operator} {self.num2}")
        self.question_label.config(text=f"{self.num1} {self.operator} {self.num2} = ?")

    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
            if user_answer == self.correct_answer:
                self.feedback_label.config(text="✅ Correct!", fg="green")
                if self.retry_flag == 0:
                    self.score += 1
                self.retry_flag = 0
                self.update_score_label()
            else:
                self.feedback_label.config(text=f"❌ Try again!", fg="red")
                self.retry_flag = 1
                return  # Let the user retry
        except ValueError:
            self.feedback_label.config(text="⚠️ Please enter a number!", fg="orange")
            return

        self.question_count += 1
        # if self.question_count < self.total_questions:
        if self.score < self.total_questions:
            self.root.after(1000, self.generate_question)
        else:
            self.show_final_score()

    def show_final_score(self):
        percent = int((self.score / self.question_count) * 100)
        self.question_label.config(text=f"🎉 You got {self.score}/{self.question_count} right ({percent}%) ")
        self.answer_entry.pack_forget()
        self.submit_button.pack_forget()
        self.feedback_label.pack_forget()

    def exit_app(self):
        if self.score < score_threshold:
            remaining = self.total_questions - self.score
            self.feedback_label.config(
                text=f"🔒 You need {remaining} more correct answer(s) to exit.", fg="blue"
            )
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()
