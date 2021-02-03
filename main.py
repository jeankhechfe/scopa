# Scopa rules can be found here https://en.wikipedia.org/wiki/Scopa
import sys
import uipyqt
import scopa
from PyQt5.QtWidgets import *


def run_game_with_form():
    app = QApplication(sys.argv)
    sc = scopa.Scopa()
    ex = uipyqt.ScopaForm(sc)

    ex.prepare_for_my_move()
    ex.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    run_game_with_form()
