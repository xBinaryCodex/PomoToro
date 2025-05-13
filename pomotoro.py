import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import QTimer, Qt

class PomoToro(QWidget):
    def __init__(self):
        super().__init__()

        # --- window setup ---
        self.setWindowTitle("PomoToro")
        self.setGeometry(100, 100, 300, 300)
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

        self.time_left = 5

        # --- Status ---
        self.current_mode = "Work"
        self.session_count = 0

        # --- Status label ---
        self.status_label = QLabel("Status: Work")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 20px")
        layout.insertWidget(0, self.status_label)

    def start_timer(self):
        self.timer.start(1000)

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
                    self.start_long_break()
                else:
                    self.start_short_break()
            elif self.current_mode in ["Short Break", "Long Break"]:
                self.start_work_session()

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


if __name__ =="__main__":
    app = QApplication(sys.argv)
    window = PomoToro()
    window.show()
    sys.exit(app.exec())