import logging
from os import stat_result
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
from support import slack


jquery = """
document.body.appendChild((function() {
    var jq = document.createElement('script')
    jq.src = '//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'
    return jq
})())
"""

open_all_leagues_js = """
$('.ipn-Competition-closed').each(function(index, element) {
    element.click()
})
"""

logger = logging.getLogger(__name__)


class Driver(object):
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=' + settings.profile_dir)
        options.add_argument('--profile-directory=' + settings.profile)

        self.driver = uc.Chrome(options=options)
        self.driver.get(settings.url)
        self.driver.set_window_size(1400, 1200)

        self.driver.execute_script(jquery)

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
            return True
        except WebDriverException as e:
            logger.warning(f'action=_click_element, xpath={xpath}')
            logger.warning(e)
            if iterativel:
                sleep(2)
                self._click_element(xpath)
            else:
                return False

    def get_current_url(self):
        return self.driver.current_url

    def create_new_window(self, url):
        script = 'window.open("' + url + '")'
        self.driver.execute_script(script)

    def finish(self):
        self.driver.close()
        self.driver.quit()

    # bet365.com
    def login(self):
        try:
            if not self._click_element(el.login_area, 3, False):
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
        self.driver.execute_script(open_all_leagues_js)
        logger.info('action=open_all_leagues is succeeded!')

    # bet365.com/#/IP/EV???????????C1 > lavel
    def get_game_lavel(self):
        return {
            'game_time': self._get_elements(el.lavel_game_time),
            'team_name_1': self._get_elements(el.team_name_1),
            'team_name_2': self._get_elements(el.team_name_2),
            'score_1': self._get_elements(el.lavel_score_1),
            'score_2': self._get_elements(el.lavel_score_2)}

    # bet365.com/#/IP/EV???????????C1 > status and summary
    def get_game_detail_info(self):
        # stats info
        if not self._click_element(el.stats, 3, False):
            return None
        sleep(0.5)
        attacks = [
            int(self._get_element(el.attacks_1).text),
            int(self._get_element(el.attacks_2).text)]
        d_attacks = [
            int(self._get_element(el.d_attacks_1).text),
            int(self._get_element(el.d_attacks_2).text)]
        try:
            possessions = [
                int(self._get_element(el.possession_1).text),
                int(self._get_element(el.possession_2).text)]
        except TimeoutException:
            possessions = [50, 50]
        yellow_card = [
            int(self._get_element(el.yellow_card_1).text),
            int(self._get_element(el.yellow_card_2).text)]
        red_card = [
            int(self._get_element(el.red_card_1).text),
            int(self._get_element(el.red_card_2).text)]
        corner_kick = [
            int(self._get_element(el.corner_kick_1).text),
            int(self._get_element(el.corner_kick_2).text)]
        on_target = [
            int(self._get_element(el.on_target_1).text),
            int(self._get_element(el.on_target_2).text)]
        off_target = [
            int(self._get_element(el.off_target_1).text),
            int(self._get_element(el.off_target_2).text)]

        # summary info
        self._click_element(el.summary)
        time = int(self._get_element(el.game_time).text[:2])
        number_of_shifts = [
            int(self._get_element(el.number_of_shifts_1).text),
            int(self._get_element(el.number_of_shifts_2).text)]
        pk = [
            int(self._get_element(el.pk_1).text),
            int(self._get_element(el.pk_2).text)]
        goal = [
            int(self._get_element(el.goal_1).text),
            int(self._get_element(el.goal_2).text)]

        return {
            'time': time,
            'attacks': attacks,
            'd_attacks': d_attacks,
            'possession': possessions,
            'yellow_card': yellow_card,
            'red_card': red_card,
            'corner_kick': corner_kick,
            'on_target': on_target,
            'off_target': off_target,
            'number_of_shifts': number_of_shifts,
            'pk': pk,
            'goal': goal}

    def click_game_lavel(self, box):
        count = 0
        try:
            box.click()
            return True
        except NoSuchElementException:
            return False
        except TimeoutException:
            return False
        except ElementClickInterceptedException:
            if count > 5:
                return False
            count += 1
            self.click_game_lavel(box)

    def check_amg(self):
        try:
            count = len(self._get_elements(el.amg_count, limit=1))
        except TimeoutException:
            return False
        if logic.exists_amg(count):
            data = self.get_game_detail_info()
            if logic.can_bet_amg(data):
                return True
        return False

    # bet365.com/#/IP/EV???????????C1
    def send_valid_game(self, data):
        can_not_bet = True
        for i in range(len(data['game_time'])):
            # Check number of golas and game time
            valid = logic.valid_game(
                game_time=int(data['game_time'][i].text[:2]),
                score_1=int(data['score_1'][i].text),
                score_2=int(data['score_2'][i].text))
            if valid and self.click_game_lavel(data['game_time'][i]):
                if self.check_amg():
                    current_url = self.get_current_url()
                    self.create_new_window(current_url)
                    slack.send_message(current_url)
                    can_not_bet = False
        if can_not_bet:
            logger.info('There are no games to bet on.')
        else:
            slack.send_message('🔼 Games which you can bet. 🔼')
