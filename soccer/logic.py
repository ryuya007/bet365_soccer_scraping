import logging


logger = logging.getLogger(__name__)

# game time
GAME_START_TIME = 63
GAME_END_TIME = 83

# bet type
AMG_VALID_COUNT = 2

# game status
ATTACKS_COUNT_DIFF = 20
ATTACKS_COUNT_LIMIT = 150
D_ATTACKS_COUNT_DIFF = 20
D_ATTACKS_COUNT_LIMIT = 100
POSSESSION_DIFF = 20
YELLOW_CARD_LIMIT = 10
RED_CARD_LIMIT = 0
CORNER_KICK_LIMIT = 12
ON_TARGET_DIFF = 2
ON_TARGET_LIMIT = 8
OFF_TARGET_DIFF = 3
OFF_TARGET_LIMIT = 12
PK_LIMIT = 0


def valid_game(play_time, score_1, score_2):
    if GAME_START_TIME <= play_time <= GAME_END_TIME:
        if score_1 + score_2 <= 3 and score_1 != 3 and score_2 != 3:
            return True
    return False

def exists_amg(count):
    if count >= AMG_VALID_COUNT:
        return True
    return False

def can_bet_amg(data):
    """
    parameter
        play_time: 63
        attacks: [78, 69]
        d_attacks: [44, 38]
        possession: [48, 52]
        yellow_card: [2, 5]
        red_card: [0, 0]
        corner_kick: [5, 3]
        on_target: [2, 4]
        off_target: [8, 6]
        shifts: [4, 1]
        pk: [1, 0]
        goal: [2, 1]
        goal_time: [[23, 44], [69]]
    """
    if data is None:
        return False

    a_1 = data['attacks'][0]
    a_2 = data['attacks'][1]
    if a_1 == 0 or a_2 == 0 or ATTACKS_COUNT_DIFF < abs(a_1 - a_2) or \
        ATTACKS_COUNT_LIMIT < a_1 + a_2:
        return False

    da_1 = data['d_attacks'][0]
    da_2 = data['d_attacks'][1]
    if da_1 == 0 or da_2 == 0 or D_ATTACKS_COUNT_DIFF < abs(da_1 - da_2) or \
        D_ATTACKS_COUNT_LIMIT < da_1 + da_2:
        return False

    if POSSESSION_DIFF < abs(data['possession'][0] - data['possession'][1]):
        return False

    if YELLOW_CARD_LIMIT < data['yellow_card'][0] + data['yellow_card'][1]:
        return False

    if RED_CARD_LIMIT < data['red_card'][0] + data['red_card'][1]:
        return False

    if CORNER_KICK_LIMIT < data['corner_kick'][0] + data['corner_kick'][1]:
        return False

    on_1 = data['on_target'][0]
    on_2 = data['on_target'][1]
    if (on_1 == 0 and on_2 == 0) or ON_TARGET_DIFF < abs(on_1 - on_2) or \
        ON_TARGET_LIMIT < on_1 + on_2:
        return False

    off_1 = data['on_target'][0]
    off_2 = data['on_target'][1]
    if (off_1 == 0 and off_2 == 0) or OFF_TARGET_DIFF < abs(off_1 - off_2) or \
        OFF_TARGET_LIMIT < off_1 + off_2:
        return False

    if PK_LIMIT < abs(data['pk'][0] + data['pk'][1]):
        return False

    return True
