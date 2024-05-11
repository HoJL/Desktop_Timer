import sys
from pathlib import Path
from PyQt5.QtCore import QEvent, Qt, QPoint, QTimer, QUrl, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QSettings, QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont, QFontDatabase, QMouseEvent, QPalette, QColor, QCloseEvent, QKeyEvent, QIcon
from PyQt5.QtMultimedia import QSoundEffect
from my_titlebar import MyTitleBar
from setting_widget import SettingDialog

class MainWindow(QMainWindow):

    WIN_W = 300
    WIN_H = 100

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.__init_font()
        self.setWindowTitle('Desktop Timer')
        self.title_bar = MyTitleBar(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint| Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(self.WIN_W, self.WIN_H)
        self.setting = None
        self.zero_str = '00:00:00'
        self.timeer_label = QLabel(self.zero_str, self)
        self.timeer_label.setObjectName('time')
        self.timeer_label.setStyleSheet('#time{background-color: rgba(0, 0, 0, 2);}')
        self.timeer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.change_font(self.font_list[0])
        widget = QWidget(self)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.title_bar)
        layout.addWidget(self.timeer_label)
        self.setCentralWidget(widget)
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        menu = self.menuBar()
        menu.setNativeMenuBar(True)

        self.title_bar.menu_btn.clicked.connect(self.__setting_popup)
        self.title_bar.hide()
        self.is_play = False
        self.title_bar.play_btn.clicked.connect(self.__play_and_pause)
        self.title_bar.reset_btn.clicked.connect(self.__reset_slot)

        self.auto_reset = False
        self.vibrate = False
        self.pressed = False

        self.elapsed_time = 0
        self.remain_time = 0
        self.defalut_time = 0
        self.prev_sec = 0
        self.sound_option = 0
        self.cur_color = QColor(0, 0, 0)
        self.timer = QTimer(self)
        self.timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.timer.setInterval(16)
        self.interval = self.timer.interval()
        self.timer.timeout.connect(self.__timer_slot)

        self.alarm_sound = QSoundEffect(self)
        base = Path(__file__).resolve().parent.__str__()
        self.alarm_sound.setSource(QUrl.fromLocalFile(base + '/alarm1.wav'))
        self.alarm_sound.setLoopCount(4)

        self.__init_animation()
        self.show()
        self.__load()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.__save()

    def keyPressEvent(self, e: QKeyEvent):
        if e.modifiers() & Qt.Modifier.SHIFT:
            if e.key() == Qt.Key.Key_C:
                self.__move_center()

    def __save(self):
        qs = QSettings(self.windowTitle() + '.ini', QSettings.Format.IniFormat)
        qs.setValue('Window/pos', self.pos())
        qs.setValue('Option/time', self.__get_time_at_setting())
        qs.setValue('Option/auto_reset', self.__is_auto_reset_checked())
        qs.setValue('Option/vibrate', self.__is_vibrate_checked())
        qs.setValue('Option/sound', self.__get_sound_option())
        color = self.__get_cur_color()
        qs.setValue('Option/color', color)

    def __load(self):
        qs = QSettings(self.windowTitle() + '.ini', QSettings.Format.IniFormat)
        pos = qs.value('Window/pos')
        if pos is None:
            return
        h, m, s = qs.value('Option/time')
        auto_reset = qs.value('Option/auto_reset', type=bool)
        vibrate = qs.value('Option/vibrate', type=bool)
        sound = qs.value('Option/sound', type=int)
        color = qs.value('Option/color')
        self.move(pos)
        self.setting = SettingDialog(self)
        self.setting.set_time(h, m, s)
        self.setting.set_check_option(auto_reset, vibrate)
        self.setting.set_sound_option(sound)
        self.setting.set_color_option(color)

        self.__update_setting(h, m, s, auto_reset, vibrate, sound, color)

    def __move_center(self):
        fg = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

    def __init_animation(self):
        duration = 50
        x = self.timeer_label.x()
        self.anim = QPropertyAnimation(self.timeer_label, b"pos")
        self.anim.setEasingCurve(QEasingCurve.Type.InOutBounce)
        self.anim.setEndValue(QPoint( x+ 2, self.timeer_label.y()))
        self.anim.setDuration(duration)

        self.anim2 = QPropertyAnimation(self.timeer_label, b"pos")
        self.anim2.setEasingCurve(QEasingCurve.Type.InOutBounce)
        self.anim2.setEndValue(QPoint(x, self.timeer_label.y()))
        self.anim2.setDuration(duration)

        self.anim3 = QPropertyAnimation(self.timeer_label, b"pos")
        self.anim3.setEasingCurve(QEasingCurve.Type.InOutBounce)
        self.anim3.setEndValue(QPoint(x -2, self.timeer_label.y()))
        self.anim3.setDuration(duration)

        self.anim4 = QPropertyAnimation(self.timeer_label, b"pos")
        self.anim4.setEasingCurve(QEasingCurve.Type.InOutBounce)
        self.anim4.setEndValue(QPoint(x, self.timeer_label.y()))
        self.anim4.setDuration(duration)

        self.anim_group = QSequentialAnimationGroup()
        self.anim_group.addAnimation(self.anim)
        self.anim_group.addAnimation(self.anim2)
        self.anim_group.addAnimation(self.anim3)
        self.anim_group.addAnimation(self.anim4)
        self.anim_group.setLoopCount(40)

    def __reset_timer(self):
        self.timer.stop()
        self.remain_time = self.defalut_time
        self.is_play = False
        self.title_bar.change_play_pix(self.is_play)
        h, m, s = self.__get_time_at_setting()
        self.__set_timer_label_text(h, m, s)
        self.update()
    
    def __reset_slot(self):
        self.__stop_end_effect()
        self.__reset_timer()

    def __stop_vibrate(self):
        self.anim_group.stop()

    def __stop_sound(self):
        self.alarm_sound.stop()

    def __stop_end_effect(self):
        self.__stop_sound()
        self.__stop_vibrate()

    def __timer_slot(self):
        self.elapsed_time += self.interval
        self.remain_time -= self.interval
        if self.remain_time <= 0:
            self.__timer_end()
            return
        sec = self.remain_time // 1000
        if self.prev_sec == sec:
            return
        time_str = self.__time_format(sec)
        self.prev_sec = sec
        self.timeer_label.setText(time_str)

    def __time_format(self, time):
        m, s = divmod(time, 60)
        time_str = '00:{:02d}:{:02d}'.format(m, s)
        if (m > 60):
            h, m = divmod(m, 60)
            time_str = '{:02d}:{:02d}:{:02d}'.format(h, m, s)

        return time_str

    def __set_remain_time(self, h: int, m: int, s: int):
        total_sec = (h * 60 * 60) + (m * 60) + s
        self.remain_time = total_sec * 1000
        self.defalut_time = self.remain_time

    def __play_and_pause(self):
        if self.remain_time <= 0:
            return
        self.__stop_end_effect()
        if self.is_play is True:
            self.timer.stop()
            print(self.remain_time / 1000.0)
            self.is_play = False
        else:
            self.timer.start()
            self.is_play = True

        self.title_bar.change_play_pix(self.is_play)

    def __timer_end(self):
        self.__reset_timer()
        if self.vibrate is True:
            self.anim_group.start()
        if self.auto_reset is False:
            self.timeer_label.setText(self.zero_str)
            self.remain_time = 0
        if self.sound_option == 1:
            self.alarm_sound.play()

    def __init_font(self):
        self.fontDB = QFontDatabase()
        self.font_list = list()
        base = Path(__file__).resolve().parent.__str__()
        
        self.__add_font_data(base + '/font/7segment.ttf')
        self.__add_font_data(base + '/font/HakgyoansimBareondotumB.ttf')
        self.__add_font_data(base + '/font/ChangwonDangamAsac-Bold.ttf')
        self.__add_font_data(base + '/font/PyeongChangPeace-Bold.ttf')
        self.__add_font_data(base + '/font/DNFBitBitv2.ttf')

    def __add_font_data(self, name):
        id = self.fontDB.addApplicationFont(name)
        fm = QFontDatabase.applicationFontFamilies(id)
        self.font_list.append(fm[0])

    def change_font(self, font_name):
        font = QFont(font_name, 60)
        self.timeer_label.setFont(font)
        w = self.timeer_label.fontMetrics().boundingRect(self.timeer_label.text()).width()

        ratio = (self.WIN_W - 15) / w
        stretch = 100 * ratio
        font = self.timeer_label.font()
        font.setStretch(int(stretch))
        self.timeer_label.setFont(font)

    def change_color(self):
        self.p = QPalette()
        self.p.setColor(QPalette.ColorRole.WindowText, self.cur_color)
        self.timeer_label.setPalette(self.p)
        self.update()

    def __calibrate_pos(self, y):
        point: QPoint = self.anim.endValue()
        point2: QPoint = self.anim2.endValue()
        point3: QPoint = self.anim3.endValue()
        point4: QPoint = self.anim4.endValue()
        self.anim.setEndValue(QPoint(point.x(), y))
        self.anim2.setEndValue(QPoint(point2.x(), y))
        self.anim3.setEndValue(QPoint(point3.x(), y))
        self.anim4.setEndValue(QPoint(point4.x(), y))

    def enterEvent(self, a0: QEvent | None) -> None:
        self.title_bar.show()
        self.__calibrate_pos(self.timeer_label.y())
        self.update()

    def leaveEvent(self, a0: QEvent | None) -> None:
        self.title_bar.hide()
        self.pressed = False
        self.__calibrate_pos(0)
        self.update()

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        self.pressed = True
        self.oldPos = event.globalPos()
    
    def mouseMoveEvent(self, event: QMouseEvent | None):
        if self.pressed is False:
            return
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    
    def mouseReleaseEvent(self, a0: QMouseEvent | None) -> None:
        self.pressed = False
    
    def __setting_popup(self):
        self.__reset_timer()
        if self.setting is None:
            self.setting = SettingDialog(self)
        self.__stop_end_effect()
        self.setting.exec_()
        if self.setting.res == self.setting.RES_OK:
            hour, min, sec = self.__get_time_at_setting()
            # self.__set_timer_label_text(hour, min, sec)
            # self.__set_remain_time(hour, min, sec)
            # self.auto_reset = self.__is_auto_reset_checked()
            # self.vibrate = self.__is_vibrate_checked()
            # # self.prev_sec = self.defalut_time // 1000
            # self.sound_option = self.__get_sound_option()
            # self.cur_color = self.__get_cur_color()
            # self.change_color()
            self.__update_setting(hour, min, sec,
                self.__is_auto_reset_checked(), self.__is_vibrate_checked(),
                self.__get_sound_option(), self.__get_cur_color())

    def __update_setting(self, hour, min, sec, auto_reset, vibrate, sound_opt, color):
        self.__set_timer_label_text(hour, min, sec)
        self.__set_remain_time(hour, min, sec)
        self.auto_reset = auto_reset
        self.vibrate = vibrate
        # self.prev_sec = self.defalut_time // 1000
        self.sound_option = sound_opt
        self.cur_color = color
        self.change_color()


    def __set_timer_label_text(self, h, m, s):
        time = '{:02d}:{:02d}:{:02d}'.format(h, m, s)
        self.timeer_label.setText(time)
    
    def __get_time_at_setting(self):
        if self.setting is None:
            return 0, 0, 0
        hour = self.setting.hour_box.value()
        min = self.setting.minute_box.value()
        sec = self.setting.second_box.value()
        return hour, min, sec
    
    def __is_auto_reset_checked(self):
        if self.setting is None:
            return False
        return self.setting.is_auto_reset_checked()

    def __is_vibrate_checked(self):
        if self.setting is None:
            return False
        return self.setting.is_vibrate_checked()
    
    def __get_sound_option(self):
        if self.setting is None:
            return 0
        return self.setting.sound_combobox.currentIndex()
    
    def __get_cur_color(self):
        if self.setting is None:
            return QColor(0, 0, 0)
        return self.setting.get_color()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ico = Path(__file__).resolve().parent.__str__() + '/timer.ico'
    app_icon = QIcon()
    app_icon.addFile(ico, QSize(16,16))
    app_icon.addFile(ico, QSize(24,24))
    app_icon.addFile(ico, QSize(32,32))
    app_icon.addFile(ico, QSize(48,48))
    app_icon.addFile(ico, QSize(256,256))
    app.setWindowIcon(app_icon)
    main = MainWindow()
    sys.exit(app.exec_())
