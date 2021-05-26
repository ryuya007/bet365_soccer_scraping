import logging


logger = logging.getLogger(__name__)

GAME_START_TIME = 63
GAME_END_TIME = 80


def get_valid_game(data):
    for i in range(len(data['game_time'])):
        if GAME_START_TIME <= int(data['game_time'][i].text[:2]) <= GAME_END_TIME:
            socre_1 = int(data['score_1'][i].text)
            score_2 = int(data['score_2'][i].text)
            if socre_1 + score_2 <= 3 and socre_1 != 3 and score_2 != 3:
                print(data['team_name_1'][i].text, data['team_name_2'][i].text)
