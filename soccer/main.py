import logging
from time import sleep

import action


log_format = '%(asctime)s %(name)-12s %(levelname)s:%(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)


if __name__ == '__main__':
    # driver = action.Driver()
    # driver.first_step()
    # sleep(3)
    # while True:
    #     driver.open_all_leagues()
    #     data = driver.get_game_lavel()
    #     driver.send_valid_game(data)
    #     sleep(300)


    # text code
    driver = action.Driver()
    driver.first_step()
    sleep(3)
    data = driver.get_stats_info()
    print(data['attacks'])
