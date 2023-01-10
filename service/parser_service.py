from service.selenium_proxy import SeleniumConnect
from service.content_service import ContentService
from service.image_service import ImageService
import random
import datetime

import time
from fake_useragent import UserAgent


class ParserService:
    list_host = ''
    name_script = ''
    url = ''

    def __init__(self, list_host, url, name_script):
        self.last_host = ''
        self.list_host = list_host
        self.url = url
        self.name_script = name_script

    def started(self):
        image_service = ImageService()
        useragent = UserAgent()

        page_number = 1
        page_number = int(page_number)

        copy_list_host = list(self.list_host)

        errorCount = dict()
        while True:
            time.sleep(random.randrange(4, 7, 1))

            host = self.get_host(copy_list_host)

            self.last_host = host

            selenium_connect = SeleniumConnect(host, 8000, 'login', 'pass')
            driver = selenium_connect.get_chromedriver(True, useragent.random, self.name_script)
            driver.maximize_window()

            pagination_string = image_service.read_pagination()

            print('errorCount', errorCount)

            try:
                if page_number > 1 and not pagination_string:
                    print('Парсинг завершен')

                    break

                time.sleep(random.randrange(4, 7, 1))

                # если предыдущая попытка закончилась с ошибкой, то все заново проходим ту же страницу
                if page_number not in errorCount:
                    if len(pagination_string):
                        page_number = int(pagination_string.pop(0))

                        image_service.save_pagination(','.join(pagination_string))
                elif errorCount.get(page_number) >= 2:
                    page_number = int(pagination_string.pop(0))

                answer_content = ContentService.get_content(driver, self.url, page_number, self.name_script)

                print('answer_content', answer_content)

                # если в ответе есть ошибка
                if answer_content.get('error'):
                    if page_number in errorCount:
                        errorCount[page_number] += 1
                    else:
                        errorCount[page_number] = 1
                        page_number = answer_content['page']
                else:
                    errorCount = dict()

            except Exception as _ex:
                print(_ex)
                date_exception = datetime.datetime.now()

                with open('logs/log.txt', 'a') as the_file:
                    the_file.write("{}".format(date_exception) + " - " + format(_ex) + '\n')

            finally:
                driver.close()
                driver.quit()

    def get_new_host(self, host):
        if host == self.last_host:
            new_list_host = list(self.list_host)
            host = new_list_host.pop(random.randrange(0, len(new_list_host), 1))
            self.get_new_host(host)

        return host

    def get_host(self, copy_list_host):
        if not copy_list_host:
            copy_list_host = list(self.list_host)

        host = copy_list_host.pop(random.randrange(0, len(copy_list_host), 1))

        if host == self.last_host:
            host = self.get_new_host(host)

        return host
