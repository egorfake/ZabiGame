import tkinter as tk
from tkinter import Toplevel, Label, Menu
from PIL import Image, ImageTk
import random
import csv
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


IMAGE_PATH = resource_path("RusselZ.png")
PHRASES_CSV = resource_path("phrases.csv")
CHAR_W = 220
CHAR_H = 314

class DesktopCharacter:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#000000")
        self.root.attributes("-transparentcolor", "#000000")

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self.x = self.screen_w - CHAR_W - 20
        self.y = self.screen_h - CHAR_H - 60
        self.root.geometry(f"{CHAR_W}x{CHAR_H}+{self.x}+{self.y}")

        self.canvas = tk.Canvas(
            self.root,
            width=CHAR_W,
            height=CHAR_H,
            bd=0,
            highlightthickness=0,
            relief="flat",
            bg="#000000"
        )
        self.canvas.pack(fill="both", expand=True)

        self.original = Image.open(IMAGE_PATH).convert("RGBA").resize(
            (CHAR_W, CHAR_H), Image.Resampling.LANCZOS
        )
        self.photo = ImageTk.PhotoImage(self.original)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.canvas.image = self.photo

        self.phrases = self.load_phrases()
        self.dialog = None

        self.menu = Menu(self.root, tearoff=0)
        self.menu.add_command(label="Закрыть игру", command=self.close_app)

        self.canvas.bind("<Button-1>", self.on_character_click)
        self.canvas.bind("<Button-3>", self.show_menu)

        if self.phrases:
            self.show_dialog("Привет, я Забиден и я сейчас разрабатываю teewars legacy")

    def load_phrases(self):
        phrases = []
        try:
            with open(PHRASES_CSV, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    text = (row.get("text") or "").strip()
                    if text:
                        phrases.append(text)
        except FileNotFoundError:
            phrases = ["Файл phrases.csv не найден."]
        return phrases

    def on_character_click(self, event=None):
        if self.phrases:
            self.show_dialog(random.choice(self.phrases))

    def show_dialog(self, text):
        if self.dialog is not None and self.dialog.winfo_exists():
            self.dialog.destroy()

        self.dialog = Toplevel(self.root)
        self.dialog.overrideredirect(True)
        self.dialog.attributes("-topmost", True)
        self.dialog.configure(bg="#1e1e1e")

        outer = tk.Frame(self.dialog, bg="#000000", bd=0, highlightthickness=0)
        outer.pack(padx=0, pady=0)

        inner = tk.Frame(outer, bg="#f2f2f2", bd=0, highlightthickness=0)
        inner.pack(padx=4, pady=4)

        label = Label(
            inner,
            text=text,
            bg="#f2f2f2",
            fg="#1a1a1a",
            font=("Courier New", 12, "bold"),
            justify="left",
            padx=12,
            pady=10,
            wraplength=280,
            bd=0,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        label.pack()

        self.dialog.update_idletasks()
        dw = self.dialog.winfo_width()
        dh = self.dialog.winfo_height()
        dx = self.x - dw - 15
        dy = self.y + 20

        if dx < 10:
            dx = self.x
            dy = self.y - dh - 10

        self.dialog.geometry(f"{dw}x{dh}+{dx}+{dy}")
        self.dialog.after(10000, self.dialog.destroy)

    def show_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def close_app(self):
        self.root.destroy()

def main():
    root = tk.Tk()
    DesktopCharacter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
