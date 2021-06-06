import logging
import traceback
from pprint import pprint
from time import sleep

from selenium.common.exceptions import WebDriverException

import action

log_format = '%(asctime)s %(name)-12s %(levelname)s:%(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)


def bet365_bot():
    try:
        driver = action.Driver()
        driver.first_step()
        while True:
            driver.open_all_leagues()
            data = driver.get_game_lavel()
            driver.send_valid_game(data)
            sleep(300)

    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f'message={e}')
        sleep(300)


if __name__ == '__main__':
    bet365_bot()

    # text code
    # driver = action.Driver()
    # driver.first_step()
    # sleep(15)
    # print(driver.get_goal_time())


    # from utils.output_csv import output_game_info

    # data = {
    #     'play_time': 63,
    #     'attacks': [78, 69],
    #     'd_attacks': [44, 38],
    #     'possession': [48, 52],
    #     'yellow_card': [2, 5],
    #     'red_card': [0, 0],
    #     'corner_kick': [5, 3],
    #     'on_target': [2, 4],
    #     'off_target': [8, 6],
    #     'shifts': [4, 1],
    #     'pk': [1, 0],
    #     'goal': [2, 1],
    #     'goal_time': [[23, 44], [69]]
    # }
    # output_game_info(data)

