import logging
from time import sleep

import action
import logic
from support import line

log_format = '%(asctime)s %(name)-12s %(levelname)s:%(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)


if __name__ == '__main__':
    # driver = action.Driver()
    # driver.first_step()
    # sleep(3)
    # while True:
    #     driver.open_all_leagues()
    #     data = driver.get_game_lavel()
    #     logic.get_valid_game(data)

    #     sleep(300)

    print(line.send_message(['Hello!']))
