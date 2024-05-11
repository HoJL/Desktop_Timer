from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QSpinBox, QPushButton, QHBoxLayout, QVBoxLayout, QDialog, QGridLayout, QStyle, QProxyStyle, QStyleOption, QStyleHintReturn, QApplication, QCheckBox, QComboBox
from PyQt5.QtGui import QPalette, QColor, QGuiApplication
from my_vcolorpicker import MyColorPicker

class MyStyle(QProxyStyle):
    def styleHint(self, hint: QStyle.StyleHint, option: QStyleOption = None, widget: QWidget = None, returnData: QStyleHintReturn = None) -> int:
        super().styleHint(hint, option, widget, returnData)
        if (hint == QStyle.StyleHint.SH_SpinControls_DisableOnBounds):
            return True
        return QProxyStyle.styleHint(self, hint, option)


class SettingDialog(QDialog):

    RES_OK = 1
    RES_CANCEL = -1
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.dark_mode()
        self.setWindowTitle('Setting')
        self.setObjectName('setting')
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        # self.setWindowFlags(Qt.WindowType.Window)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setMinimumWidth(300)
        self.resize(400, 400)
        self.orign = self.palette()
        self.res = -1
        self.base_layout = QVBoxLayout(self)
        time_layout = self.init_time()
        self.base_layout.addLayout(time_layout)
        self.base_layout.addSpacing(20)

        checkbox_option_layout = self.init_check_option()
        self.base_layout.addLayout(checkbox_option_layout)
        
        decision_layout = self.init_decision_button()
        self.base_layout.addStretch(3)
        self.base_layout.addLayout(decision_layout)
        self.color_picker = MyColorPicker()
        self.color_picker.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
    def exec_(self) -> int:
        self.__init_prev_data()
        self.color_picker.setGeometry(self.parent().geometry())
        return super().exec_()

    def __init_prev_data(self):
        self.prev_hour = self.hour_box.value()
        self.prev_minute = self.minute_box.value()
        self.prev_second = self.second_box.value()
        self.prev_auto_reset = self.auto_reset.isChecked()
        self.prev_loop = self.vibrate.isChecked()
        self.prev_sound_option = self.sound_combobox.currentIndex()
    
    def __revert_data(self):
        self.hour_box.setValue(self.prev_hour)
        self.minute_box.setValue(self.prev_minute)
        self.second_box.setValue(self.prev_second)
        self.auto_reset.setChecked(self.prev_auto_reset)
        self.vibrate.setChecked(self.prev_loop)
        self.sound_combobox.setCurrentIndex(self.prev_sound_option)

    def init_time(self):
        time_layout = QVBoxLayout()
        label_layout = QHBoxLayout()
        spinbox_layout = QHBoxLayout()
        time_layout.addLayout(label_layout)
        time_layout.addLayout(spinbox_layout)

        hour_label = self.create_spinbox_label('Hour')
        minute_label = self.create_spinbox_label('Minute')
        second_label = self.create_spinbox_label('Second')
        label_layout.addWidget(hour_label, alignment=Qt.AlignmentFlag.AlignLeft)
        label_layout.addWidget(minute_label, alignment=Qt.AlignmentFlag.AlignLeft)
        label_layout.addWidget(second_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.hour_box = self.create_spinbox()
        self.hour_box.setRange(0, 99)
        self.minute_box = self.create_spinbox()
        self.second_box = self.create_spinbox()
        spinbox_layout.addWidget(self.hour_box, alignment=Qt.AlignmentFlag.AlignLeft)
        spinbox_layout.addWidget(self.minute_box, alignment=Qt.AlignmentFlag.AlignLeft)
        spinbox_layout.addWidget(self.second_box, alignment=Qt.AlignmentFlag.AlignLeft)
        return time_layout

    def init_check_option(self):
        checkbox_layout = QVBoxLayout()
        self.auto_reset = QCheckBox(self)
        self.auto_reset.setText('Auto reset')
        self.vibrate = QCheckBox(self)
        self.vibrate.setText('Vibrate')
        self.sound_combobox = QComboBox(self)
        self.sound_combobox.addItem('No Sound')
        self.sound_combobox.addItem('Sound')
        self.sound_combobox.setFixedWidth(100)
        self.sound_combobox.currentTextChanged.connect(self.__combobox_changed_slot)
        self.prev_color = QColor(0, 0, 0)

        self.color_text_label = QLabel(self)
        self.color_text_label.setText('Color')
        self.color_text_label.setFixedSize(100, 12)
        self.color_label = QLabel(self)
        self.color_label.setObjectName('color_label')
        self.color_label.setFixedSize(100, 25)
        self.color_label.setStyleSheet("""
            #color_label{
                background-color: rgb(%d, %d, %d);
                border: 3px solid white;
            }
        """% (self.prev_color.red(), self.prev_color.green(), self.prev_color.blue()))
        self.color_label.mousePressEvent = self.__color_pick
        checkbox_layout.addWidget(self.auto_reset)
        checkbox_layout.addWidget(self.vibrate)
        checkbox_layout.addWidget(self.sound_combobox)
        checkbox_layout.addSpacing(10)
        checkbox_layout.addWidget(self.color_text_label)
        checkbox_layout.addWidget(self.color_label)
        return checkbox_layout

    def __color_pick(self, e):
        r, g, b, a = self.prev_color.getRgb()
        ir, ig, ib = self.color_picker.clampRGB(self.color_picker.getColor((r, g, b)))
        self.prev_color = QColor(int(ir), int(ig), int(ib))
        self.color_label.setStyleSheet("""
            #color_label{
                background-color: rgb(%f, %f, %f);
                border: 3px solid white;
            }
        """% (ir, ig, ib))

    def get_color(self):
        return self.prev_color

    def __combobox_changed_slot(self):
        self.sound_option = self.sound_combobox.currentIndex()

    def init_decision_button(self):
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 15)
        btn_layout.addStretch(4)
        self.ok_btn = QPushButton('OK', self)
        self.ok_btn.clicked.connect(self.__ok_slot)
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(self.__cancel_slot)
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(self.cancel_btn)
        return btn_layout

    def is_auto_reset_checked(self):
        return self.auto_reset.isChecked()

    def is_vibrate_checked(self):
        return self.vibrate.isChecked()

    def dark_mode(self):
        self.palette_dark = QPalette()
        self.palette_dark.setColor(QPalette.ColorRole.Window, QColor(31 , 31, 31))
        self.palette_dark.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        self.palette_dark.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        self.palette_dark.setColor(QPalette.ColorRole.AlternateBase, QColor(31, 31, 31))
        self.palette_dark.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        self.palette_dark.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        self.palette_dark.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.palette_dark.setColor(QPalette.ColorRole.Button, QColor(31, 31, 31))
        self.palette_dark.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        self.palette_dark.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        self.palette_dark.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        self.palette_dark.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        self.palette_dark.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        self.setPalette(self.palette_dark)

    def light_mode(self):
        self.setPalette(QApplication.palette())

    def create_spinbox(self):
        spinbox = QSpinBox(self)
        spinbox.setRange(0, 59)
        spinbox.setFixedSize(50, 40)
        f = spinbox.font()
        f.setPointSize(15)
        f.setBold(True)
        spinbox.setFont(f)
        spinbox.setStyle(MyStyle())
        # spinbox.setPalette(self.palette_dark)
        return spinbox
    
    def create_spinbox_label(self, txt):
        label = QLabel(txt, self)
        label.setFixedSize(50, 20)
        # label.setPalette(self.palette_dark)
        # label.setStyleSheet('background-color: #111111;')
        return label

    def set_time(self, h, m, s):
        self.hour_box.setValue(h)
        self.minute_box.setValue(m)
        self.second_box.setValue(s)
    
    def set_check_option(self, auto_reset, vibrate):
        self.auto_reset.setChecked(auto_reset)
        self.vibrate.setChecked(vibrate)
    
    def set_sound_option(self, sound_option):
        self.sound_combobox.setCurrentIndex(sound_option)

    def set_color_option(self, color: QColor):
        self.prev_color = color
        self.color_label.setStyleSheet("""
            #color_label{
                background-color: rgb(%f, %f, %f);
                border: 3px solid white;
            }
        """% (color.red(), color.green(), color.blue()))

    def __cancel_slot(self):
        self.res = self.RES_CANCEL
        self.close()
        self.__revert_data()

    def __ok_slot(self):
        self.res = self.RES_OK
        self.close()