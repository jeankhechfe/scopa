import random
import tactics

# all possible colors: Denari, Bastoni, Spade, Coppe
colors = [tactics.denaro, " ", " ", " "]
hand_size = 3
initial_table_size = 4
no_of_players = 2
no_take = -99


class Scopa:
    deck = []
    hands = []
    piles = []
    table = []
    scopa_count = []
    points = []
    last_hand_played = -1

    def __init__(self):
        self.generate_deck()
        self.initiate_play()

    def generate_deck(self):
        all_cards = []
        for color in colors:
            for i in range(1, 8):
                card = "0" + str(i) + color
                all_cards.append(card)
            for j in range(11, 14):
                card = str(j) + color
                all_cards.append(card)
        self.deck = []
        while len(all_cards) > 0:
            pos = random.randint(0, len(all_cards) - 1)
            random_card = all_cards[pos]
            all_cards.remove(random_card)
            self.deck.append(random_card)
        print(self.deck)

    # create table, hands, piles and scopa count
    def initiate_play(self):
        for i in range(0, initial_table_size):
            self.table.append(self.deck.pop())
        for p in range(0, no_of_players):
            hand = []
            self.draw_hand(hand)
            self.hands.append(hand)
            self.scopa_count.append(0)
            self.piles.append([])

    # draw cards from deck to hand, return False if hand is empty
    def draw_hand(self, hand):
        if len(self.deck) == 0:
            return False
        for c in range(0, hand_size):
            hand.append(self.deck.pop())
        return True

    def print_game_results(self):
        print("Scopas: " + str(self.scopa_count))
        for s in range(0, no_of_players):
            pile_score = self.calculate_score(s)
            print("Score for hand " + str(s) + ", cards " + str(len(self.piles[s])) + " ("
                  + str(self.piles[s]) + ") is " + str(pile_score))

    def print_status(self):
        print("===========")
        print("Table:")
        print(self.table)
        print("Hands")
        print(self.hands)
        print("Deck")
        print(self.deck)
        print("Scopas")
        print(self.scopa_count)
        for pile in self.piles:
            print("Pile size: "+str(len(pile))+", content: "+str(pile))
        print("===========\n")

    def check_sum_of_cards(self):
        csum = len(self.table)
        csum += len(self.deck)
        for hand in self.hands:
            csum += len(hand)
        for pile in self.piles:
            csum += len(pile)
        if csum != 40:
            print("Sum is "+str(sum)+" instead of 40")
            exit(1)

    # returns possible takes - each item in the list is a couple: card from hand, cards to be taken
    def possible_takes(self, hand):
        takes_with_sum = tactics.all_takes_with_sum(self.table)
        filtered_takes = []
        for take in takes_with_sum:
            for card in hand:
                take_sum = take[0]
                card_value = int(card[:2])
                if card_value == take_sum:
                    # build list where each item is a list: card from hand, cards to be taken
                    filtered_takes.append([card, take[1]])
        return filtered_takes

    # return sum of cards in hands and deck
    def sum_of_all_cards_in_game(self):
        csum = 0
        csum += len(self.deck)
        for hand in self.hands:
            csum += len(hand)
        return csum

    # draw hand if necessary, return True is game should be ended
    def draw_hand_if_necessary(self, hand_no):
        if len(self.hands[hand_no]) == 0:
            more_cards = self.draw_hand(self.hands[hand_no])
            return not more_cards
        return False

    def get_potential_takes(self, hand_number):
        return self.possible_takes(self.hands[hand_number])

    def get_best_take(self, hand_number, potential_takes):
        best_take_score = -1
        best_take_index = no_take
        for t in range(0, len(potential_takes)):
            # remember the last hand played
            self.last_hand_played = hand_number
            # check what is the score
            current_take_score = tactics.get_score_for_take(potential_takes[t], self.table)
            if current_take_score > best_take_score:
                best_take_index = t
                best_take_score = current_take_score
        return best_take_index

    def drop_a_card(self, hand_number):
        card_to_be_dropped = tactics.select_card_to_be_dropped(self.hands[hand_number], self.table)
        self.hands[hand_number].remove(card_to_be_dropped)
        self.table.append(card_to_be_dropped)
        return card_to_be_dropped

    def remove_card_from_hand_and_table(self, potential_takes, hand_number, best_take_index):
        card_from_hand = potential_takes[best_take_index][0]
        self.hands[hand_number].remove(card_from_hand)
        self.piles[hand_number].append(card_from_hand)
        for card in potential_takes[best_take_index][1]:
            self.table.remove(card)
            self.piles[hand_number].append(card)
        # if no cards left on the table, increase scopa count
        if len(self.table) == 0 and not len(self.deck) == 0:
            self.scopa_count[hand_number] += 1

    # this function plays single hand with hand number
    def play_hand(self, hand_number):
        if len(self.hands[hand_number]) == 0:
            self.draw_hand(self.hands[hand_number])
        potential_takes = self.get_potential_takes(hand_number)
        best_take_index = self.get_best_take(hand_number, potential_takes)
        if best_take_index != no_take:
            self.remove_card_from_hand_and_table(potential_takes, hand_number, best_take_index)
            return potential_takes[best_take_index]
        else:
            # no cards can be taken, drop a card
            return [self.drop_a_card(hand_number), []]

    def has_sevens(self, pile_number):
        more_sevens = True
        no_of_sevens = tactics.sevens(self.piles[pile_number])
        for i in range(0, len(self.piles)):
            if i != pile_number:
                more_sevens = tactics.sevens(self.piles[i]) <= no_of_sevens
        return more_sevens

    def has_card(self, pile_number):
        more_cards = True
        no_of_cards = len(self.piles[pile_number])
        for i in range(0, len(self.piles)):
            if i != pile_number:
                more_cards = len(self.piles[i]) <= no_of_cards
        return more_cards

    def has_denars(self, pile_number):
        more_denars = True
        no_of_denars = tactics.denars(self.piles[pile_number])
        for i in range(0, len(self.piles)):
            if i != pile_number:
                more_denars = tactics.denars(self.piles[i]) <= no_of_denars
        return more_denars

    # this function calculates results of a pile with given number
    def calculate_score(self, pile_number):
        score = 0
        if tactics.settebello(self.piles[pile_number]):
            score += 1
        if self.has_sevens(pile_number):
            score += 1
        if self.has_card(pile_number):
            score += 1
        if self.has_denars(pile_number):
            score += 1
        score += self.scopa_count[pile_number]
        return score
