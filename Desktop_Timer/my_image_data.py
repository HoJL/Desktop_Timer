from PyQt5.QtGui import QImage, QPixmap

class MyImage():

    close_svg = """<?xml version="1.0" ?><svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><defs><style>.cls-1{fill:none;stroke:#cccccc;stroke-linecap:round;stroke-linejoin:round;stroke-width:2px;}</style></defs><title/><g id="cross"><line class="cls-1" x1="7" x2="25" y1="7" y2="25"/><line class="cls-1" x1="7" x2="25" y1="25" y2="7"/></g></svg>
    """
    close_w_svg = """<?xml version="1.0" ?><svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><defs><style>.cls-1{fill:none;stroke:#ffffff;stroke-linecap:round;stroke-linejoin:round;stroke-width:2px;}</style></defs><title/><g id="cross"><line class="cls-1" x1="7" x2="25" y1="7" y2="25"/><line class="cls-1" x1="7" x2="25" y1="25" y2="7"/></g></svg>
    """
    menu_svg = """<?xml version="1.0" ?><svg fill="none" height="100" viewBox="0 0 24 24" width="100" xmlns="http://www.w3.org/2000/svg"><path d="M4 6H20M4 12H20M4 18H20" stroke="#cccccc" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/></svg>
    """
    play_svg = """<?xml version="1.0" ?><!DOCTYPE svg  PUBLIC '-//W3C//DTD SVG 1.1//EN'  'http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd'><svg height="512px" id="Layer_1" style="enable-background:new 0 0 512 512;" version="1.1" viewBox="0 0 512 512" width="512px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path fill="#cccccc" d="M405.2,232.9L126.8,67.2c-3.4-2-6.9-3.2-10.9-3.2c-10.9,0-19.8,9-19.8,20H96v344h0.1c0,11,8.9,20,19.8,20  c4.1,0,7.5-1.4,11.2-3.4l278.1-165.5c6.6-5.5,10.8-13.8,10.8-23.1C416,246.7,411.8,238.5,405.2,232.9z"/></svg>
    """
    pause_svg = """<?xml version="1.0" ?><svg height="512" viewBox="0 0 512 512" width="512" xmlns="http://www.w3.org/2000/svg"><title/><path fill="#cccccc" d="M208,432H160a16,16,0,0,1-16-16V96a16,16,0,0,1,16-16h48a16,16,0,0,1,16,16V416A16,16,0,0,1,208,432Z"/><path fill="#cccccc" d="M352,432H304a16,16,0,0,1-16-16V96a16,16,0,0,1,16-16h48a16,16,0,0,1,16,16V416A16,16,0,0,1,352,432Z"/></svg>
    """
    reset_svg = """<?xml version="1.0" ?><svg height="512px" viewBox="0 0 21 21" width="512px" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd" stroke="#cccccc" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" transform="matrix(0 1 1 0 2.5 2.5)"><path d="m3.98652376 1.07807068c-2.38377179 1.38514556-3.98652376 3.96636605-3.98652376 6.92192932 0 4.418278 3.581722 8 8 8s8-3.581722 8-8-3.581722-8-8-8"/><path d="m4 1v4h-4" transform="matrix(1 0 0 -1 0 6)"/></g></svg>
    """
    img_list = {'close': close_svg, 'menu': menu_svg, 'play': play_svg, 'pause': pause_svg, 'reset': reset_svg}
    def __init__(self) -> None:
        pass

    @staticmethod
    def __svg_to_pixmap(name):
        svg_bytearry = bytearray(MyImage.img_list[name], 'utf-8')
        img = QImage.fromData(svg_bytearry)
        return QPixmap.fromImage(img)

    @staticmethod
    def get_pixmap(name) -> QPixmap:
        pixmap = MyImage.__svg_to_pixmap(name)
        return pixmap
