from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QApplication
from PyQt5.QtGui import QPalette, QIcon, QImage, QPixmap
from PyQt5 import QtSvg
from my_image_data import MyImage
from icon_button import IconButton


class MyTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAutoFillBackground(True)
        p = QPalette()
        p.setColor(p.ColorRole.Background, Qt.GlobalColor.white)
        self.setPalette(p)
        self.setFixedHeight(30)
        self.setObjectName('TitleBar')
        self.setStyleSheet(
            """#TitleBar{
                background-color: #1f1f1f;
                border: 0px;
                border-radius: 10px;
                }
            """
        )
        self.setContentsMargins(0, 0, 0, 0)

        close_btn = IconButton(self)
        pix = MyImage.get_pixmap('close')
        close_btn.setIcon(QIcon(pix))
        close_btn.set_align('right')
        close_btn.set_close()
        close_btn.clicked.connect(QApplication.closeAllWindows)
        
        self.menu_btn = IconButton(self)
        pix = MyImage.get_pixmap('menu')
        self.menu_btn.setIcon(QIcon(pix))
        self.menu_btn.set_align('left')
        # self.menu_btn.clicked.connect(self.__setting_popup)

        self.reset_btn = IconButton(self)
        pix = MyImage.get_pixmap('reset')
        self.reset_btn.setIcon(QIcon(pix))
        self.reset_btn.setFixedWidth(40)
        
        self.play_btn = IconButton(self)
        self.play_pix = MyImage.get_pixmap('play')
        self.pause_pix = MyImage.get_pixmap('pause')
        self.play_btn.setIcon(QIcon(self.play_pix))
        self.play_btn.setFixedWidth(90)

        layout.addWidget(self.menu_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addSpacing(1)
        layout.addWidget(self.reset_btn)
        layout.addWidget(self.play_btn)
        layout.addSpacing(1)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)
    

    def change_play_pix(self, is_play):
        if is_play is True:
            self.play_btn.setIcon(QIcon(self.pause_pix))
        else:
            self.play_btn.setIcon(QIcon(self.play_pix))
