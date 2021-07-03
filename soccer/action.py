import logging
import traceback
from time import sleep

import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        JavascriptException,
                                        NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import elements as el
import logic
import settings
from utils import output_csv, slack

open_all_leagues_js = """
elements = document.getElementsByClassName('ipn-Competition-closed')
count = elements.length
for (let i = 0; i < count; i++) {
    elements[0].click()
}
"""

logger = logging.getLogger(__name__)


class Driver(object):
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=' + settings.profile_dir)
        options.add_argument('--profile-directory=' + settings.profile)

        uc.TARGET_VERSION = 91
        self.driver = uc.Chrome(options=options)
        self.driver.get(settings.url)
        self.driver.set_window_size(1400, 1200)

    def _get_element(self, xpath, limit=5):
        try:
            return WebDriverWait(self.driver, limit).until(
                EC.visibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            logger.warning('action=_get_elements is TimeoutException')
            logger.warning(f'xpath={xpath}')
            return None

    def _get_elements(self, xpath, limit=5):
        try:
            return WebDriverWait(self.driver, limit).until(
                EC.visibility_of_all_elements_located((By.XPATH, xpath)))
        except TimeoutException:
            logger.warning('action=_get_elements is TimeoutException')
            logger.warning(f'xpath={xpath}')
            return None

    def _click_element(self, xpath, limit=5, iterativel=5):
        for _ in range(iterativel):
            element = self._get_element(xpath, limit)
            if element:
                try:
                    element.click()
                    return True
                except (ElementClickInterceptedException,
                        StaleElementReferenceException):
                    sleep(1)
        return False

    def _get_element_text(self, xpath):
        element = self._get_element(xpath, limit=1)
        if element:
            text = element.text
            try:
                return int(text)
            except ValueError:
                return text
        return None

    def _get_elements_text(self, xpath):
        elements = self._get_elements(xpath, limit=1)
        if elements:
            text_list = [e.text for e in elements]
            return text_list
        return None

    def create_new_window(self, url):
        script = 'window.open("' + url + '")'
        self.driver.execute_script(script)

    # bet365.com
    def login(self):
        try:
            if not self._click_element(el.login_area, 3, 3):
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
        sleep(2)
        self._click_element(el.in_play_btn)
        self._click_element(el.soccer_icon)
        sleep(2)
        self._click_element(el.top_game)
        sleep(2)

    def bet_status_check(self):
        if self._get_element(el.bet_count):
            self._click_element(el.my_bets_btn)
            self._click_element(el.team_name)
            self.league_name = self._get_element_text(el.selected_leagu_name)
            self._click_element(el.my_bets_btn)
            return True
        return False

    # bet365.com/#/IP/EV???????????C1
    def open_all_leagues(self):
        self.driver.execute_script(open_all_leagues_js)
        logger.info('action=open_all_leagues is succeeded!')

    # bet365.com/#/IP/EV???????????C1 > lavel
    def get_game_lavel(self):
        elements = self._get_elements(el.lavel_play_time)
        play_times = [e.text[:2] for e in elements]

        return {
            'lavel': self._get_elements(el.lavel),
            'play_time': play_times,
            'team_name_1': self._get_elements_text(el.team_name_1),
            'team_name_2': self._get_elements_text(el.team_name_2),
            'score_1': self._get_elements_text(el.lavel_score_1),
            'score_2': self._get_elements_text(el.lavel_score_2)}

    # bet365.com/#/IP/EV???????????C1 > status and summary
    def get_game_detail_info(self):
        # stats info
        self._click_element(el.stats)
        sleep(0.5)
        attacks = [
            self._get_element_text(el.attacks_1),
            self._get_element_text(el.attacks_2)]
        d_attacks = [
            self._get_element_text(el.d_attacks_1),
            self._get_element_text(el.d_attacks_2)]
        possessions = [
            self._get_element_text(el.possession_1),
            self._get_element_text(el.possession_2)]
        if not (possessions[0] and possessions[1]):
           possessions = [50, 50]
        yellow_card = [
            self._get_element_text(el.yellow_card_1),
            self._get_element_text(el.yellow_card_2)]
        red_card = [
            self._get_element_text(el.red_card_1),
            self._get_element_text(el.red_card_2)]
        corner_kick = [
            self._get_element_text(el.corner_kick_1),
            self._get_element_text(el.corner_kick_2)]
        on_target = [
            self._get_element_text(el.on_target_1),
            self._get_element_text(el.on_target_2)]
        off_target = [
            self._get_element_text(el.off_target_1),
            self._get_element_text(el.off_target_2)]

        # summary info
        self._click_element(el.summary)
        play_time = self._get_element_text(el.play_time)
        shifts = [
            self._get_element_text(el.shifts_1),
            self._get_element_text(el.shifts_2)]
        pk = [
            self._get_element_text(el.pk_1),
            self._get_element_text(el.pk_2)]
        goal = [
            self._get_element_text(el.goal_1),
            self._get_element_text(el.goal_2)]

        self._click_element(el.show_more, limit=0.2, iterativel=1)
        goal_time = self.get_goal_time()

        return {
            'play_time': play_time,
            'attacks': attacks,
            'd_attacks': d_attacks,
            'possession': possessions,
            'yellow_card': yellow_card,
            'red_card': red_card,
            'corner_kick': corner_kick,
            'on_target': on_target,
            'off_target': off_target,
            'shifts': shifts,
            'pk': pk,
            'goal': goal,
            'goal_time': goal_time}

    def get_goal_time(self):
        home_goals = self._get_elements(el.home_goals, limit=0.2)
        away_goals = self._get_elements(el.away_goals, limit=0.2)

        goal_time = [[], []]
        if home_goals:
            for i in range(len(home_goals)):
                goal_time[0].append(eval(home_goals[i].text.replace("'", '')))
        if away_goals:
            for i in range(len(away_goals)):
                goal_time[1].append(eval(away_goals[i].text.replace("'", '')))
        if goal_time[0] or goal_time[1]:
            return goal_time
        return None

    def click_game_lavel(self, box):
        count = 0
        try:
            box.click()
            return True
        except NoSuchElementException:
            return False
        except ElementClickInterceptedException:
            if count > 5:
                return False
            count += 1
            self.click_game_lavel(box)

    def check_amg(self):
        amg_elements = self._get_elements(el.all_amg_under, limit=1)
        if amg_elements and logic.exists_amg(len(amg_elements)):
            data = self.get_game_detail_info()
            if logic.can_bet_amg(data):
                logger.info(data)
                return True
        return False

    # bet365.com/#/IP/EV???????????C1
    def send_valid_game(self, data):
        can_not_bet = True
        urls = []
        for i in range(len(data['lavel'])):
            try:
                # Check number of golas and game time
                valid = logic.valid_game(
                    play_time=int(data['play_time'][i]),
                    score_1=int(data['score_1'][i]),
                    score_2=int(data['score_2'][i]))
                if valid and self.click_game_lavel(data['lavel'][i]):
                    if self.check_amg():
                        current_url = self.driver.current_url
                        self.create_new_window(current_url)
                        urls.append(current_url)
                        can_not_bet = False
            except (StaleElementReferenceException, IndexError) as e:
                logging.warning(traceback.format_exc())
                logger.warning(f'send_valid_game is failed, {e}')
                continue
        if can_not_bet:
            logger.info('There are no games to bet on.')
        else:
            slack.send_message(urls)

    # bet365.com/#/MB/
    def watch_bet_game(self):
        data_1 = {
            'league_name': self.league_name,
            'home_team': self._get_element_text(el.home_team),
            'away_team': self._get_element_text(el.away_team),
            'how_to_bet': self._get_element_text(el.how_to_bet),
            'odds': self._get_element_text(el.odds),
            'stake': self._get_element_text(el.stake)
        }

        while True:
            data_2 = self.get_game_detail_info()
            data_2.update(data_1)
            data_2.update({
                'to_return': self._get_element_text(el.to_return),
                'cash_out': self._get_element_text(el.cash_out)
            })
            output_csv.output_game_info(data_2)
            sleep(300)
            if not self._get_element(el.bet_count):
                break
