# Scopa rules can be found here https://en.wikipedia.org/wiki/Scopa
import sys
import uipyqt
import scopa
from PyQt5.QtWidgets import *

# this is the main game loop
"""
def run_game():
    while sum_of_all_cards_in_game() != 0:
        for h in range(0, no_of_players):
            play_hand(h)
            # print_status()
            # check_sum_of_cards()

    # if any cards were left on the table, get them to the last person taking cards from the table
    for card in table.copy():
        piles[last_hand_played].append(card)
        table.remove(card)

    print_game_results()
"""


def run_game_with_form():
    app = QApplication(sys.argv)
    sc = scopa.Scopa()
    ex = uipyqt.ScopaForm(sc)

    ex.prepare_for_my_move()
    ex.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    run_game_with_form()

    # print_status()
    # run_game()
