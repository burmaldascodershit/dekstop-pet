import tkinter as tk
import random
import time
import math

# Desktop Pet — Windows 10/11, Python 3.10+
# No external packages required.

KEY_COLOR = "#ff00ff"

class DesktopPet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Desktop Pet")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=KEY_COLOR)
        try:
            self.root.wm_attributes("-transparentcolor", KEY_COLOR)
        except tk.TclError:
            pass

        self.width, self.height = 180, 175
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.x, self.y = max(20, sw - 230), max(60, sh - 260)
        self.vx, self.vy = random.choice([-2, 2]), 0
        self.dragging = False
        self.drag_offset = (0, 0)
        self.hunger = 20
        self.energy = 85
        self.happiness = 75
        self.mood = "happy"
        self.message = "Привет! Я твой питомец 🐾"
        self.message_until = time.time() + 4
        self.last_tick = time.time()
        self.last_cursor_check = 0
        self.last_reaction = 0
        self.last_needs_update = time.time()
        self.sleeping = False
        self.frame = 0

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height,
                                bg=KEY_COLOR, highlightthickness=0, bd=0)
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.canvas.bind("<Button-3>", self.popup)
        self.canvas.bind("<Double-Button-1>", self.pet)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<F1>", lambda e: self.help_message())

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="🍎 Покормить", command=self.feed)
        self.menu.add_command(label="❤️ Погладить", command=self.pet)
        self.menu.add_command(label="🎾 Поиграть", command=self.play)
        self.menu.add_command(label="💤 Сон / бодрствование", command=self.toggle_sleep)
        self.menu.add_separator()
        self.menu.add_command(label="📊 Состояние питомца", command=self.show_status)
        self.menu.add_command(label="❔ Как управлять", command=self.help_message)
        self.menu.add_separator()
        self.menu.add_command(label="✖ Закрыть питомца", command=self.root.destroy)

        self.place()
        self.draw()
        self.tick()
        self.root.mainloop()

    def place(self):
        self.root.geometry(f"{self.width}x{self.height}+{int(self.x)}+{int(self.y)}")

    def say(self, text, seconds=3):
        self.message = text
        self.message_until = time.time() + seconds

    def start_drag(self, event):
        self.dragging = True
        self.drag_offset = (event.x_root - self.x, event.y_root - self.y)
        self.vx = self.vy = 0
        self.say("Ух ты, летим! ✨", 1.5)

    def drag(self, event):
        if self.dragging:
            self.x = event.x_root - self.drag_offset[0]
            self.y = event.y_root - self.drag_offset[1]
            self.place()

    def stop_drag(self, event):
        if self.dragging:
            self.dragging = False
            self.vx = random.choice([-2.2, -1.5, 1.5, 2.2])
            self.vy = -1
            self.say("Приземляюсь!", 1.5)

    def popup(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def feed(self):
        self.hunger = max(0, self.hunger - 38)
        self.happiness = min(100, self.happiness + 8)
        self.energy = min(100, self.energy + 3)
        self.sleeping = False
        self.say(random.choice(["Ням-ням! 🍎", "Вкусно! Спасибо! 😋", "Есть ещё? 🍪"]), 3.5)

    def pet(self, event=None):
        self.happiness = min(100, self.happiness + 16)
        self.say(random.choice(["Мур-р-р ❤️", "Вот это приятно!", "Ещё погладь! 🥰"]), 3)

    def play(self):
        self.happiness = min(100, self.happiness + 22)
        self.energy = max(0, self.energy - 14)
        self.hunger = min(100, self.hunger + 7)
        self.sleeping = False
        self.vy = -5
        self.vx = random.choice([-3, 3])
        self.say(random.choice(["Лови мяч! 🎾", "Ура, играем!", "Прыг-скок!"]), 3)

    def toggle_sleep(self):
        self.sleeping = not self.sleeping
        if self.sleeping:
            self.say("Хр-р-р… 💤", 5)
        else:
            self.energy = min(100, self.energy + 10)
            self.say("Я проснулся! ☀️", 3)

    def show_status(self):
        status = (f"Настроение: {self.mood}\n"
                  f"Голод: {self.hunger}/100\n"
                  f"Энергия: {self.energy}/100\n"
                  f"Радость: {self.happiness}/100\n\n"
                  "ПКМ по питомцу — меню.")
        self.say(status, 6)

    def help_message(self):
        self.say("ЛКМ — тащить • двойной клик — погладить • ПКМ — меню", 6)

    def tick(self):
        now = time.time()
        dt = min(0.1, now - self.last_tick)
        self.last_tick = now
        self.frame += 1

        # Needs slowly change with time.
        if now - self.last_needs_update > 12:
            self.hunger = min(100, self.hunger + 1)
            self.energy = max(0, self.energy - (0 if self.sleeping else 1))
            if self.sleeping:
                self.energy = min(100, self.energy + 2)
            if self.hunger > 75:
                self.happiness = max(0, self.happiness - 2)
            self.last_needs_update = now

        if not self.dragging:
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            if not self.sleeping:
                # Little wandering and bouncing at screen edges.
                if random.random() < 0.018:
                    self.vx = random.choice([-1.8, -1.2, 1.2, 1.8])
                self.vy += 0.12
                self.x += self.vx
                self.y += self.vy
                floor = sh - self.height - 5
                if self.y > floor:
                    self.y = floor
                    self.vy *= -0.45
                    if abs(self.vy) < 0.8:
                        self.vy = 0
                if self.y < 25:
                    self.y = 25
                    self.vy = abs(self.vy) * 0.5
                if self.x < 0 or self.x > sw - self.width:
                    self.vx *= -1
                    self.x = min(max(0, self.x), sw - self.width)
                self.place()

        # React when the pointer approaches.
        if now - self.last_cursor_check > 0.35 and not self.dragging:
            self.last_cursor_check = now
            try:
                px, py = self.root.winfo_pointerxy()
                cx, cy = self.x + self.width/2, self.y + self.height/2
                dist = math.hypot(px-cx, py-cy)
                if dist < 115 and now - self.last_reaction > 3:
                    self.last_reaction = now
                    self.say(random.choice(["О, курсор! 👀", "Поиграем?", "Привет! 🐾"]), 2)
                    if not self.sleeping:
                        self.vx = 1.7 if px < cx else -1.7
            except tk.TclError:
                pass

        if self.hunger > 80:
            self.mood = "голодный"
        elif self.energy < 20:
            self.mood = "сонный"
        elif self.happiness < 25:
            self.mood = "скучающий"
        elif self.sleeping:
            self.mood = "спит"
        else:
            self.mood = "довольный"

        self.draw()
        self.root.after(60, self.tick)

    def draw(self):
        c = self.canvas
        c.delete("all")

        # Speech bubble.
        if time.time() < self.message_until:
            msg = self.message
            # Keep bubble compact and readable.
            if len(msg) > 42:
                msg = msg[:39] + "..."
            c.create_rounded_rectangle if False else None
            c.create_rectangle(8, 5, self.width-8, 38, fill="#fffdf4",
                               outline="#5c5268", width=2)
            c.create_text(self.width/2, 21, text=msg, fill="#292536",
                          font=("Segoe UI", 9, "bold"), width=self.width-24)

        bob = 0 if self.sleeping else int(math.sin(self.frame / 5) * 3)
        # Soft shadow.
        c.create_oval(39, 145, 141, 164, fill="#7d6f91", outline="")
        # Ears and body, a friendly round cat-like pet.
        c.create_polygon(48, 83+bob, 47, 52+bob, 72, 68+bob,
                         fill="#f5bd77", outline="#59445a", width=3)
        c.create_polygon(108, 68+bob, 133, 51+bob, 132, 84+bob,
                         fill="#f5bd77", outline="#59445a", width=3)
        c.create_oval(40, 61+bob, 140, 151+bob,
                      fill="#ffd49a", outline="#59445a", width=3)
        # Face.
        if self.sleeping:
            c.create_arc(61, 91+bob, 82, 107+bob, start=15, extent=150,
                         style=tk.ARC, outline="#392d43", width=3)
            c.create_arc(98, 91+bob, 119, 107+bob, start=15, extent=150,
                         style=tk.ARC, outline="#392d43", width=3)
            c.create_text(125, 55+bob, text="Zz", fill="#65517d",
                          font=("Segoe UI", 12, "bold"))
        else:
            c.create_oval(63, 88+bob, 79, 106+bob, fill="#392d43", outline="")
            c.create_oval(101, 88+bob, 117, 106+bob, fill="#392d43", outline="")
            c.create_oval(67, 90+bob, 72, 96+bob, fill="white", outline="")
            c.create_oval(105, 90+bob, 110, 96+bob, fill="white", outline="")
        c.create_polygon(86, 108+bob, 94, 108+bob, 90, 113+bob,
                         fill="#c76c79", outline="#59445a")
        c.create_arc(77, 109+bob, 91, 122+bob, start=205, extent=130,
                     style=tk.ARC, outline="#59445a", width=2)
        c.create_arc(90, 109+bob, 104, 122+bob, start=205, extent=130,
                     style=tk.ARC, outline="#59445a", width=2)
        # Whiskers.
        for yy in (105, 113):
            c.create_line(53, yy+bob, 73, yy+2+bob, fill="#59445a", width=1)
            c.create_line(107, yy+2+bob, 127, yy+bob, fill="#59445a", width=1)
        # Mood icon.
        icon = "💤" if self.sleeping else ("🍎" if self.hunger > 80 else
                                           ("💗" if self.happiness > 65 else "…"))
        c.create_text(90, 143+bob, text=icon, font=("Segoe UI Emoji", 12))
        # Small instruction hint.
        c.create_text(self.width/2, 169, text="ПКМ — меню", fill="#ffffff",
                      font=("Segoe UI", 8, "bold"), tags="hint")

if __name__ == "__main__":
    DesktopPet()
