import logging
from time import sleep

import action

log_format = '%(asctime)s %(name)-12s %(levelname)s:%(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)


if __name__ == '__main__':
    driver = action.Driver()
    driver.first_step()
    sleep(3)
    while True:
        driver.open_all_leagues()
        data = driver.get_game_lavel()
        for i in range(len(data['game_time'])):
            print(data['game_time'][i].text)
            print(data['team_name_1'][i].text)
            print(data['team_name_2'][i].text)
            print(data['score_1'][i].text)
            print(data['score_2'][i].text)

        sleep(300)
