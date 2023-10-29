from CONSTANTS import *
from libraries import *
from game import Game


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.init_window()
        self.initUI()

    def init_window(self):
        self.setGeometry(*win_cord, *win_size)
        self.setWindowTitle(win_title)
        self.setWindowIcon(QtGui.QIcon(win_icon))
        self.setObjectName("Window")
        self.setStyleSheet("#Window {background: #cfc; border-radius: 10px}")

    def lvl_button_clicked(self):
        btn = self.sender()
        print(int(btn.text().replace("LVL-", "")))

        self.GameApp = Game(int(btn.text().replace("LVL-", "")))
        self.GameApp.show()
        self.hide()

    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("Oбнаружена ошибка !:", tb)
        with open(file="erors.log", mode="a") as erors:
            erors.write(str(datetime.datetime.now()) + "\n")
            erors.write(str("\t" + tb).replace("\n", "\n\t")[:-1])

    #    QtWidgets.QApplication.quit()             # !!! если вы хотите, чтобы событие завершилось

    sys.excepthook = excepthook

    def initUI(self):
        self.buttons = QGridLayout(self)
        self.lvl_layout = QGridLayout(self)
        self.buttons_lvl = dict()
        self.setCursor(Qt.PointingHandCursor)
        for i_y in range(3):
            for i_x in range(10):
                self.buttons_lvl[(i_y, i_x)] = QPushButton(text=f"LVL-{(i_y * 10 + i_x) + 1}", parent=self)
                self.buttons_lvl[(i_y, i_x)].x = i_x
                self.buttons_lvl[(i_y, i_x)].y = i_y
                self.buttons_lvl[(i_y, i_x)].clicked.connect(lambda: self.lvl_button_clicked())
                self.lvl_layout.addWidget(self.buttons_lvl[i_y, i_x], i_y, i_x)
        print(self.buttons_lvl)
        self.two_player_game_layout = QGridLayout(self)
        self.buttons.addLayout(self.lvl_layout, 0, 0)
        self.buttons.addLayout(self.two_player_game_layout, 1, 0)
        self.bl_game = QPushButton("Играть по Bluetooth", self)
        self.two_player_game_layout.addWidget(self.bl_game, 0, 0)
        self.en_game = QPushButton("Играть по интернету", self)
        self.two_player_game_layout.addWidget(self.en_game, 0, 1)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = App()

    game.show()
    sys.exit(app.exec())
