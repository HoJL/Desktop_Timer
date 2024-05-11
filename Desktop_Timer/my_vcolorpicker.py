from PyQt5.QtGui import QMouseEvent
import vcolorpicker
from vcolorpicker import ColorPicker

class MyColorPicker(ColorPicker):

    def __init__(self, lightTheme: bool = False, useAlpha: bool = False):
        super().__init__(lightTheme, useAlpha)
        self.ui.lastcolor_vis.mousePressEvent = self.setLastColor
        
    def getColor(self, lc: tuple = None):
        if lc != None and self.usingAlpha:
            alpha = lc[3]
            lc = lc[:3]
            self.setAlpha(alpha)
            self.alpha = alpha
        if lc == None: lc = self.lastcolor
        else: self.lastcolor = lc

        self.setRGB(lc)
        self.rgbChanged()
        r,g,b = lc
        self.prev_r = r
        self.prev_g = g
        self.prev_b = b
        self.ui.lastcolor_vis.setStyleSheet(f"background-color: rgb({r},{g},{b});")
        if self.exec_():
            r, g, b = vcolorpicker.hsv2rgb(self.color)
            self.lastcolor = (r,g,b)
            if self.usingAlpha: return (r,g,b,self.alpha)
            return (r,g,b)
        else:
            return self.lastcolor

    def setLastColor(self, a0: QMouseEvent | None) -> None:
        r = self.prev_r
        g = self.prev_g
        b = self.prev_b
        self.setRGB((r, g, b))
        self.color = vcolorpicker.rgb2hsv(r,g,b)
        self.setHSV(self.color)
        self.setHex(vcolorpicker.rgb2hex((r,g,b)))
        self.ui.color_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")