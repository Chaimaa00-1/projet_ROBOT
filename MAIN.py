import tkinter as tk
import json
import os


class NumericKeypad(tk.Toplevel):
    def __init__(self, parent, target_entry, min_value=0, max_value=90, on_ok=None, on_close=None):
        super().__init__(parent)
        self.title("Clavier numérique")
        self.resizable(False, False)
        self.configure(bg="#f7f9fc")
        self.transient(parent)

        self.target_entry = target_entry
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = ""
        self.on_ok = on_ok
        self.on_close = on_close

        self.position_window(parent, target_entry)
        self.build_ui()

        self.protocol("WM_DELETE_WINDOW", self.handle_close)
        self.grab_set()

    def position_window(self, parent, target_entry):
        width = 460
        height = 540
        margin = 20
        bottom_safety = 70

        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        entry_x = target_entry.winfo_rootx()
        entry_y = target_entry.winfo_rooty()
        entry_width = target_entry.winfo_width()

        space_right = screen_width - (entry_x + entry_width)
        space_left = entry_x

        if space_right >= width + margin:
            pos_x = entry_x + entry_width + margin
        elif space_left >= width + margin:
            pos_x = entry_x - width - margin
        elif space_right >= space_left:
            pos_x = screen_width - width - margin
        else:
            pos_x = margin

        pos_x = max(0, min(pos_x, screen_width - width))

        pos_y = entry_y
        max_y = screen_height - height - bottom_safety
        if pos_y > max_y:
            pos_y = max(max_y, 0)

        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def build_ui(self):
        title = tk.Label(
            self,
            text="Saisir l'angle",
            font=("Segoe UI", 16, "bold"),
            bg="#f7f9fc",
            fg="#1f2937"
        )
        title.pack(pady=(12, 8))

        self.display = tk.Entry(
            self,
            font=("Consolas", 26, "bold"),
            justify="center",
            bd=2,
            relief="solid",
            bg="white",
            fg="#c2185b"
        )
        self.display.pack(fill="x", padx=20, pady=(0, 12), ipady=10)

        keypad_frame = tk.Frame(self, bg="#f7f9fc")
        keypad_frame.pack(padx=16, pady=6, fill="both", expand=True)

        buttons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2),
            ("C", 3, 0), ("0", 3, 1), ("OK", 3, 2),
        ]

        for text, row, col in buttons:
            bg = "#e91e63"
            fg = "white"

            if text == "C":
                bg = "#ef5350"
            elif text == "OK":
                bg = "#43a047"

            btn = tk.Button(
                keypad_frame,
                text=text,
                font=("Segoe UI", 18, "bold"),
                bg=bg,
                fg=fg,
                activebackground=bg,
                activeforeground=fg,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, padx=6, pady=6, sticky="nsew", ipady=10)

        for i in range(3):
            keypad_frame.grid_columnconfigure(i, weight=1)
        for i in range(4):
            keypad_frame.grid_rowconfigure(i, weight=1)

    def on_button_click(self, value):
        if value == "C":
            self.current_value = ""
            self.refresh_display()
        elif value == "OK":
            self.validate_and_apply()
        else:
            self.current_value += value
            self.refresh_display()

    def refresh_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_value)

    def validate_and_apply(self):
        try:
            if self.current_value.strip() == "":
                return

            number = float(self.current_value)

            if number < self.min_value:
                number = self.min_value
            if number > self.max_value:
                number = self.max_value

            self.target_entry.delete(0, tk.END)
            if int(number) == number:
                self.target_entry.insert(0, str(int(number)))
            else:
                self.target_entry.insert(0, str(number))

            callback = self.on_ok
            self.on_ok = None
            self.on_close = None
            self.destroy()

            if callback:
                callback()

        except ValueError:
            self.current_value = ""
            self.refresh_display()

    def handle_close(self):
        callback = self.on_close
        self.on_ok = None
        self.on_close = None
        self.destroy()

        if callback:
            callback()


class TextKeypad(tk.Toplevel):
    def __init__(self, parent, title_text="Saisir un nom"):
        super().__init__(parent)
        self.title(title_text)
        self.resizable(False, False)
        self.configure(bg="#f7f9fc")
        self.transient(parent)

        self.value = None
        self.current_text = ""

        self.position_window(parent)
        self.build_ui(title_text)

        self.grab_set()

    def position_window(self, parent):
        width = 680
        height = 700
        bottom_safety = 70

        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        pos_x = max((screen_width - width) // 2, 0)
        pos_y = 100

        max_y = screen_height - height - bottom_safety
        if pos_y > max_y:
            pos_y = max(max_y, 0)

        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def build_ui(self, title_text):
        title = tk.Label(
            self,
            text=title_text,
            font=("Segoe UI", 18, "bold"),
            bg="#f7f9fc",
            fg="#1f2937"
        )
        title.pack(pady=(16, 10))

        self.display = tk.Entry(
            self,
            font=("Consolas", 22, "bold"),
            justify="center",
            bd=2,
            relief="solid",
            bg="white",
            fg="#6d1533"
        )
        self.display.pack(fill="x", padx=24, pady=(0, 16), ipady=12)

        keypad_frame = tk.Frame(self, bg="#f7f9fc")
        keypad_frame.pack(padx=20, pady=8, fill="both", expand=True)

        buttons = [
            ("A", 0, 0), ("B", 0, 1), ("C1", 0, 2), ("D", 0, 3), ("E", 0, 4),
            ("F", 1, 0), ("G", 1, 1), ("H", 1, 2), ("I", 1, 3), ("J", 1, 4),
            ("K", 2, 0), ("L", 2, 1), ("M", 2, 2), ("N", 2, 3), ("O", 2, 4),
            ("P", 3, 0), ("Q", 3, 1), ("R", 3, 2), ("S", 3, 3), ("T", 3, 4),
            ("U", 4, 0), ("V", 4, 1), ("W", 4, 2), ("X", 4, 3), ("Y", 4, 4),
            ("Z", 5, 0), ("0", 5, 1), ("1", 5, 2), ("2", 5, 3), ("3", 5, 4),
            ("4", 6, 0), ("5", 6, 1), ("6", 6, 2), ("7", 6, 3), ("8", 6, 4),
            ("9", 7, 0), ("_", 7, 1), ("CLR", 7, 2), ("OK", 7, 3)
        ]

        for text, row, col in buttons:
            display_text = text
            bg = "#e91e63"
            fg = "white"

            if text == "CLR":
                bg = "#ef5350"
            elif text == "OK":
                bg = "#43a047"
            elif text == "C1":
                display_text = "C"

            btn = tk.Button(
                keypad_frame,
                text=display_text,
                font=("Segoe UI", 15, "bold"),
                bg=bg,
                fg=fg,
                activebackground=bg,
                activeforeground=fg,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew", ipady=8)

        for i in range(5):
            keypad_frame.grid_columnconfigure(i, weight=1)
        for i in range(8):
            keypad_frame.grid_rowconfigure(i, weight=1)

    def on_button_click(self, value):
        if value == "CLR":
            self.current_text = ""
            self.refresh_display()
        elif value == "OK":
            self.value = self.current_text.strip()
            self.destroy()
        else:
            if value == "C1":
                value = "C"
            self.current_text += value
            self.refresh_display()

    def refresh_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_text)

    def get_value(self):
        self.wait_window()
        return self.value


class RobotControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Control Panel - eRobot 3Kg")
        self.root.geometry("1000x650")
        self.root.minsize(800, 480)
        try:
            self.root.state("zoomed")
        except tk.TclError:
            try:
                self.root.attributes("-zoomed", True)
            except tk.TclError:
                pass
        self.root.overrideredirect(True)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.configure(bg="#f4f6f8")

        self.axis_names = {
            1: "J1 Base",
            2: "J2 Shoulder",
            3: "J3 Elbow",
            4: "J4 Wrist 1",
            5: "J5 Wrist 2",
            6: "J6 Tool"
        }

        self.axis_vars = {}
        self.angle_entries = {}
        self.saved_positions = {}
        self.saved_links = {}
        self.link_delay_ms = 2000
        self.save_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "robot_saves.json"
        )

        self.colors = {
            "bg_main": "#f4f6f8",
            "header": "#7b1e3a",
            "header_text": "#ffffff",
            "card_bg": "#ffffff",
            "section_title": "#6d1533",
            "table_header": "#f7d6e2",
            "table_row": "#fffafb",
            "row_gray": "#c9ced4",
            "row_selected": "#f48fb1",
            "row_saved": "#66bb6a",
            "row_editing": "#29b6f6",
            "button_primary": "#c2185b",
            "button_secondary": "#ec407a",
            "button_dark": "#8e244d",
            "button_green": "#2e7d32",
            "button_orange": "#ef6c00",
            "button_red": "#c62828",
            "button_gray": "#5f6b7a",
            "text_dark": "#2d2d2d",
            "text_muted": "#6b7280",
            "entry_bg": "#ffffff",
            "log_bg": "#1f1f1f",
            "log_fg": "#f8d7e3",
            "check_bg": "#ffe4ee"
        }

        self.app_password = "1234"

        self.build_login_screen()

    def build_login_screen(self):
        self.login_frame = tk.Frame(self.root, bg=self.colors["header"])
        self.login_frame.pack(fill="both", expand=True)

        card = tk.Frame(self.login_frame, bg=self.colors["card_bg"], bd=1, relief="solid")
        card.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(
            card,
            text="Connexion",
            font=("Segoe UI", 20, "bold"),
            fg=self.colors["section_title"],
            bg=self.colors["card_bg"]
        )
        title.pack(padx=50, pady=(30, 10))

        subtitle = tk.Label(
            card,
            text="Entrez le mot de passe pour accéder au panneau",
            font=("Segoe UI", 10),
            fg=self.colors["text_muted"],
            bg=self.colors["card_bg"]
        )
        subtitle.pack(padx=50, pady=(0, 16))

        self.password_entry = tk.Entry(
            card,
            font=("Segoe UI", 16),
            justify="center",
            show="•",
            relief="solid",
            bd=2,
            bg=self.colors["entry_bg"]
        )
        self.password_entry.pack(padx=50, pady=(0, 10), ipady=8, fill="x")
        self.password_entry.focus_set()
        self.password_entry.bind("<Return>", lambda e: self.check_password())

        self.login_error_label = tk.Label(
            card,
            text="",
            font=("Segoe UI", 9, "bold"),
            fg=self.colors["button_red"],
            bg=self.colors["card_bg"]
        )
        self.login_error_label.pack(padx=50, pady=(0, 6))

        login_btn = tk.Button(
            card,
            text="Se connecter",
            command=self.check_password,
            bg=self.colors["button_primary"],
            fg="white",
            activebackground=self.colors["button_primary"],
            activeforeground="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=8
        )
        login_btn.pack(padx=50, pady=(0, 30), fill="x")

    def check_password(self):
        entered_password = self.password_entry.get()

        if entered_password == self.app_password:
            self.login_frame.destroy()
            self.build_ui()
        else:
            self.login_error_label.configure(text="Mot de passe incorrect.")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus_set()

    def build_ui(self):
        self.build_top_bar()
        self.build_body()

    def build_top_bar(self):
        top_bar = tk.Frame(self.root, bg=self.colors["header"], height=90)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        left_buttons = [
            ("Save Position", "#3949ab", self.save_current_position),
            ("Load Position", self.colors["button_primary"], self.load_saved_position),
            ("Create Link", self.colors["button_secondary"], self.create_link),
            ("Run Link", self.colors["button_gray"], self.run_link),
            ("Sauvegarder", self.colors["button_orange"], self.persist_save),
            ("Récupérer", self.colors["button_orange"], self.persist_load),
        ]

        right_buttons = [
            ("Start", self.colors["button_green"], self.move_all_selected),
            ("Stop", self.colors["button_red"], self.stop_all_and_reset),
        ]

        def make_top_bar_button(text, color, cmd):
            return tk.Button(
                top_bar,
                text=text,
                command=cmd,
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                font=("Segoe UI", 14, "bold"),
                relief="flat",
                bd=0,
                padx=16,
                pady=16,
                cursor="hand2"
            )

        for text, color, cmd in left_buttons:
            make_top_bar_button(text, color, cmd).pack(side="left", padx=8, pady=16)

        for text, color, cmd in reversed(right_buttons):
            make_top_bar_button(text, color, cmd).pack(side="right", padx=8, pady=16)

    def build_body(self):
        body = tk.Frame(self.root, bg=self.colors["bg_main"])
        body.pack(fill="both", expand=True)

        self.build_axes_controls(body)

    def build_card_title(self, parent, text):
        label = tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            fg=self.colors["section_title"],
            bg=self.colors["card_bg"]
        )
        label.pack(anchor="w", padx=10, pady=(10, 6))

    def build_axes_controls(self, parent):
        frame = tk.Frame(parent, bg=self.colors["card_bg"], bd=1, relief="solid")
        frame.pack(fill="both", expand=True)

        table_container = tk.Frame(frame, bg=self.colors["card_bg"])
        table_container.pack(fill="both", expand=True, padx=8, pady=8)

        headers = ["Select", "Axis", "Jog -", "Jog +", "Angle"]

        for col, header in enumerate(headers):
            tk.Label(
                table_container,
                text=header,
                font=("Segoe UI", 18, "bold"),
                bg=self.colors["table_header"],
                fg=self.colors["text_dark"],
                padx=6,
                pady=18,
                relief="groove",
                bd=1
            ).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

        for motor_id in range(1, 7):
            selected_var = tk.BooleanVar(value=False)

            self.axis_vars[motor_id] = {
                "selected": selected_var
            }

            row_bg = self.colors["row_gray"]

            select_cell = tk.Frame(table_container, bg=row_bg, relief="groove", bd=1)
            select_cell.grid(row=motor_id, column=0, sticky="nsew", padx=1, pady=1)

            select_cb = tk.Checkbutton(
                select_cell,
                variable=selected_var,
                onvalue=True,
                offvalue=False,
                font=("Segoe UI", 16, "bold"),
                indicatoron=False,
                width=3,
                bg=row_bg,
                fg=self.colors["section_title"],
                activebackground=self.colors["check_bg"],
                selectcolor=self.colors["check_bg"],
                relief="raised",
                bd=2,
                highlightthickness=0,
                cursor="hand2",
                command=lambda m=motor_id: self.refresh_select_button(m)
            )
            select_cb.pack(expand=True, ipadx=6, ipady=10, padx=8, pady=8)
            self.axis_vars[motor_id]["select_button"] = select_cb
            self.axis_vars[motor_id]["select_cell"] = select_cell

            axis_label = tk.Label(
                table_container,
                text=self.axis_names[motor_id],
                font=("Segoe UI", 16, "bold"),
                bg=row_bg,
                fg=self.colors["text_dark"],
                padx=10,
                pady=14,
                relief="groove",
                bd=1
            )
            axis_label.grid(row=motor_id, column=1, sticky="nsew", padx=1, pady=1)
            self.axis_vars[motor_id]["axis_label"] = axis_label

            jog_left_btn = self.make_button(
                table_container, "◀️", self.colors["row_gray"],
                lambda m=motor_id: self.jog_step(m, -1),
                motor_id, 2
            )

            jog_right_btn = self.make_button(
                table_container, "▶️", self.colors["row_gray"],
                lambda m=motor_id: self.jog_step(m, 1),
                motor_id, 3
            )
            self.axis_vars[motor_id]["jog_left_btn"] = jog_left_btn
            self.axis_vars[motor_id]["jog_right_btn"] = jog_right_btn

            angle_entry = tk.Entry(
                table_container,
                width=6,
                font=("Consolas", 20, "bold"),
                justify="center",
                bg=self.colors["row_gray"],
                disabledbackground=self.colors["row_gray"],
                fg=self.colors["text_dark"],
                disabledforeground=self.colors["text_dark"],
                insertbackground=self.colors["text_dark"],
                relief="groove",
                bd=1,
                highlightthickness=0,
                state="disabled",
                cursor="arrow"
            )
            angle_entry.configure(state="normal")
            angle_entry.insert(0, "0")
            angle_entry.configure(state="disabled")
            angle_entry.grid(row=motor_id, column=4, padx=1, pady=1, ipady=14, sticky="nsew")
            angle_entry.bind("<FocusOut>", lambda e, m=motor_id: self.clamp_angle(m))
            angle_entry.bind("<KeyRelease>", lambda e, m=motor_id: self.clamp_angle_live(m))
            angle_entry.bind("<Button-1>", lambda e, m=motor_id: self.open_keypad(m))
            self.angle_entries[motor_id] = angle_entry

        for col in range(len(headers)):
            table_container.grid_columnconfigure(col, weight=1)

        table_container.grid_columnconfigure(0, weight=2)
        table_container.grid_columnconfigure(1, weight=2)

        for row in range(7):
            table_container.grid_rowconfigure(row, weight=1)

    def make_button(self, parent, text, color, command, row, col):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            font=("Segoe UI", 20, "bold"),
            width=4,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=6,
            pady=14
        )
        btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        return btn

    def clamp_angle_value(self, value):
        try:
            number = float(value)
        except ValueError:
            return 0

        if number < 0:
            return 0
        if number > 90:
            return 90
        return number

    def format_angle(self, value):
        if int(value) == value:
            return str(int(value))
        return str(value)

    def set_angle_entry_text(self, motor_id, text):
        entry = self.angle_entries[motor_id]
        previous_state = entry.cget("state")
        entry.configure(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, text)
        entry.configure(state=previous_state)

    def clamp_angle(self, motor_id):
        entry = self.angle_entries[motor_id]
        value = entry.get().strip()
        clamped = self.clamp_angle_value(value)
        self.set_angle_entry_text(motor_id, self.format_angle(clamped))

    def clamp_angle_live(self, motor_id):
        entry = self.angle_entries[motor_id]
        value = entry.get().strip()

        if value in ["", "-", ".", "-."]:
            return

        try:
            numeric_value = float(value)
        except ValueError:
            self.set_angle_entry_text(motor_id, "0")
            return

        clamped = self.clamp_angle_value(numeric_value)
        if numeric_value != clamped:
            self.set_angle_entry_text(motor_id, self.format_angle(clamped))

    def open_keypad(self, motor_id):
        if not self.axis_vars[motor_id]["selected"].get():
            self.log("Sélectionne d'abord l'axe pour modifier l'angle.")
            return

        self.highlight_editing_row(motor_id, True)

        def finish_edit():
            self.highlight_editing_row(motor_id, False)

        NumericKeypad(
            self.root,
            self.angle_entries[motor_id],
            min_value=0,
            max_value=90,
            on_ok=finish_edit,
            on_close=finish_edit
        )
    def highlight_editing_row(self, motor_id, is_editing):
        select_cell = self.axis_vars[motor_id]["select_cell"]
        axis_label = self.axis_vars[motor_id]["axis_label"]
        button = self.axis_vars[motor_id]["select_button"]
        angle_entry = self.angle_entries[motor_id]

        if is_editing:
            edit_color = self.colors["row_editing"]
            select_cell.configure(bg=edit_color)
            axis_label.configure(bg=edit_color)
            button.configure(bg=edit_color, activebackground=edit_color)
            angle_entry.configure(state="normal", bg=edit_color)
        else:
            self.refresh_select_button(motor_id)

    def jog_step(self, motor_id, step):
        entry = self.angle_entries[motor_id]

        try:
            current_value = float(entry.get().strip())
        except ValueError:
            current_value = 0

        new_value = self.clamp_angle_value(current_value + step)

        self.set_angle_entry_text(motor_id, self.format_angle(new_value))

        self.send_command({
            "command": "moveMotor",
            "motorID": motor_id,
            "angle": new_value
        })

    def refresh_select_button(self, motor_id):
        button = self.axis_vars[motor_id]["select_button"]
        select_cell = self.axis_vars[motor_id]["select_cell"]
        axis_label = self.axis_vars[motor_id]["axis_label"]
        jog_left_btn = self.axis_vars[motor_id]["jog_left_btn"]
        jog_right_btn = self.axis_vars[motor_id]["jog_right_btn"]
        angle_entry = self.angle_entries[motor_id]
        is_selected = self.axis_vars[motor_id]["selected"].get()

        button.configure(text="✓" if is_selected else "")

        row_color = self.colors["row_selected"] if is_selected else self.colors["row_gray"]
        select_cell.configure(bg=row_color)
        button.configure(bg=row_color, activebackground=row_color)
        axis_label.configure(bg=row_color)

        jog_color = self.colors["button_orange"] if is_selected else self.colors["row_gray"]
        jog_left_btn.configure(bg=jog_color, activebackground=jog_color)
        jog_right_btn.configure(bg=jog_color, activebackground=jog_color)

        if is_selected:
            angle_entry.configure(state="normal", bg=row_color)
        else:
            angle_entry.configure(
                state="disabled",
                disabledbackground=row_color,
                disabledforeground=self.colors["text_dark"]
            )

    def reset_table_selection(self):
        for motor_id in range(1, 7):
            self.axis_vars[motor_id]["selected"].set(False)
            self.refresh_select_button(motor_id)

    def stop_all_and_reset(self):
        self.send_command({"command": "stopAllMotors"})
        self.reset_table_selection()
        self.reset_all_angles_to_zero()

    def reset_all_angles_to_zero(self):
        for motor_id in range(1, 7):
            self.set_angle_entry_text(motor_id, "0")

    def flash_saved_feedback(self):
        for motor_id in range(1, 7):
            select_cell = self.axis_vars[motor_id]["select_cell"]
            axis_label = self.axis_vars[motor_id]["axis_label"]
            button = self.axis_vars[motor_id]["select_button"]
            angle_entry = self.angle_entries[motor_id]

            select_cell.configure(bg=self.colors["row_saved"])
            axis_label.configure(bg=self.colors["row_saved"])
            angle_entry.configure(
                state="disabled",
                disabledbackground=self.colors["row_saved"],
                disabledforeground=self.colors["text_dark"]
            )
            button.configure(
                bg=self.colors["row_saved"],
                activebackground=self.colors["row_saved"]
            )

        self.root.after(600, self.reset_table_selection)

    def move_all_selected(self):
        selected_motors = []

        for motor_id in range(1, 7):
            if self.axis_vars[motor_id]["selected"].get():
                self.clamp_angle(motor_id)
                angle = float(self.angle_entries[motor_id].get())
                selected_motors.append((motor_id, angle))

        if not selected_motors:
            self.log("Aucun moteur sélectionné.")
            return

        for motor_id, angle in selected_motors:
            self.send_command({
                "command": "moveMotor",
                "motorID": motor_id,
                "angle": angle
            })

    def save_current_position(self):
        keypad = TextKeypad(self.root, "Nom de la position")
        position_name = keypad.get_value()

        if not position_name:
            self.log("Enregistrement annulé.")
            return

        position_data = {}

        for motor_id in range(1, 7):
            self.clamp_angle(motor_id)
            angle = float(self.angle_entries[motor_id].get())
            position_data[motor_id] = angle

        self.saved_positions[position_name] = position_data
        self.log(f"Position enregistrée : {position_name} -> {position_data}")
        self.flash_saved_feedback()
        self.reset_all_angles_to_zero()

    def load_saved_position(self):
        if not self.saved_positions:
            self.log("Aucune position enregistrée.")
            return

        load_window = tk.Toplevel(self.root)
        load_window.title("Choisir une position")
        load_window.geometry("680x700")
        load_window.resizable(False, False)
        load_window.configure(bg="#f7f9fc")
        load_window.transient(self.root)
        load_window.grab_set()

        title = tk.Label(
            load_window,
            text="Positions enregistrées",
            font=("Segoe UI", 14, "bold"),
            bg="#f7f9fc",
            fg="#1f2937"
        )
        title.pack(pady=(10, 6))

        listbox = tk.Listbox(
            load_window,
            font=("Consolas", 18),
            bg="white",
            fg="#6d1533",
            relief="solid",
            bd=1
        )
        listbox.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        for position_name in self.saved_positions.keys():
            listbox.insert(tk.END, position_name)

        def apply_selected_position():
            selection = listbox.curselection()
            if not selection:
                self.log("Aucune position sélectionnée.")
                return

            position_name = listbox.get(selection[0])
            position_data = self.saved_positions[position_name]
            motors_list = []

            for motor_id, angle in position_data.items():
                self.set_angle_entry_text(motor_id, self.format_angle(angle))

                motors_list.append({
                    "motorID": motor_id,
                    "angle": angle
                })

            self.log(f"Position chargée : {position_name}")

            self.send_command({
                "command": "moveMotors",
                "motors": motors_list
            })

            load_window.destroy()

        def delete_selected_position():
            selection = listbox.curselection()
            if not selection:
                self.log("Choisis une position à supprimer.")
                return

            position_name = listbox.get(selection[0])
            del self.saved_positions[position_name]
            listbox.delete(selection[0])
            self.log(f"Position supprimée : {position_name}")

            if not self.saved_positions:
                load_window.destroy()

        buttons_frame = tk.Frame(load_window, bg="#f7f9fc")
        buttons_frame.pack(pady=(0, 10))

        load_button = tk.Button(
            buttons_frame,
            text="Charger",
            command=apply_selected_position,
            bg=self.colors["button_primary"],
            fg="white",
            activebackground=self.colors["button_primary"],
            activeforeground="white",
            font=("Segoe UI", 16, "bold"),
            width=12,
            relief="flat",
            bd=0,
            padx=12,
            pady=16,
            cursor="hand2"
        )
        load_button.pack(side="left", padx=10)

        delete_button = tk.Button(
            buttons_frame,
            text="Supprimer",
            command=delete_selected_position,
            bg=self.colors["button_red"],
            fg="white",
            activebackground=self.colors["button_red"],
            activeforeground="white",
            font=("Segoe UI", 16, "bold"),
            width=12,
            relief="flat",
            bd=0,
            padx=12,
            pady=16,
            cursor="hand2"
        )
        delete_button.pack(side="left", padx=10)

        listbox.bind("<Double-Button-1>", lambda event: apply_selected_position())

    def create_link(self):
        if len(self.saved_positions) < 2:
            self.log("Il faut au moins 2 positions enregistrées pour créer une liaison.")
            return

        name_keypad = TextKeypad(self.root, "Nom de la liaison")
        link_name = name_keypad.get_value()

        if not link_name:
            self.log("Création de liaison annulée.")
            return

        link_window = tk.Toplevel(self.root)
        link_window.title("Créer une liaison")
        link_window.geometry("680x700")
        link_window.resizable(False, False)
        link_window.configure(bg="#f7f9fc")
        link_window.transient(self.root)
        link_window.grab_set()

        title = tk.Label(
            link_window,
            text="Créer l'ordre de la liaison",
            font=("Segoe UI", 11, "bold"),
            bg="#f7f9fc",
            fg="#1f2937"
        )
        title.pack(pady=(10, 6))

        content = tk.Frame(link_window, bg="#f7f9fc")
        content.pack(fill="both", expand=True, padx=10, pady=10)

        left_frame = tk.Frame(content, bg="#f7f9fc")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

        center_frame = tk.Frame(content, bg="#f7f9fc")
        center_frame.pack(side="left", fill="y", padx=4)

        right_frame = tk.Frame(content, bg="#f7f9fc")
        right_frame.pack(side="left", fill="both", expand=True, padx=(8, 0))

        tk.Label(
            left_frame,
            text="Positions disponibles",
            font=("Segoe UI", 13, "bold"),
            bg="#f7f9fc",
            fg="#6d1533"
        ).pack(pady=(0, 6))

        available_listbox = tk.Listbox(
            left_frame,
            font=("Consolas", 18),
            bg="white",
            fg="#6d1533",
            relief="solid",
            bd=1,
            exportselection=False
        )
        available_listbox.pack(fill="both", expand=True)

        for position_name in self.saved_positions.keys():
            available_listbox.insert(tk.END, position_name)

        tk.Label(
            right_frame,
            text="Ordre de la liaison",
            font=("Segoe UI", 13, "bold"),
            bg="#f7f9fc",
            fg="#6d1533"
        ).pack(pady=(0, 6))

        ordered_listbox = tk.Listbox(
            right_frame,
            font=("Consolas", 18),
            bg="white",
            fg="#6d1533",
            relief="solid",
            bd=1,
            exportselection=False
        )
        ordered_listbox.pack(fill="both", expand=True)

        def add_position():
            selection = available_listbox.curselection()
            if not selection:
                self.log("Choisis une position à ajouter.")
                return

            position_name = available_listbox.get(selection[0])
            ordered_listbox.insert(tk.END, position_name)

        def remove_position():
            selection = ordered_listbox.curselection()
            if not selection:
                self.log("Choisis une position à retirer.")
                return

            ordered_listbox.delete(selection[0])

        def delete_available_position():
            selection = available_listbox.curselection()
            if not selection:
                self.log("Choisis une position à supprimer.")
                return

            position_name = available_listbox.get(selection[0])

            if position_name in self.saved_positions:
                del self.saved_positions[position_name]

            available_listbox.delete(selection[0])
            self.log(f"Position supprimée : {position_name}")

        def move_up():
            selection = ordered_listbox.curselection()
            if not selection:
                self.log("Choisis une position dans l'ordre de la liaison.")
                return

            index = selection[0]
            if index == 0:
                return

            item = ordered_listbox.get(index)
            ordered_listbox.delete(index)
            ordered_listbox.insert(index - 1, item)
            ordered_listbox.selection_clear(0, tk.END)
            ordered_listbox.selection_set(index - 1)
            ordered_listbox.activate(index - 1)

        def move_down():
            selection = ordered_listbox.curselection()
            if not selection:
                self.log("Choisis une position dans l'ordre de la liaison.")
                return

            index = selection[0]
            if index == ordered_listbox.size() - 1:
                return

            item = ordered_listbox.get(index)
            ordered_listbox.delete(index)
            ordered_listbox.insert(index + 1, item)
            ordered_listbox.selection_clear(0, tk.END)
            ordered_listbox.selection_set(index + 1)
            ordered_listbox.activate(index + 1)

        def save_link_selection():
            ordered_positions = list(ordered_listbox.get(0, tk.END))

            if len(ordered_positions) < 2:
                self.log("Il faut au moins 2 positions dans la liaison.")
                return

            self.saved_links[link_name] = ordered_positions
            self.log(f"Liaison enregistrée : {link_name} -> {ordered_positions}")
            link_window.destroy()

        add_btn = tk.Button(
            center_frame,
            text="Add →",
            command=add_position,
            bg=self.colors["button_primary"],
            fg="white",
            activebackground=self.colors["button_primary"],
            activeforeground="white",
            font=("Segoe UI", 12, "bold"),
            width=10,
            relief="flat",
            bd=0,
            padx=6,
            pady=10,
            cursor="hand2"
        )
        add_btn.pack(pady=6)

        remove_btn = tk.Button(
            center_frame,
            text="Remove",
            command=remove_position,
            bg=self.colors["button_red"],
            fg="white",
            activebackground=self.colors["button_red"],
            activeforeground="white",
            font=("Segoe UI", 12, "bold"),
            width=10,
            relief="flat",
            bd=0,
            padx=6,
            pady=10,
            cursor="hand2"
        )
        remove_btn.pack(pady=6)

        delete_btn = tk.Button(
            center_frame,
            text="Supprimer",
            command=delete_available_position,
            bg=self.colors["button_gray"],
            fg="white",
            activebackground=self.colors["button_gray"],
            activeforeground="white",
            font=("Segoe UI", 12, "bold"),
            width=10,
            relief="flat",
            bd=0,
            padx=6,
            pady=10,
            cursor="hand2"
        )
        delete_btn.pack(pady=6)

        up_btn = tk.Button(
            center_frame,
            text="Up",
            command=move_up,
            bg=self.colors["button_gray"],
            fg="white",
            activebackground=self.colors["button_gray"],
            activeforeground="white",
            font=("Segoe UI", 12, "bold"),
            width=10,
            relief="flat",
            bd=0,
            padx=6,
            pady=10,
            cursor="hand2"
        )
        up_btn.pack(pady=6)

        down_btn = tk.Button(
            center_frame,
            text="Down",
            command=move_down,
            bg=self.colors["button_gray"],
            fg="white",
            activebackground=self.colors["button_gray"],
            activeforeground="white",
            font=("Segoe UI", 12, "bold"),
            width=10,
            relief="flat",
            bd=0,
            padx=6,
            pady=10,
            cursor="hand2"
        )
        down_btn.pack(pady=6)

        save_btn = tk.Button(
            center_frame,
            text="Save Link",
            command=save_link_selection,
            bg=self.colors["button_green"],
            fg="white",
            activebackground=self.colors["button_green"],
            activeforeground="white",
            font=("Segoe UI", 12, "bold"),
            width=10,
            relief="flat",
            bd=0,
            padx=6,
            pady=10,
            cursor="hand2"
        )
        save_btn.pack(pady=16)

    def run_link(self):
        if not self.saved_links:
            self.log("Aucune liaison enregistrée.")
            return

        run_window = tk.Toplevel(self.root)
        run_window.title("Exécuter une liaison")
        run_window.geometry("680x700")
        run_window.resizable(False, False)
        run_window.configure(bg="#f7f9fc")
        run_window.transient(self.root)
        run_window.grab_set()

        title = tk.Label(
            run_window,
            text="Liaisons enregistrées",
            font=("Segoe UI", 14, "bold"),
            bg="#f7f9fc",
            fg="#1f2937"
        )
        title.pack(pady=(10, 6))

        listbox = tk.Listbox(
            run_window,
            font=("Consolas", 18),
            bg="white",
            fg="#6d1533",
            relief="solid",
            bd=1
        )
        listbox.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        for link_name in self.saved_links.keys():
            listbox.insert(tk.END, link_name)

        def start_selected_link():
            selection = listbox.curselection()
            if not selection:
                self.log("Aucune liaison sélectionnée.")
                return

            link_name = listbox.get(selection[0])
            run_window.destroy()

            code_keypad = TextKeypad(self.root, f"Code de sauvegarde de '{link_name}'")
            code = code_keypad.get_value()

            if not code:
                self.log("Lancement annulé.")
                return

            if not os.path.exists(self.save_file_path):
                self.log("Aucune sauvegarde trouvée pour ce code.")
                return

            try:
                with open(self.save_file_path, "r", encoding="utf-8") as save_file:
                    all_saves = json.load(save_file)
            except (json.JSONDecodeError, OSError) as error:
                self.log(f"Erreur de lecture de la sauvegarde : {error}")
                return

            if code not in all_saves:
                self.log("Code introuvable.")
                return

            entry = all_saves[code]
            links_in_entry = entry.get("links", {})

            if link_name not in links_in_entry:
                self.log(f"La liaison '{link_name}' n'est pas enregistrée sous ce code.")
                return

            positions_in_entry = {
                name: {int(motor_id): angle for motor_id, angle in position.items()}
                for name, position in entry.get("positions", {}).items()
            }
            self.saved_positions.update(positions_in_entry)

            positions_sequence = links_in_entry[link_name]
            self.log(f"Démarrage liaison : {link_name} -> {positions_sequence}")
            self.execute_link_sequence(positions_sequence, 0)

        run_button = tk.Button(
            run_window,
            text="Lancer",
            command=start_selected_link,
            bg=self.colors["button_green"],
            fg="white",
            activebackground=self.colors["button_green"],
            activeforeground="white",
            font=("Segoe UI", 16, "bold"),
            width=12,
            relief="flat",
            bd=0,
            padx=12,
            pady=16,
            cursor="hand2"
        )
        run_button.pack(pady=(0, 16))

        listbox.bind("<Double-Button-1>", lambda event: start_selected_link())

    def execute_link_sequence(self, positions_sequence, index):
        if index >= len(positions_sequence):
            self.log("Liaison terminée.")
            return

        position_name = positions_sequence[index]

        if position_name not in self.saved_positions:
            self.log(f"Position introuvable dans la liaison : {position_name}")
            return

        position_data = self.saved_positions[position_name]
        motors_list = []

        for motor_id, angle in position_data.items():
            self.set_angle_entry_text(motor_id, self.format_angle(angle))

            motors_list.append({
                "motorID": motor_id,
                "angle": angle
            })

        self.log(f"Exécution position : {position_name}")

        self.send_command({
            "command": "moveMotors",
            "motors": motors_list
        })

        self.root.after(
            self.link_delay_ms,
            lambda: self.execute_link_sequence(positions_sequence, index + 1)
        )

    def persist_save(self):
        if not self.saved_positions and not self.saved_links:
            self.log("Aucune position ni liaison à sauvegarder.")
            return

        all_saves = {}
        if os.path.exists(self.save_file_path):
            try:
                with open(self.save_file_path, "r", encoding="utf-8") as save_file:
                    all_saves = json.load(save_file)
            except (json.JSONDecodeError, OSError):
                all_saves = {}

        name_keypad = TextKeypad(self.root, "Nom de la sauvegarde")
        save_name = name_keypad.get_value()

        if not save_name:
            self.log("Sauvegarde annulée.")
            return

        overwrite = save_name in all_saves

        select_window = tk.Toplevel(self.root)
        select_window.title("Sauvegarder")
        select_window.geometry("680x700")
        select_window.resizable(False, False)
        select_window.configure(bg="#f7f9fc")
        select_window.transient(self.root)
        select_window.grab_set()

        title = tk.Label(
            select_window,
            text=f"Sauvegarde : {save_name}",
            font=("Segoe UI", 14, "bold"),
            bg="#f7f9fc",
            fg="#1f2937"
        )
        title.pack(pady=(12, 2))

        subtitle_text = "Choisissez ce que vous voulez enregistrer."
        if overwrite:
            subtitle_text = "Ce nom existe déjà : la sauvegarde sera remplacée. " + subtitle_text

        subtitle = tk.Label(
            select_window,
            text=subtitle_text,
            font=("Segoe UI", 9),
            bg="#f7f9fc",
            fg="#6b7280",
            wraplength=620
        )
        subtitle.pack(pady=(0, 8))

        content = tk.Frame(select_window, bg="#f7f9fc")
        content.pack(fill="both", expand=True, padx=14, pady=6)

        left_frame = tk.Frame(content, bg="#f7f9fc")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

        right_frame = tk.Frame(content, bg="#f7f9fc")
        right_frame.pack(side="left", fill="both", expand=True, padx=(8, 0))

        tk.Label(
            left_frame,
            text="Positions",
            font=("Segoe UI", 9, "bold"),
            bg="#f7f9fc",
            fg="#6d1533"
        ).pack(pady=(0, 6))

        positions_listbox = tk.Listbox(
            left_frame,
            font=("Consolas", 10),
            bg="white",
            fg="#6d1533",
            relief="solid",
            bd=1,
            selectmode="extended",
            exportselection=False
        )
        positions_listbox.pack(fill="both", expand=True)

        position_names = list(self.saved_positions.keys())
        for position_name in position_names:
            positions_listbox.insert(tk.END, position_name)

        tk.Label(
            right_frame,
            text="Liaisons",
            font=("Segoe UI", 9, "bold"),
            bg="#f7f9fc",
            fg="#6d1533"
        ).pack(pady=(0, 6))

        links_listbox = tk.Listbox(
            right_frame,
            font=("Consolas", 10),
            bg="white",
            fg="#6d1533",
            relief="solid",
            bd=1,
            selectmode="extended",
            exportselection=False
        )
        links_listbox.pack(fill="both", expand=True)

        link_names = list(self.saved_links.keys())
        for link_name in link_names:
            links_listbox.insert(tk.END, link_name)

        def confirm_save():
            selected_positions = [position_names[i] for i in positions_listbox.curselection()]
            selected_links = [link_names[i] for i in links_listbox.curselection()]

            if not selected_positions and not selected_links:
                self.log("Sélectionne au moins une position ou une liaison.")
                return

            positions_to_save = {
                name: {str(motor_id): angle for motor_id, angle in self.saved_positions[name].items()}
                for name in selected_positions
            }
            links_to_save = {name: self.saved_links[name] for name in selected_links}

            all_saves[save_name] = {
                "positions": positions_to_save,
                "links": links_to_save
            }

            try:
                with open(self.save_file_path, "w", encoding="utf-8") as save_file:
                    json.dump(all_saves, save_file, ensure_ascii=False, indent=2)
                select_window.destroy()
                self.log(
                    f"Sauvegardé sous le nom '{save_name}' -> "
                    f"positions : {selected_positions if selected_positions else 'aucune'}, "
                    f"liaisons : {selected_links if selected_links else 'aucune'}"
                )
            except OSError as error:
                self.log(f"Erreur lors de la sauvegarde : {error}")

        save_button = tk.Button(
            select_window,
            text="Enregistrer la sélection",
            command=confirm_save,
            bg=self.colors["button_green"],
            fg="white",
            activebackground=self.colors["button_green"],
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=10,
            pady=8,
            cursor="hand2"
        )
        save_button.pack(pady=(6, 12))

    def persist_load(self):
        if not os.path.exists(self.save_file_path):
            self.log("Aucune sauvegarde trouvée.")
            return

        try:
            with open(self.save_file_path, "r", encoding="utf-8") as save_file:
                all_saves = json.load(save_file)
        except (json.JSONDecodeError, OSError) as error:
            self.log(f"Erreur de lecture de la sauvegarde : {error}")
            return

        if not all_saves:
            self.log("Aucune sauvegarde trouvée.")
            return

        load_window = tk.Toplevel(self.root)
        load_window.title("Récupérer une sauvegarde")
        load_window.geometry("680x700")
        load_window.resizable(False, False)
        load_window.configure(bg="#f7f9fc")
        load_window.transient(self.root)
        load_window.grab_set()

        title = tk.Label(
            load_window,
            text="Sauvegardes disponibles",
            font=("Segoe UI", 13, "bold"),
            bg="#f7f9fc",
            fg="#1f2937"
        )
        title.pack(pady=(10, 6))

        listbox = tk.Listbox(
            load_window,
            font=("Consolas", 14),
            bg="white",
            fg="#6d1533",
            relief="solid",
            bd=1
        )
        listbox.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        codes = []

        def refresh_listbox():
            codes.clear()
            listbox.delete(0, tk.END)
            for save_code in all_saves.keys():
                codes.append(save_code)
                entry = all_saves[save_code]
                nb_positions = len(entry.get("positions", {}))
                nb_links = len(entry.get("links", {}))
                listbox.insert(
                    tk.END,
                    f"{save_code}  ({nb_positions} position(s), {nb_links} liaison(s))"
                )

        refresh_listbox()

        def load_selected():
            selection = listbox.curselection()
            if not selection:
                self.log("Aucune sauvegarde sélectionnée.")
                return

            code = codes[selection[0]]
            entry = all_saves[code]

            loaded_positions = {
                name: {int(motor_id): angle for motor_id, angle in position.items()}
                for name, position in entry.get("positions", {}).items()
            }
            loaded_links = entry.get("links", {})

            self.saved_positions.update(loaded_positions)
            self.saved_links.update(loaded_links)

            load_window.destroy()
            self.log(f"Travail récupéré pour le code : {code}")
            self.log(f"Positions récupérées : {list(loaded_positions.keys()) if loaded_positions else 'aucune'}")
            self.log(f"Liaisons récupérées : {list(loaded_links.keys()) if loaded_links else 'aucune'}")

        def delete_selected():
            selection = listbox.curselection()
            if not selection:
                self.log("Aucune sauvegarde sélectionnée.")
                return

            code = codes[selection[0]]
            del all_saves[code]

            try:
                with open(self.save_file_path, "w", encoding="utf-8") as save_file:
                    json.dump(all_saves, save_file, ensure_ascii=False, indent=2)
                self.log(f"Sauvegarde '{code}' supprimée.")
            except OSError as error:
                self.log(f"Erreur lors de la suppression : {error}")
                return

            refresh_listbox()

        buttons_frame = tk.Frame(load_window, bg="#f7f9fc")
        buttons_frame.pack(pady=(0, 16))

        load_button = tk.Button(
            buttons_frame,
            text="Charger",
            command=load_selected,
            bg=self.colors["button_green"],
            fg="white",
            activebackground=self.colors["button_green"],
            activeforeground="white",
            font=("Segoe UI", 16, "bold"),
            width=12,
            relief="flat",
            bd=0,
            padx=12,
            pady=16,
            cursor="hand2"
        )
        load_button.pack(side="left", padx=10)

        delete_button = tk.Button(
            buttons_frame,
            text="Supprimer",
            command=delete_selected,
            bg=self.colors["button_red"],
            fg="white",
            activebackground=self.colors["button_red"],
            activeforeground="white",
            font=("Segoe UI", 16, "bold"),
            width=12,
            relief="flat",
            bd=0,
            padx=12,
            pady=16,
            cursor="hand2"
        )
        delete_button.pack(side="left", padx=10)

        listbox.bind("<Double-Button-1>", lambda event: load_selected())

    def log(self, message):
        print(message)

    def send_command(self, command_dict):
        json_command = json.dumps(command_dict, ensure_ascii=False)
        self.log(json_command)


if __name__ == "__main__":
    root = tk.Tk()
    app = RobotControlApp(root)
    root.mainloop()