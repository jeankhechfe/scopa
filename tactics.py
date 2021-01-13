denaro = "*"
settebello_symbol = "07"+denaro
lay_card_button_name = "Put Card"
claim_cards_button_name = "Collect Cards"
opponent_hand_frame_name = "Opponent's hand"
actions_frame_name = "Actions"
my_hand_frame_name = "My Hand"
table_frame_name = "Table"
this_was_scopa = "It was a Scopa!"

settebello_factor = 5
card_factor = 1
seven_factor = 5
denar_factor = 2
scopa_factor = 10
leaving_single_card_factor = -3
leaving_two_cards_factor = -1


def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]


# returns the list of all possible sums of table, along with cards that are part of this combinat
# but only if the sum is possible to be taken
def all_takes_with_sum(s):
    # store all the sublists
    ps = powerset(s)
    takes_with_sum = []

    for cset in ps:
        take_sum = sum_of_cards(cset)
        # if the sum is equal or smaller than threshold, append it -
        # in scopa sums between 8 and 10 as well as anything over 13 is not a valid take
        if (1 <= take_sum <= 7) or (11 <= take_sum <= 13):
            takes_with_sum.append([take_sum, cset])

    return takes_with_sum


# returns the sum of cards in a list
def sum_of_cards(clist):
    val = 0
    for i in range(0, len(clist)):
        card_val = clist[i][:2]
        val = val + int(card_val)
    return val


# return true if settebello
def settebello(cards):
    for card in cards:
        if card == settebello_symbol:
            return True
    return False


# returns count of sevens
def sevens(cards):
    sevens_count = 0
    for card in cards:
        if card[1] == "7":
            sevens_count += 1
    return sevens_count


# returns count of denars
def denars(cards):
    denars_count = 0
    for card in cards:
        if card[2] == denaro:
            denars_count += 1
    return denars_count


def get_score_for_take(take, table):
    score = len(take[1]*card_factor)
    if take[0] == "07D" or settebello(take[1]):
        score += settebello_factor
    if take[0][2] == denaro:
        score += denar_factor
    score += (denars(take[1]) * denar_factor)
    if take[0][1] == "7":
        score += seven_factor
    score += (sevens(take[1]) * seven_factor)
    if len(take[1]) == len(table):
        score += scopa_factor
    if len(take[1])+2 == len(table):
        score += leaving_two_cards_factor
    if len(take[1])+1 == len(table):
        score += leaving_single_card_factor

    return score


def select_card_to_be_dropped(hand, table):
    # drop the lowest
    lowest = hand[0]
    for i in range(1, len(hand)):
        if int(lowest[:1]) > int(hand[i][:1]):
            lowest = hand[i]
    return lowest
