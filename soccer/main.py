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
        sleep(3)
        while True:
            driver.open_all_leagues()
            data = driver.get_game_lavel()
            driver.send_valid_game(data)
            sleep(280)

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
