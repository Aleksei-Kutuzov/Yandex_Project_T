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

    def create_pazzle(self):
        promts = "0, 0, 170, 480 ; 170, 0, 500, 480"
        filename = self.cur.execute("SELECT * FROM lvls WHERE num = 1").fetchall()[0][1] + ".jpg"
        with Image.open(filename) as img:
            self.pazle_list = list()
            s = 0
            for i in promts.split(" ; "):
                i1 = [int(i_k) for i_k in i.split(', ')]
                self.pix = QtGui.QPixmap(img.crop([int(i_k) for i_k in i.split(', ')]))

                i_im = QLabel(self)
                i_im.setGeometry(i1[0], i1[1], abs(i1[0] - i1[2]), abs(i1[1] - i1[3]))
                i_im.setPixmap(self.pix)
                self.pazle_list.append(i_im)
                print(*i1[:2], abs(i1[0] - i1[2]), abs(i1[1] - i1[3]))
                print([int(i_k) for i_k in i.split(', ')])

                s += 1


    def init_window(self):
        self.setGeometry(*win_cord, *win_size)
        self.setWindowTitle(win_title)
        self.setWindowIcon(QtGui.QIcon(win_icon))
        self.setObjectName("Window2")
        self.setStyleSheet("#Window2 {background: #cfc; border-radius: 10px}")

    def initUI(self):
        pass