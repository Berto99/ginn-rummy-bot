import random
from copy import deepcopy
from typing import List, Any, Union

card_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
card_suites = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
deck = []
cards_cpy = deepcopy(deck)
hand = []
in_combination = []
not_in_combination = [0]
cards_passed = []

# Card deck building
for i in card_suites:
    for j in card_numbers:
        deck.append([i, j])

# Random hand distributing
i = 0
while i < 10:
    candidate = random.choice(deck)
    if candidate not in hand:
        hand.append(candidate)
        deck.remove(candidate)
        i += 1

# Concrete hand distributing (Debug)
"""hand = [['Clubs', 2], ['Clubs', 8], ['Clubs', 1], ['Spades', 4], ['Spades', 3], ['Clubs', 3], ['Hearts', 3], ['Diamonds', 3], ['Hearts', 8], ['Diamonds', 8]]
for cardh in hand:
    deck.remove(cardh)"""


# Upon creating combination, scan the entire hand for cards to add to that combination
def combination_morph(combination, virt_hand):
    index = 1
    while index < len(combination):
        card = combination[index]
        index_comp = 0
        while index_comp < len(virt_hand):
            comp_card = virt_hand[index_comp]
            if combination[0] == 1:
                if card[0] == comp_card[0]:
                    if abs(card[1] - comp_card[1]) <= 1:
                        combination.append(comp_card)
                        virt_hand.remove(comp_card)
                        index_comp -= 1
            if combination[0] == 2:
                if card[1] == comp_card[1]:
                    combination.append(comp_card)
                    virt_hand.remove(comp_card)
                    index_comp -= 1
            index_comp += 1
        index += 1
    return [len(combination), combination]


# Calculate the chance that the next card will be 'valuable' to the player
def chance(in_combination_local):
    chance = 0
    for c in in_combination_local:
        c1 = deepcopy(c)
        if c1[0] == 1:
            c1.remove(c1[0])
            card_in_hand = False
            max_card = max(c1, key=lambda x: x[1])
            min_card = min(c1, key=lambda x: x[1])
            if max_card[1] < 13:
                for comb in in_combination_local:
                    if [c1[0][0], max_card[1] + 1] in comb or [c1[0][0], max_card[1] + 1] in cards_passed:
                        card_in_hand = True
                        break
                if not card_in_hand:
                    chance += 1/len(deck)
            card_in_hand = False
            if min_card[1] > 1:
                for comb in in_combination_local:
                    if [c1[0][0], min_card[1] - 1] in comb or [c1[0][0], min_card[1] - 1] in cards_passed:
                        card_in_hand = True
                        break
                if not card_in_hand:
                    chance += 1/len(deck)
        if c1[0] == 2:
            c1.remove(c1[0])
            card_in_hand = False
            suites_cpy = deepcopy(card_suites)
            for card_s in c1:
                suites_cpy.remove(card_s[0])
            for comb in in_combination_local:
                if comb[0] == 1:
                    for a in range(1, len(comb)):
                        card = comb[a]
                        if card in cards_passed:
                            card_in_hand = True
                            break
                        elif card[0] in suites_cpy:
                            if card[1] == c1[0][1]:
                                card_in_hand = True
                                break
            if not card_in_hand:
                chance += (1/len(deck)) * len(suites_cpy)
    return chance * 100


# Sort the cards into card combinations - Sequential or Identical
def configure(hand_given):
    virtual_hand = deepcopy(hand_given)
    current_card = []
    in_combination_local = []
    not_in_combination_local = [0]
    while 1:

        if len(virtual_hand) > 0:
            current_card = virtual_hand[0]
        else:
            break
        added = False
        virtual_hand.remove(current_card)

        # Combination[0] codes:
        # 1 - Sequential combination
        # 2 - Identical combination
        # 0 - Not in combination

        seq_hand = deepcopy(virtual_hand)
        ident_hand = deepcopy(virtual_hand)
        new_combination_seq = [1]
        new_combination_ident = [2]
        length_seq = 0
        length_ident = 0

        # Creating new seq. combination (if possible)
        for comparing_card in seq_hand:
            if current_card[0] == comparing_card[0]:
                if abs(current_card[1] - comparing_card[1]) <= 1:
                    seq_hand.remove(comparing_card)
                    new_combination_seq.append(current_card)
                    new_combination_seq.append(comparing_card)
                    combination_morph(new_combination_seq, seq_hand)
                    length_seq = len(new_combination_seq)

                    # Code that checks a copy of our combinations for the comparing_card, and if it has better options, it is included in them, instead of with the current_card
                    other_combination = [2, comparing_card]
                    if combination_morph(deepcopy(other_combination), deepcopy(seq_hand))[0] > length_seq:
                        new_combination_seq = combination_morph(other_combination, seq_hand)[1]
                        seq_hand.insert(0, current_card)
                    same_elem = []
                    for elem in new_combination_seq:
                        if elem in new_combination_ident:
                            same_elem = elem
                            break
                    if length_seq > 4 and length_seq > length_ident > 2 and same_elem is not None:
                        new_combination_seq.remove(same_elem)
                        length_seq -= 1
                    added = True
                    break
        # Creating new identical combination (if possible)
        for comparing_card_i in ident_hand:
            if current_card[1] == comparing_card_i[1]:
                ident_hand.remove(comparing_card_i)
                new_combination_ident.append(current_card)
                new_combination_ident.append(comparing_card_i)
                combination_morph(new_combination_ident, ident_hand)
                length_ident = len(new_combination_ident)
                # Code that checks a copy of our combinations for the comparing_card, and if it has better options, it is included in them, instead of with the current_card
                other_combination = [1, comparing_card_i]
                if combination_morph(deepcopy(other_combination), deepcopy(ident_hand))[0] > length_ident:
                    new_combination_ident = combination_morph(other_combination, ident_hand)[1]
                    ident_hand.insert(0, current_card)
                same_elem = []
                for elem in new_combination_ident:
                    if elem in new_combination_seq:
                        same_elem = elem
                        break
                if length_ident == 5 and length_ident > length_seq > 2 and same_elem is not None:
                    new_combination_ident.remove(same_elem)
                    length_ident -= 1

                added = True
                break
        if added:
            if length_seq >= length_ident:
                in_combination_local.append(new_combination_seq)
                virtual_hand = seq_hand
            else:
                in_combination_local.append(new_combination_ident)
                virtual_hand = ident_hand

        if not added:
            not_in_combination_local.append(current_card)

    new_hand = [in_combination_local, not_in_combination_local, chance(in_combination_local)]
    return new_hand


def is_card_good(b, lowest_sum, new_chance):
    new_hand = deepcopy(hand)
    new_hand.insert(new_hand.index(b), random_card)
    new_hand.remove(b)
    left_sum_new = sum(s[1] for s in configure(new_hand)[1][1:])
    dual_sum_new = 0
    for v in configure(new_hand)[0]:
        if len(v) == 3:
            for s in v[1:]:
                dual_sum_new += s[1]
    if left_sum_new + dual_sum_new < lowest_sum:
        lowest_sum = left_sum_new + dual_sum_new
    if configure(new_hand)[2] > new_chance:
        new_chance = configure(new_hand)[2]


counter = 0
while 1:
    random_card = random.choice(deck)
    # random_card = ['Clubs', 4]
    print('Card from deck:')
    print(random_card)
    print('')
    print(hand)
    print('Current chance:')
    current_chance = configure(hand)[2]
    in_combination = configure(hand)[0]
    not_in_combination = configure(hand)[1]
    print(current_chance)
    print('')
    print("Combinations before card from deck:")
    for c in in_combination:
        print(c)
    print(not_in_combination)

    current_best = []
    new_chance = 0
    new_hand_length = []
    new_hand_chance = []
    left_sum = sum(s[1] for s in not_in_combination[1:])
    dual_sum = 0
    for v in in_combination:
        if len(v) == 3:
            for s in v[1:]:
                dual_sum += s[1]
    lowest_sum = 130
    if len(not_in_combination) > 1:
        print('Looking in Not-Combo...')
        for b in not_in_combination[1:]:
            new_hand_test = deepcopy(hand)
            new_hand_test.insert(new_hand_test.index(b), random_card)
            new_hand_test.remove(b)
            left_sum_new = sum(s[1] for s in configure(new_hand_test)[1][1:])
            dual_sum_new = 0
            for v in configure(new_hand_test)[0]:
                if len(v) == 3:
                    for s in v[1:]:
                        dual_sum_new += s[1]
            if left_sum_new + dual_sum_new < lowest_sum:
                lowest_sum = left_sum_new + dual_sum_new
                new_hand_length = new_hand_test
            if configure(new_hand_test)[2] > new_chance:
                new_chance = configure(new_hand_test)[2]
                new_hand_chance = new_hand_test
    else:
        print('Looking in Combo...')
        two_sized = len([x for x in in_combination if len(x) == 3])
        for b in in_combination:
            if two_sized > 1:
                if len(b) < 4:
                    for cardc in b[1:]:
                        new_hand_test = deepcopy(hand)
                        new_hand_test.insert(new_hand_test.index(cardc), random_card)
                        new_hand_test.remove(cardc)
                        left_sum_new = sum(s[1] for s in configure(new_hand_test)[1][1:])
                        dual_sum_new = 0
                        for v in configure(new_hand_test)[0]:
                            if len(v) == 3:
                                for s in v[1:]:
                                    dual_sum_new += s[1]
                        if left_sum_new + dual_sum_new < lowest_sum:
                            lowest_sum = left_sum_new + dual_sum_new
                            new_hand_length = new_hand_test
                        if configure(new_hand_test)[2] > new_chance:
                            new_chance = configure(new_hand_test)[2]
                            new_hand_chance = new_hand_test
            elif two_sized == 1:
                if len(b) > 4:
                    max_card = max(b[1:], key=lambda x: x[1])
                    min_card = min(b[1:], key=lambda x: x[1])
                    for cardc in b[1:]:
                        if cardc == max_card or cardc == min_card:
                            new_hand_test = deepcopy(hand)
                            new_hand_test.insert(new_hand_test.index(cardc), random_card)
                            new_hand_test.remove(cardc)
                            left_sum_new = sum(s[1] for s in configure(new_hand_test)[1][1:])
                            dual_sum_new = 0
                            for v in configure(new_hand_test)[0]:
                                if len(v) == 3:
                                    for s in v[1:]:
                                        dual_sum_new += s[1]
                            if left_sum_new + dual_sum_new < lowest_sum:
                                lowest_sum = left_sum_new + dual_sum_new
                                new_hand_length = new_hand_test
                            if configure(new_hand_test)[2] > new_chance:
                                new_chance = configure(new_hand_test)[2]
                                new_hand_chance = new_hand_test

    if lowest_sum < left_sum + dual_sum:
        print('')
        print('Swapped for:')
        swapped_card = [item for item in hand if item not in new_hand_length][0]
        print(swapped_card)
        cards_passed.append(swapped_card)
        new_configs = configure(new_hand_length)
        in_combination = new_configs[0]
        not_in_combination = new_configs[1]
        hand = new_hand_length
        print('')
        print('Combinations after card from deck:')
        for c in in_combination:
            print(c)
        print(not_in_combination)
        print('')
    elif lowest_sum == left_sum + dual_sum:
        if new_chance > current_chance:
            print('')
            print('Swapped for:')
            swapped_card = [item for item in hand if item not in new_hand_length][0]
            print(swapped_card)
            cards_passed.append(swapped_card)
            new_configs = configure(new_hand_chance)
            in_combination = new_configs[0]
            not_in_combination = new_configs[1]
            hand = new_hand_chance
            print('')
            print('Combinations after card from deck:')
            for c in in_combination:
                print(c)
            print(not_in_combination)
            print('')
            print('Chance that the next card is good:')
            print(new_chance)
    else:
        print('')
        print('Dit not swap!')
        cards_passed.append(random_card)
    if 0 < lowest_sum < 10:
        print('Stop!')
        print(counter + 1)
        break
    if lowest_sum == 0:
        print('Ginn!')
        print(counter + 1)
        break
    deck.remove(random_card)

    print('------------------------------------------------------------')
    counter += 1

    print(counter)
print(counter + 1)
file = open("round_nums.txt", "a+")
file.write(str(counter+1))
file.write('\n')
file.close()


