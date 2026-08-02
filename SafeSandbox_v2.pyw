# -*- coding: utf-8 -*-
"""Desktop shell for the SafeSandbox v2 workspace."""

import os
import sys
import traceback

os.environ.setdefault(
    "QTWEBENGINE_CHROMIUM_FLAGS",
    "--disable-gpu-shader-disk-cache",
)

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QRect, Qt, QTimer, QUrl
from PyQt6.QtGui import QColor, QFont, QIcon, QPainter, QPen, QPixmap
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget


APP_NAME = "SafeSandbox"
HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(HERE, "SafeSandbox_v2.html")

INK = QColor("#111525")
PANEL = QColor("#171B2C")
PURPLE = QColor("#735FFF")
CYAN = QColor("#20CAD8")
MUTED = QColor("#9DA3B7")
WHITE = QColor("#F7F8FC")


class LaunchCard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(520, 270)

        screen = QApplication.primaryScreen().availableGeometry()
        self.move(
            screen.center().x() - self.width() // 2,
            screen.center().y() - self.height() // 2,
        )

        self.progress = 8
        self.display_progress = 8
        self.status = "Preparing local workspace"
        self.pulse = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(24)

        self.animation = QPropertyAnimation(self, b"windowOpacity", self)
        self.animation.setDuration(260)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def showEvent(self, event):
        super().showEvent(event)
        self.animation.start()

    def advance(self, status, amount):
        self.status = status
        self.progress = min(96, self.progress + amount)
        QApplication.processEvents()

    def finish(self):
        self.progress = 100
        self.display_progress = 100
        self.status = "Workspace ready"
        self.update()
        QApplication.processEvents()

    def _tick(self):
        self.pulse = (self.pulse + 1) % 120
        if self.display_progress < self.progress:
            self.display_progress += 1
        self.update()

    def paintEvent(self, event):
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(INK)
        painter.drawRoundedRect(8, 8, 504, 254, 24, 24)

        painter.setBrush(PANEL)
        painter.drawRoundedRect(24, 24, 152, 222, 18, 18)

        gradient_phase = abs(60 - self.pulse) / 60
        mark_color = QColor(
            int(PURPLE.red() + (CYAN.red() - PURPLE.red()) * gradient_phase),
            int(PURPLE.green() + (CYAN.green() - PURPLE.green()) * gradient_phase),
            int(PURPLE.blue() + (CYAN.blue() - PURPLE.blue()) * gradient_phase),
        )
        painter.setBrush(mark_color)
        painter.drawRoundedRect(66, 59, 68, 68, 20, 20)
        painter.setPen(WHITE)
        painter.setFont(QFont("Segoe UI", 27, QFont.Weight.Bold))
        painter.drawText(QRect(66, 59, 68, 68), Qt.AlignmentFlag.AlignCenter, "S")

        painter.setPen(WHITE)
        painter.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        painter.drawText(
            QRect(38, 151, 124, 24),
            Qt.AlignmentFlag.AlignCenter,
            APP_NAME,
        )
        painter.setPen(MUTED)
        painter.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
        painter.drawText(
            QRect(38, 175, 124, 18),
            Qt.AlignmentFlag.AlignCenter,
            "LOCAL ANALYSIS",
        )

        painter.setPen(PURPLE)
        painter.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        painter.drawText(206, 65, "OPENING WORKSPACE")

        painter.setPen(WHITE)
        painter.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        painter.drawText(206, 103, "Triage Desk")

        painter.setPen(MUTED)
        painter.setFont(QFont("Segoe UI", 9))
        painter.drawText(206, 130, self.status)

        track = QRect(206, 171, 266, 8)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#292F47"))
        painter.drawRoundedRect(track, 4, 4)

        fill_width = int(track.width() * self.display_progress / 100)
        if fill_width:
            painter.setBrush(PURPLE)
            painter.drawRoundedRect(
                QRect(track.x(), track.y(), fill_width, track.height()),
                4,
                4,
            )

        painter.setPen(MUTED)
        painter.setFont(QFont("Consolas", 8))
        painter.drawText(206, 207, "OFFLINE")
        painter.setPen(WHITE)
        painter.setFont(QFont("Consolas", 9, QFont.Weight.Bold))
        painter.drawText(
            QRect(400, 194, 72, 18),
            Qt.AlignmentFlag.AlignRight,
            f"{self.display_progress:02d}%",
        )


def make_icon():
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(PURPLE)
    painter.drawRoundedRect(5, 5, 54, 54, 16, 16)
    painter.setPen(WHITE)
    painter.setFont(QFont("Segoe UI", 25, QFont.Weight.Bold))
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "S")
    painter.end()
    return QIcon(pixmap)


class SafeSandboxWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(make_icon())
        self.resize(1440, 900)

        self.view = QWebEngineView(self)
        settings = self.view.settings()
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls,
            True,
        )
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptEnabled,
            True,
        )
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalStorageEnabled,
            True,
        )
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.ScreenCaptureEnabled,
            False,
        )

        self.view.titleChanged.connect(
            lambda title: self.setWindowTitle(title or APP_NAME)
        )
        self.view.loadFinished.connect(self._load_finished)
        self.setCentralWidget(self.view)

    def _load_finished(self, loaded):
        if not loaded:
            QMessageBox.critical(
                self,
                APP_NAME,
                f"Could not open the local workspace:\n{HTML_PATH}",
            )

    def open_workspace(self):
        if not os.path.isfile(HTML_PATH):
            QMessageBox.critical(
                self,
                APP_NAME,
                "SafeSandbox_v2.html is missing.\n\n"
                f"Expected:\n{HTML_PATH}\n\n"
                "Keep the HTML and PYW files together.",
            )
            return False
        self.view.load(QUrl.fromLocalFile(HTML_PATH))
        return True


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setWindowIcon(make_icon())

    splash = LaunchCard()
    splash.show()
    app.processEvents()

    splash.advance("Starting offline renderer", 20)
    window = SafeSandboxWindow()
    splash.advance("Loading analysis workspace", 34)

    def reveal_workspace(loaded):
        if not loaded:
            splash.close()
            return
        splash.advance("Restoring local preferences", 28)

        def finish_launch():
            splash.finish()
            window.showMaximized()
            QTimer.singleShot(350, splash.close)

        QTimer.singleShot(1400, finish_launch)

    window.view.loadFinished.connect(reveal_workspace)
    if not window.open_workspace():
        splash.close()
        return 1

    return app.exec()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        try:
            QMessageBox.critical(
                None,
                f"{APP_NAME} startup error",
                traceback.format_exc(),
            )
        except Exception:
            pass
        sys.exit(1)
