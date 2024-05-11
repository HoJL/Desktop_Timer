from PyQt5.QtCore import QEvent, Qt, QSize
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QMouseEvent, QPalette, QIcon, QImage, QPixmap, QColor
from my_image_data import MyImage

class IconButton(QPushButton):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setFixedSize(30, 30)
        self.setContentsMargins(0,0,0,0)
        self.setIconSize(QSize(30, 30))
        self.setObjectName('IconBtn')
        self.setStyleSheet(
            """QPushButton#IconBtn{
                    border: 0;
                }
                QPushButton#IconBtn[enter=true][close=true] {
                    background-color: rgb(236, 13, 13);
                }
                QPushButton#IconBtn[enter=true][close=true]:pressed {
                    background-color: rgb(170, 0, 0);
                }
                QPushButton#IconBtn[enter=true] {
                    background-color: rgba(255, 255, 255, 0.3);
                }
                QPushButton#IconBtn[enter=true]:pressed {
                    background-color: rgba(255, 255, 255, 0.4);
                }
                QPushButton#IconBtn[enter=false] {
                    background-color: rgba(255, 255, 255, 0);
                }
                QPushButton#IconBtn[align='left'] {
                    border-top-left-radius: 9px;
                    border-bottom-left-radius: 9px;
                }
                QPushButton#IconBtn[align='right'] {
                    border-top-right-radius: 9px;
                    border-bottom-right-radius: 9px;
                }
            """
        )
        self.p_red = QPalette()
        self.p_red.setColor(QPalette.ColorRole.Background, Qt.GlobalColor.red)

        self.p_white = QPalette()
        self.p_white.setColor(QPalette.ColorRole.Background, QColor(255, 255, 255))
        # self.setMouseTracking(True)

        self.hover_pix = None

    def set_align(self, align: str):
        self.setProperty('align', align)
        self.style().unpolish(self)
        self.style().polish(self)

    def set_close(self, b = True):
        self.setProperty('close', b)
        self.style().unpolish(self)
        self.style().polish(self)

    def enterEvent(self, a0: QEvent | None) -> None:
        self.setProperty('enter', True)
        self.style().unpolish(self)
        self.style().polish(self)

    def leaveEvent(self, a0: QEvent | None) -> None:
        self.setProperty('enter', False)
        self.style().unpolish(self)
        self.style().polish(self)

