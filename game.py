import copy
from dataclasses import dataclass

from CONSTANTS import *
from libraries import *

@dataclass()
class User:
    name: str
    lvl_max: int
    lvl_session: int


class Game(QWidget):
    def __init__(self, lvl):
        super().__init__()
        self.pazle_list = None
        self.lvl = lvl
        self.init_window()
        self.initUI()
        self.create_connection("lvls.db")
        self.create_pazzle()

    def pil_to_qPixmap(self, pil_image):
        image_data = pil_image.convert("RGBA").tobytes("raw", "RGBA")
        qImage = QtGui.QImage(image_data, pil_image.size[0], pil_image.size[1], QtGui.QImage.Format_RGBA8888)
        qPixmap = QtGui.QPixmap.fromImage(qImage)
        return qPixmap

    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
            self.cur = connection.cursor()
            res = self.cur.execute("SELECT * FROM lvls")
        except Error as e:
            with open(file="erors.log", mode="a") as erors:
                erors.write(str(datetime.datetime.now()) + "\n\t" + "Lose connection to DB:" + str(e))
            print(f"The error '{e}' occurred")

        return connection

    def enter_event_for_fragment(self, event):
        mouse_pos = event.pos()
        for i in self.pazle_list:
            if mouse_pos.x in range(*i.ranges[:2]) and mouse_pos.y in range(*i.ranges[2:]):
                print(i)
            print(mouse_pos)

    def pazle_fragment(self):
        print(self.sender().ranges)

    def create_pazzle(self):
        promts = "0, 0, 500, 500 ; 500, 0, 1000, 500 ; 1000, 0, 1500, 500 ; 0 , 500, 500, 1000 ; 500, 500, 1000, 1000"
        filename = self.cur.execute("SELECT * FROM lvls WHERE num = 1").fetchall()[0][1] + ".jpg"
        with Image.open(filename) as img:
            self.window().setGeometry(500, 50, *img.size)
            self.pazle_list = list()
            s = 0
            self.pazle_group_box = QButtonGroup()
            for i in promts.split(" ; "):
                i1 = [int(i_k) for i_k in i.split(', ')]


                i_im = QPushButton(self)
                i_im.clicked.connect(self.pazle_fragment)
                icon = QIcon()
                pixmap = self.pil_to_qPixmap(img.crop([int(i_k) for i_k in i.split(', ')]))
                icon.addPixmap(pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
                i_im.setIcon(icon)
                i_im.setIconSize(QSize(abs(i1[0] - i1[2]), abs(i1[1] - i1[3])))
                i_im.setGeometry(i1[0], i1[1], abs(i1[0] - i1[2]), abs(i1[1] - i1[3]))
                self.pazle_list.append(i_im)
                self.pazle_list[s].ranges = [int(i_k) for i_k in i.split(', ')]
                print(*i1[:2], abs(i1[0] - i1[2]), abs(i1[1] - i1[3]))
                print([int(i_k) for i_k in i.split(', ')])
                self.enterEvent = self.enter_event_for_fragment
                self.pazle_group_box.addButton(i_im)
                s += 1


    def init_window(self):
        self.setGeometry(*win_cord, *win_size)
        self.setWindowTitle(win_title)
        self.setWindowIcon(QtGui.QIcon(win_icon))
        self.setObjectName("Window2")
        self.setStyleSheet("#Window2 {background: #cfc; border-radius: 10px}")

    def initUI(self):
        pass