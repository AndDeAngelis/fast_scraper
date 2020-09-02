from tqdm import tqdm
import pickle
import numpy as np
import json


class Scraper:
    def __init__(self, browser, url):
        self.matches = []
        self.start_scraping(browser, url)

    def start_scraping(self, browser, url):
        browser.get(url)
        main_table = browser.find_element_by_xpath('/html/body/div[3]/*/div/div/div[1]/section/*/div/table/tbody')
        main_table_rows = main_table.find_elements_by_xpath(".//tr")

        print('Scraping data from ~{} matches...'.format(len(main_table_rows)))

        # Iterate over the main table
        for i in tqdm(range(len(main_table_rows))):
            match = {}
            current_tr_xpath = '//tbody/tr[{}]'.format(i + 1)

            # Scrape basic info
            basic_info = self.scrape_basic_info(browser, current_tr_xpath)
            if basic_info:
                match['basic_info'] = basic_info
                self.matches.append(match)

        # Scrape odds
        print('Scraping 1x2 odds from {} matches'.format(len(self.matches)))
        for i in tqdm(range(len(self.matches))):
            odds_url = self.matches[i].get('basic_info').get('odds_url')
            browser.get(odds_url)
            home_win_dict, draw_dict, away_win_dict = self.scrape_1x2(browser)
            self.matches[i].update({'odds': {}})
            self.matches[i]['odds'].update(home_win_dict)
            self.matches[i]['odds'].update(draw_dict)
            self.matches[i]['odds'].update(away_win_dict)

        print('Scraping under/over 2.5 odds from {} matches'.format(len(self.matches)))
        for i in tqdm(range(len(self.matches))):
            odds_url = self.matches[i].get('basic_info').get('odds_url')
            browser.get('{}#ou'.format(odds_url))
            browser.refresh()
            over_25_dict, under_25_dict = self.scrape_over_under(browser)
            self.matches[i].get('odds').update(over_25_dict)
            self.matches[i].get('odds').update(under_25_dict)

        print('Scraping goal/no goal odds from {} matches'.format(len(self.matches)))
        for i in tqdm(range(len(self.matches))):
            odds_url = self.matches[i].get('basic_info').get('odds_url')
            browser.get('{}#bts'.format(odds_url))
            browser.refresh()
            goal_dict, nogoal_dict = self.scrape_goal_nogoal(browser)
            self.matches[i].get('odds').update(goal_dict)
            self.matches[i].get('odds').update(nogoal_dict)

        print('Saving pickle...')
        self.save_pickle(url, self.matches)

        json_formatted_str = json.dumps(self.matches, indent=4)
        print(json_formatted_str)

    def scrape_basic_info(self, browser, tr_xpath):
        try:
            basic_info = {}

            match_date = browser.find_element_by_xpath('{}/td[6]'.format(tr_xpath)).text
            basic_info['match_date'] = match_date

            nation_reference = browser.find_element_by_xpath('/html/body/div[3]/*/div/div/div[1]/section/ul/li[3]/a')
            nation = nation_reference.text
            basic_info['nation'] = nation

            league_reference = browser.find_element_by_xpath('/html/body/div[3]/*/div/div/div[1]/section/ul/li[4]/span')
            league = league_reference.text
            basic_info['league'] = league

            match_name = browser.find_element_by_xpath('{}/td[1]'.format(tr_xpath)).text
            basic_info['match_name'] = match_name

            result = browser.find_element_by_xpath('{}/td[2]'.format(tr_xpath)).text
            basic_info['result'] = result

            odds_url = browser.find_element_by_xpath('{}/td[1]/a'.format(tr_xpath)).get_attribute('href')
            basic_info['odds_url'] = odds_url

            return basic_info

        except:
            return None

    def scrape_1x2(self, browser):
        odds_table_rows_1x2 = browser.find_elements_by_xpath('//*[@id="sortable-1"]/tbody/tr')

        home_win_dict = {'home_win': {}}
        draw_dict = {'draw': {}}
        away_win_dict = {'away_win': {}}
        for i in range(len(odds_table_rows_1x2)):
            try:
                book_name = browser.find_element_by_xpath('//*[@id="sortable-1"]/tbody/tr[{}]/td[1]'.format(i+1)).text
            except:
                book_name = '__unknown'

            # Home win odd
            try:
                home_win_opening_odd = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][1]'.format(i+1)
                ).get_attribute('data-opening-odd')
            except:
                home_win_opening_odd = np.nan

            try:
                home_win_opening_odd_date = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][1]'.format(i+1)
                ).get_attribute('data-opening-date')
            except:
                home_win_opening_odd_date = np.nan

            try:
                home_win_closing_odd = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][1]'.format(i+1)
                ).get_attribute('data-odd')
            except:
                home_win_closing_odd = np.nan

            try:
                home_win_closing_odd_date = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][1]'.format(i+1)
                ).get_attribute('data-created')
            except:
                home_win_closing_odd_date = np.nan

            current_home_win_dict = {book_name: {home_win_opening_odd_date: home_win_opening_odd,
                                                 home_win_closing_odd_date: home_win_closing_odd}}
            home_win_dict['home_win'].update(current_home_win_dict)

            # Draw odd
            try:
                draw_opening_odd = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][2]'.format(i+1)
                ).get_attribute('data-opening-odd')
            except:
                draw_opening_odd = np.nan

            try:
                draw_opening_odd_date = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][2]'.format(i+1)
                ).get_attribute('data-opening-date')
            except:
                draw_opening_odd_date = np.nan

            try:
                draw_closing_odd = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][2]'.format(i+1)
                ).get_attribute('data-odd')
            except:
                draw_closing_odd = np.nan

            try:
                draw_closing_odd_date = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][2]'.format(i+1)
                ).get_attribute('data-created')
            except:
                draw_closing_odd_date = np.nan

            current_draw_dict = {book_name: {draw_opening_odd_date: draw_opening_odd,
                                                 draw_closing_odd_date: draw_closing_odd}}
            draw_dict['draw'].update(current_draw_dict)

            # Away win odd
            try:
                away_win_opening_odd = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][3]'.format(i+1)
                ).get_attribute('data-opening-odd')
            except:
                away_win_opening_odd = np.nan

            try:
                away_win_opening_odd_date = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][3]'.format(i+1)
                ).get_attribute('data-opening-date')
            except:
                away_win_opening_odd_date = np.nan

            try:
                away_win_closing_odd = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][3]'.format(i+1)
                ).get_attribute('data-odd')
            except:
                away_win_closing_odd = np.nan

            try:
                away_win_closing_odd_date = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][3]'.format(i+1)
                ).get_attribute('data-created')
            except:
                away_win_closing_odd_date = np.nan

            current_away_win_dict = {book_name: {away_win_opening_odd_date: away_win_opening_odd,
                                             away_win_closing_odd_date: away_win_closing_odd}}
            away_win_dict['away_win'].update(current_away_win_dict)

        return home_win_dict, draw_dict, away_win_dict

    def scrape_over_under(self, browser):
        odds_table_rows_uo_25 = browser.find_elements_by_xpath('//tbody/tr/td[contains(text(),"2.5")]/..')

        over_25_dict = {'over_25': {}}
        under_25_dict = {'under_25': {}}

        for i in range(len(odds_table_rows_uo_25)):
            try:
                book_name = browser.find_element_by_xpath('//tbody/tr[{}]/td[contains(text(),"2.5")]/../td[1]'.format(i+1)).text
            except:
                book_name = '__unknown'

            # Over odd
            try:
                over_opening_odd = browser.find_element_by_xpath(
                    '//tbody/tr[{}]/td[contains(text(),"2.5")]/../td[contains(@class, "table-main")][2]'.format(i + 1)
                ).get_attribute('data-opening-odd')
            except:
                over_opening_odd = np.nan

            try:
                over_opening_odd_date = browser.find_element_by_xpath(
                    '//tbody/tr[{}]/td[contains(text(),"2.5")]/../td[contains(@class, "table-main")][2]'.format(i + 1)
                ).get_attribute('data-opening-date')
            except:
                over_opening_odd_date = np.nan

            try:
                over_closing_odd = browser.find_element_by_xpath(
                    '//tbody/tr[{}]/td[contains(text(),"2.5")]/../td[contains(@class, "table-main")][2]'.format(i + 1)
                ).get_attribute('data-odd')
            except:
                over_closing_odd = np.nan

            try:
                over_closing_odd_date = browser.find_element_by_xpath(
                    '//tbody/tr[{}]/td[contains(text(),"2.5")]/../td[contains(@class, "table-main")][2]'.format(i + 1)
                ).get_attribute('data-created')
            except:
                over_closing_odd_date = np.nan

            current_over_dict = {book_name: {over_opening_odd_date: over_opening_odd,
                                             over_closing_odd_date: over_closing_odd}}
            over_25_dict['over_25'].update(current_over_dict)

            # Under odd
            try:
                under_opening_odd = browser.find_element_by_xpath(
                    '//tbody/tr[{}]/td[contains(text(),"2.5")]/../td[contains(@class, "table-main")][3]'.format(i + 1)
                ).get_attribute('data-opening-odd')
            except:
                under_opening_odd = np.nan

            try:
                under_opening_odd_date = browser.find_element_by_xpath(
                    '//tbody/tr[{}]/td[contains(text(),"2.5")]/../td[contains(@class, "table-main")][3]'.format(i + 1)
                ).get_attribute('data-opening-date')
            except:
                under_opening_odd_date = np.nan

            try:
                under_closing_odd = browser.find_element_by_xpath(
                    '//tbody/tr[{}]/td[contains(text(),"2.5")]/../td[contains(@class, "table-main")][3]'.format(i + 1)
                ).get_attribute('data-odd')
            except:
                under_closing_odd = np.nan

            try:
                under_closing_odd_date = browser.find_element_by_xpath(
                    '//tbody/tr[{}]/td[contains(text(),"2.5")]/../td[contains(@class, "table-main")][3]'.format(i + 1)
                ).get_attribute('data-created')
            except:
                under_closing_odd_date = np.nan

            current_under_dict = {book_name: {under_opening_odd_date: under_opening_odd,
                                             under_closing_odd_date: under_closing_odd}}
            under_25_dict['under_25'].update(current_under_dict)

        return over_25_dict, under_25_dict

    def scrape_goal_nogoal(self, browser):
        odds_table_rows_goal_nogoal = browser.find_elements_by_xpath('//*[@id="sortable-1"]/tbody/tr')

        goal_dict = {'goal': {}}
        nogoal_dict = {'no_goal': {}}

        for i in range(len(odds_table_rows_goal_nogoal)):
            try:
                book_name = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[1]'.format(i + 1)).text
            except:
                book_name = '__unknown'

            # Goal odd
            try:
                goal_opening_odd = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][1]'.format(i + 1)
                ).get_attribute('data-opening-odd')
            except:
                goal_opening_odd = np.nan

            try:
                goal_opening_odd_date = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][1]'.format(i + 1)
                ).get_attribute('data-opening-date')
            except:
                goal_opening_odd_date = np.nan

            try:
                goal_closing_odd = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][1]'.format(i + 1)
                ).get_attribute('data-odd')
            except:
                goal_closing_odd = np.nan

            try:
                goal_closing_odd_date = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][1]'.format(i + 1)
                ).get_attribute('data-created')
            except:
                goal_closing_odd_date = np.nan

            current_goal_dict = {book_name: {goal_opening_odd_date: goal_opening_odd,
                                             goal_closing_odd_date: goal_closing_odd}}
            goal_dict['goal'].update(current_goal_dict)

            # No goal odd
            try:
                nogoal_opening_odd = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][2]'.format(i + 1)
                ).get_attribute('data-opening-odd')
            except:
                nogoal_opening_odd = np.nan

            try:
                nogoal_opening_odd_date = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][2]'.format(i + 1)
                ).get_attribute('data-opening-date')
            except:
                nogoal_opening_odd_date = np.nan

            try:
                nogoal_closing_odd = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][2]'.format(i + 1)
                ).get_attribute('data-odd')
            except:
                nogoal_closing_odd = np.nan

            try:
                nogoal_closing_odd_date = browser.find_element_by_xpath(
                    '//*[@id="sortable-1"]/tbody/tr[{}]/td[contains(@class, "table-main")][2]'.format(i + 1)
                ).get_attribute('data-created')
            except:
                nogoal_closing_odd_date = np.nan

            current_nogoal_dict = {book_name: {nogoal_opening_odd_date: nogoal_opening_odd,
                                              nogoal_closing_odd_date: nogoal_closing_odd}}
            nogoal_dict['no_goal'].update(current_nogoal_dict)

        return goal_dict, nogoal_dict

    def save_pickle(self, url, matches):
        nation, league = url.split('/')[4:6]
        pickle_name = '{}_{}.pkl'.format(nation, league)
        with open('./output-pickles/{}'.format(pickle_name), 'wb') as handle:
            pickle.dump(matches, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print('{} correctly saved!'.format(pickle_name))
