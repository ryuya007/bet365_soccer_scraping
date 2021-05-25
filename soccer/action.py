import logging
from time import sleep

import undetected_chromedriver.v2 as uc
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException,
                                        StaleElementReferenceException,
                                        WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings
import elements as el

logger = logging.getLogger(__name__)


class Driver(object):
    
    def __init__(self):
        self.driver = uc.Chrome()
        self.driver.get(settings.url)
        self.driver.set_window_size(1400, 1200)

    def _get_element(self, xpath):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath)))

    def _get_elements(self, xpath):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, xpath)))

    def _click_element(self, xpath):
        try:
            self._get_element(xpath).click()
            logger.info(f'action=_click_element is succeeded! xpath={xpath}')
        except WebDriverException as e:
            logger.warning(f'action=_click_element, xpath={xpath}')
            logger.warning(e)
            sleep(2)
            self._click_element(xpath)
    
    def login(self):
        try:
            self._click_element(el.login_area)
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

    def get_game_lavel(self):
        return {
            'game_time': self._get_elements(el.lavel_game_time),
            'team_name_1': self._get_elements(el.team_name_1),
            'team_name_2': self._get_elements(el.team_name_2),
            'score_1': self._get_elements(el.lavel_score_1),
            'score_2': self._get_elements(el.lavel_score_2)
        }