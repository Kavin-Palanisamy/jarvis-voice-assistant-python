import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QFrame
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QColor, QFont, QPainter, QPen, QBrush
import psutil

class GlowingRing(QWidget):
    def __init__(self, parent=None, size=200, color=QColor(0, 255, 255, 150), speed=2000):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.color = color
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(50)

    def rotate(self):
        self.angle = (self.angle + 5) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(self.color, 2)
        pen.setDashPattern([10, 5])
        painter.setPen(pen)
        
        painter.translate(self.width() // 2, self.height() // 2)
        painter.rotate(self.angle)
        
        painter.drawEllipse(-self.width() // 2 + 5, -self.height() // 2 + 5, self.width() - 10, self.height() - 10)

class JarvisHUD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.status = "SYSTEM ONLINE"
        self.initUI()

    def initUI(self):
        # Set window stays on top, transparent, and frameless
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 400, 500)

        # Central Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)

        # Glowing Ring
        self.ring = GlowingRing(self, size=250)
        self.layout.addWidget(self.ring)

        # Status Label
        self.status_label = QLabel(self.status)
        self.status_label.setStyleSheet("color: #00ffff; font-family: 'Orbitron', 'Segoe UI'; font-size: 24px; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        # System Stats Label
        self.stats_label = QLabel("CPU: 0% | RAM: 0%")
        self.stats_label.setStyleSheet("color: #00ffff; font-family: 'Consolas'; font-size: 14px; opacity: 0.7;")
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.stats_label)

        # Camera Feed Panel (Minimized by default)
        self.camera_label = QLabel("Camera Feed: OFFLINE")
        self.camera_label.setFixedSize(200, 150)
        self.camera_label.setStyleSheet("border: 1px solid #00ffff; background: rgba(0, 0, 0, 150); color: #00ffff; font-size: 10px;")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.camera_label)

        # Log Frame
        self.log_label = QLabel("Waiting for input...")
        self.log_label.setStyleSheet("color: #00ffff; font-family: 'Consolas'; font-size: 12px; border: 1px solid #00ffff; padding: 10px; background: rgba(0, 40, 40, 100);")
        self.log_label.setWordWrap(True)
        self.layout.addWidget(self.log_label)

        # Timer for stats update
        self.stats_timer = QTimer(self)
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(2000)

    def update_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        self.stats_label.setText(f"CPU: {cpu}% | RAM: {ram}%")

    def update_status(self, status, message=""):
        self.status_label.setText(status)
        if message:
            self.log_label.setText(message)
        
        # Change color based on status
        if "LISTENING" in status:
            self.status_label.setStyleSheet("color: #00ff00; font-family: 'Orbitron'; font-size: 24px; font-weight: bold;")
        elif "THINKING" in status:
            self.status_label.setStyleSheet("color: #ff00ff; font-family: 'Orbitron'; font-size: 24px; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: #00ffff; font-family: 'Orbitron'; font-size: 24px; font-weight: bold;")

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

def run_hud():
    app = QApplication(sys.argv)
    hud = JarvisHUD()
    hud.show()
    return app, hud

if __name__ == "__main__":
    app, hud = run_hud()
    sys.exit(app.exec_())
