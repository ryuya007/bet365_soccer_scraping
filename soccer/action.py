import logging
from time import sleep

import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException,
                                        StaleElementReferenceException,
                                        WebDriverException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings
import elements as el
import logic
from support import line


logger = logging.getLogger(__name__)


class Driver(object):
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=' + settings.profile_dir)
        options.add_argument('--profile-directory=' + settings.profile)

        self.driver = uc.Chrome(options=options)
        self.driver.get(settings.url)
        self.driver.set_window_size(1400, 1200)

    def _get_element(self, xpath, limit=10):
        return WebDriverWait(self.driver, limit).until(
            EC.visibility_of_element_located((By.XPATH, xpath)))

    def _get_elements(self, xpath, limit=10):
        return WebDriverWait(self.driver, limit).until(
            EC.visibility_of_all_elements_located((By.XPATH, xpath)))

    def _click_element(self, xpath, limit=10, iterativel=True):
        try:
            self._get_element(xpath, limit).click()
            logger.info(f'action=_click_element is succeeded! xpath={xpath}')
        except WebDriverException as e:
            logger.warning(f'action=_click_element, xpath={xpath}')
            logger.warning(e)
            if iterativel:
                sleep(2)
                self._click_element(xpath)
            else:
                return True

    # bet365.com
    def login(self):
        try:
            login_status = self._click_element(el.login_area,
                limit=3, iterativel=False)
            if login_status:
                logger.info('You are already logged in.')
                return
            username = self._get_element(el.login_username)
            password = self._get_element(el.login_password)

            username.clear()
            password.clear()
            username.send_keys(settings.username)
            password.send_keys(settings.password)
            self._click_element(el.login_btn)

            logger.info('action=login is succeeded!')
        except StaleElementReferenceException as e:
            logger.error(f'action=login is failed message={e}')

    def first_step(self):
        self.login()
        sleep(3)
        self._click_element(el.in_play_btn)
        self._click_element(el.soccer_icon)
        self._click_element(el.top_game)

    # bet365.com/#/IP/EV???????????C1
    def open_all_leagues(self):
        try:
            closed_leagues = self._get_elements(el.closed_league)
            for i in range(len(closed_leagues)):
                closed_leagues[i].click()
            logger.info('action=open_all_leagues is succeeded!')
        except NoSuchElementException:
            logger.info('action=open_all_leagues not exist')
        except WebDriverException:
            sleep(2)
            self.open_all_leagues()

    def get_current_url(self):
        return self.driver.current_url

    # bet365.com/#/IP/EV???????????C1
    def get_game_lavel(self):
        return {
            'game_time': self._get_elements(el.lavel_game_time),
            'team_name_1': self._get_elements(el.team_name_1),
            'team_name_2': self._get_elements(el.team_name_2),
            'score_1': self._get_elements(el.lavel_score_1),
            'score_2': self._get_elements(el.lavel_score_2)
        }

    def get_stats_info(self):
        attacks = [
            self._get_element(el.attacks_1).text,
            self._get_element(el.attacks_2).text
        ]
    
        stats_info = {
            'attacks': attacks
        }

        return stats_info

    def valid_bet_amg(self):
        try:
            count = len(self._get_elements(el.amg_count, limit=1))
            result = logic.valid_game_for_amg(count)
            return result
        except TimeoutException:
            return False

    # bet365.com/#/IP/EV???????????C1
    def send_valid_game(self, data):
        url_list = []
        for i in range(len(data['game_time'])):
            result = logic.valid_game(
                game_time=int(data['game_time'][i].text[:2]),
                score_1=int(data['score_1'][i].text),
                score_2=int(data['score_2'][i].text))
            if result:
                data['game_time'][i].click()
                valid = self.valid_bet_amg()
                if valid:
                    url_list.append(self.get_current_url())
        line.send_message(url_list)
