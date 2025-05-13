import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import QTimer, Qt
import time
from pynput import keyboard, mouse

class PomoToro(QWidget):
    def __init__(self):
        super().__init__()

        # --- window setup ---
        self.setWindowTitle("PomoToro")
        self.setGeometry(100, 100, 500, 500)
        self.setStyleSheet("background-color: #1e1e2f; color: white;")

        # ---layout---
        layout = QVBoxLayout()

        # ---Timer Display---
        self.timer_label = QLabel("25:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 48px;")
        layout.addWidget(self.timer_label)

        # ---Start Button---
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)
        layout.addWidget(self.start_button)

        # ---Reset Button---
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_timer)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

        # --- Timer Logic ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.inactivity_timer = QTimer()
        self.inactivity_timer.timeout.connect(self.check_inactivity)
        self.inactivity_timer.start(1000)

        self.time_left = 25 * 60

        # --- Status ---
        self.current_mode = "Work"
        self.session_count = 0

        # --- Status label ---
        self.status_label = QLabel("Status: Work")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 20px")
        layout.insertWidget(0, self.status_label)

        # ---Inactivity checks---
        self.last_activity_time = time.time()
        self.learning_mode = False

        # --- KB & Mouse activity ---
        self.keyboard_listener = keyboard.Listener(on_press=self.update_activity)
        self.mouse_listener = mouse.Listener(on_move=self.update_activity, on_click=self.update_activity)

        self.keyboard_listener.start()
        self.mouse_listener.start()

        # --- Learning Mode ---
        self.learning_button = QPushButton("Learning Mode: Off")
        self.learning_button.setCheckable(True)
        self.learning_button.clicked.connect(self.toggle_learning_mode)
        layout.addWidget(self.learning_button)


    def start_timer(self):
        if self.time_left <= 0:
            self.update_timer_label()
        self.timer.start(1000)

        if self.current_mode == "Work":
            self.status_label.setText("Status: Work")
        elif self.current_mode == "Short Break":
            self.status_label.setText("Status: Short Break")
        elif self.current_mode == "Long Break":
            self.status_label.setText("Status: Long Break")

    def reset_timer(self):
        self.timer.stop()
        self.session_count = 0
        self.current_mode = "Work"
        self.time_left = 25 * 60
        self.update_timer_label()
        self.status_label.setText("Status: Work")

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_timer_label()
        else:
            self.timer.stop()

            if self.current_mode == "Work":
                self.session_count += 1

                if self.session_count % 4 == 0:
                    self.prepare_long_break()
                else:
                    self.prepare_short_break()

            elif self.current_mode in ["Short Break", "Long Break"]:
                self.prepare_work_session()


    def update_timer_label(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")

    def start_work_session(self):
        self.current_mode = "Work"
        self.time_left = 25 * 60
        self.update_timer_label()
        self.status_label.setText("Status: Work")
        self.timer.start(1000)

    def start_short_break(self):
        self.current_mode = "Short Break"
        self.time_left = 5 * 60
        self.update_timer_label()
        self.status_label.setText("Status: Short Break")
        self.timer.start(1000)

    def start_long_break(self):
        self.current_mode = "Long Break"
        self.time_left = 30 * 60
        self.update_timer_label()
        self.status_label.setText("Status: Long Break")
        self.timer.start(1000)

    def update_activity(self, *args):
        self.last_activity_time = time.time()

    def check_inactivity(self):
        if self.current_mode != "Work" or self.learning_mode:
            return
        
        time_since_last_input = time.time() - self.last_activity_time
        if time_since_last_input >= 10:
            self.timer.stop()
            self.time_left = 25 * 60
            self.update_timer_label()
            self.status_label.setText("Inactivity Detected: Timer Reset")

    def prepare_short_break(self):
        self.current_mode = "Short Break"
        self.time_left = 5 * 60
        self.update_timer_label()
        self.status_label.setText("Short break ready")

    def prepare_long_break(self):
        self.current_mode = "Long Break"
        self.time_left = 30 * 60
        self.update_timer_label()
        self.status_label.setText("Long break ready")

    def prepare_work_session(self):
        self.current_mode = "Work"
        self.time_left = 25 * 60
        self.update_timer_label()
        self.status_label.setText("Work session ready")

    def toggle_learning_mode(self):
        self.learning_mode = not self.learning_mode

        if self.learning_mode:
            self.learning_button.setText("Learning Mode: ON")
            self.learning_button.setStyleSheet("background-color: #2e8b57; color: white;")
            self.status_label.setText("Learning Mode Active")
        else:
            self.learning_button.setText("Learning Mode: OFF")
            self.learning_button.setStyleSheet("")
            self.status_label.setText(f"Status: {self.current_mode}")

if __name__ =="__main__":
    app = QApplication(sys.argv)
    window = PomoToro()
    window.show()
    sys.exit(app.exec())