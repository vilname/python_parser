import time
import datetime
from typing import Dict, Any

from selenium.webdriver.common.by import By
import csv
import random
from selenium.webdriver.common.action_chains import ActionChains

from service.image_service import ImageService


class ContentService:

    @staticmethod
    def get_content(driver, url, page, name_script):

        driver.get(url=url.format(str(page)))

        image_service = ImageService()

        elements = driver.find_elements(By.CSS_SELECTOR, ".iva-item-content-rejJg")

        not_found_phone_button = 0
        iteration = 0
        for element in elements:
            answer_content: Dict[Any, Any] = dict()
            iteration += 1

            print('iteration', iteration)

            # создаю файл пагинации
            if page == 1:
                elements_pagination = driver.find_element(By.CSS_SELECTOR, '.pagination-root-Ntd_O') \
                    .find_elements(By.CSS_SELECTOR, '.pagination-item-JJq_j')
                size = len(elements_pagination)

                last_pagination_element = elements_pagination[size - (page + 1)]

                pagination = list(range((page + 1), int(last_pagination_element.text) + 1))

                pagination_string = image_service.read_pagination()

                if not pagination_string:
                    image_service.save_pagination(','.join(map(str, pagination)))

            # создаю рандомный таймаут
            random_number = random.randrange(3, 6, 1)
            if page % random_number == 0:
                random_number = random.randrange(8, 13, 1)

            time.sleep(random_number)

            try:
                hover = ActionChains(driver).move_to_element(element)
                hover.perform()

                time.sleep(random.randrange(3, 5, 1))

                button_phone_container = element.find_element(By.CSS_SELECTOR, '.phone-button-root-QDB8q')
                button_phone = button_phone_container.find_element(By.TAG_NAME, 'button')
                button_phone.send_keys("\n")
            except Exception as _ex:
                print('_ex-1', _ex)
                not_found_phone_button += 1

                # если в на одной странице в верстке больше 7 раз не нашли элемент, то страница загрузилась плохо
                # пропускаю ошибку, страница загрузиться заново
                if not_found_phone_button >= 7:
                    pass
                else:
                    continue

            if not_found_phone_button >= 7:
                answer_content = {
                    'error': True,
                    'page': page
                }

                return answer_content

            try:
                modal_close = driver.find_element(By.CSS_SELECTOR, '.css-89rnpj')
                modal_close.send_keys("\n")
            except Exception as _ex:
                pass

            time.sleep(random.randrange(4, 7, 1))

            try:
                name_truck = element.find_element(By.CSS_SELECTOR,'.title-listRedesign-_rejR .title-listRedesign-_rejR').get_attribute("textContent")
                place_truck = element.find_element(By.CSS_SELECTOR, '.geo-georeferences-SEtee>span>span').get_attribute("textContent")
                image_base64 = button_phone_container.find_element(By.TAG_NAME, 'img').get_attribute("src")
            except Exception as _ex:
                print('_ex-1', _ex)

                continue

            anonymous = False
            try:
                if element.find_element(By.CSS_SELECTOR, '.phone-button-anonymousNumberTooltipWrapper-sPT1M'):
                    anonymous = True
            except Exception as _ex:
                pass

            name_carrier = ''
            try:
                name_carrier = element.find_element(By.CSS_SELECTOR, '.style-title-_wK5H').get_attribute("textContent")
            except Exception as _ex:
                pass

            image_code = image_base64.split("data:image/png;base64,")

            image_service.save_image(image_code[1], page)
            phone = image_service.get_text_image(page)

            with open("files/trucking_{}.csv".format(name_script), 'a', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)

                spamwriter.writerow([
                    name_truck,
                    place_truck,
                    phone,
                    name_carrier,
                    'Да' if anonymous else 'Нет'
                ])

        return answer_content
