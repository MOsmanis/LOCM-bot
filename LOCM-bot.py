import sys
import math
from operator import attrgetter

# TODO make attacking most profitable - lose least amount of health and deal most amount of damage (kill most creatures)
# creature health - reserve to put enemy attacking resources
# my attack - what I want to put in enemy health, if I can get it down faster
# Check if I would be dead in 1-2 turns

MY_CARDS = []
class Card:
    def __init__(self,card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw):
        self.card_number = int(card_number)
        self.instance_id = int(instance_id)
        self.location = int(location)
        self.card_type = int(card_type)
        self.cost = int(cost)
        self.attack = int(attack)
        self.defense = int(defense)
        self.abilities = abilities
        self.my_health_change = int(my_health_change)
        self.opponent_health_change = int(opponent_health_change)
        self.card_draw = int(card_draw)

class Player:
    def __init__(self, player_health, player_mana, player_deck, player_rune, player_draw):
        self.player_health = player_health
        self.player_mana = player_mana 
        self.player_deck = player_deck
        self.player_rune = player_rune
        self.player_draw = player_draw 

class CardValue:
    def __init__(self, card, value, draft_index):
        self.card = card
        self.value = value
        self.draft_index = draft_index

def value_card(card, player_deck):
    value = card.attack + card.defense 
    if("G" in card.abilities):
        value += 3
    if card.cost < 7:
        same_mana_cards = [c for c in player_deck if c.cost == card.cost]
        value -= len(same_mana_cards) * 4
    else:
        high_cost_cards = [c for c in player_deck if c.cost >= 7]
        value -= len(high_cost_cards) * 4
    return value

def draft_with_value(draft_cards, player_deck):
    card_values = []
    for c in draft_cards:
        card_values.append(CardValue(c ,value_card(c, player_deck), draft_cards.index(c)))
    selected = max(card_values, key=attrgetter('value'))
    MY_CARDS.append(selected.card)
    return "PICK " + str(selected.draft_index)

# game loop
while True:
    player_health, player_mana, player_deck, player_rune, player_draw = [int(j) for j in input().split()]
    me = Player(player_health, player_mana, player_deck, player_rune, player_draw)

    player_health, player_mana, player_deck, player_rune, player_draw = [int(j) for j in input().split()]
    opponent = Player(player_health, player_mana, player_deck, player_rune, player_draw)

    opponent_hand, opponent_actions = [int(i) for i in input().split()]
    for i in range(opponent_actions):
        card_number_and_action = input()
    card_count = int(input())
    current_cards = []
    for i in range(card_count):
        card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw = input().split()
        current_cards.append(Card(card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw))

    if(me.player_mana==0):
        print(draft_with_value(current_cards, MY_CARDS))
    else:
        commands = ""

        cards_in_hand = [c for c in current_cards if c.location==0]
        playable_monsters = [c for c in cards_in_hand if c.cost<=me.player_mana and c.card_type==0]
        current_mana = me.player_mana
        while(current_mana>0 and len(playable_monsters)>0):
            highest_cost_card = max(playable_monsters, key=attrgetter('cost'))
            current_mana=current_mana-highest_cost_card.cost
            commands += "SUMMON " + str(highest_cost_card.instance_id) + ";"
            cards_in_hand.remove(highest_cost_card)
            playable_monsters = [c for c in cards_in_hand if c.cost<=current_mana and c.card_type==0]

        sys.stderr.write("commands - " + commands)

        cards_on_board = [c for c in current_cards if c.location==1 ]
        attacking_cards = [c for c in cards_on_board if c.attack>0 and not "G" in c.abilities]
        enemy_guards = [c for c in current_cards if c.location==-1 and "G" in c.abilities]
        for usable_card in attacking_cards:
            if len(enemy_guards):
                commands += "ATTACK " + str(usable_card.instance_id) + " " + str(enemy_guards[0].instance_id) + ";"
                enemy_guards[0].defense-=usable_card.attack
                if(enemy_guards[0].defense<=0):
                    enemy_guards.remove(enemy_guards[0])
            else:
                commands += "ATTACK " + str(usable_card.instance_id) + " -1;"
        if(len(enemy_guards)==0):
            for my_guard in [c for c in cards_on_board if c.attack>0 and "G" in c.abilities]:
                commands += "ATTACK " + str(my_guard .instance_id) + " -1;"
        print(commands)
