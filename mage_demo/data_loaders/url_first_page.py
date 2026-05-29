if 'data_loader':
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    import pandas as pd
    import time
    import re

    @data_loader
    def load_data(*args, **kwargs):
        """
        Fonction de chargement des données pour Mage
        """
        def parse_time_ago(time_text):
            if 'heures' in time_text or 'heure' in time_text:
                hours = int(re.search(r'\d+', time_text).group())
                return hours
            elif 'minutes' in time_text:
                minutes = int(re.search(r'\d+', time_text).group())
                return minutes / 60
            else:
                return 24

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.binary_location = '/usr/bin/google-chrome'

        try:
            service = Service(executable_path='/usr/local/bin/chromedriver')
            driver = webdriver.Chrome(service=service, options=options)

            url = "https://www.welcometothejungle.com/fr/jobs?query=data&refinementList%5Bcontract_type%5D%5B%5D=internship&refinementList%5Bcontract_type%5D%5B%5D=temporary&refinementList%5Bcontract_type%5D%5B%5D=apprenticeship&refinementList%5Boffices.state%5D%5B%5D=%C3%8Ele-de-France&refinementList%5Boffices.country_code%5D%5B%5D=FR&page=1&aroundQuery=%C3%8Ele-de-France%2C%20France&sortBy=mostRelevant"

            driver.get(url)

            wait = WebDriverWait(driver, 10)
            base_xpath = '//*[@id="app"]/div/div/div/div[2]/div/ul/li'
            wait.until(EC.presence_of_element_located((By.XPATH, base_xpath)))

            jobs_data = []
            should_continue_scrolling = True

            while should_continue_scrolling:
                visible_elements = []
                i = 1
                while True:
                    try:
                        element_xpath = f'//*[@id="app"]/div/div/div/div[2]/div/ul/li[{i}]'
                        element = driver.find_element(By.XPATH, element_xpath)
                        visible_elements.append(element)
                        i += 1
                    except:
                        break

                for element in visible_elements:
                    try:
                        url_element = element.find_element(By.XPATH, './/div/div/div/div[2]/a')
                        url = url_element.get_attribute('href')

                        time_element = element.find_element(By.XPATH, './/time/span')
                        time_ago = time_element.text

                        hours_ago = parse_time_ago(time_ago)

                        if hours_ago < 24:
                            jobs_data.append({
                                'url': url,
                                'published': time_ago,
                                'hours_ago': hours_ago
                            })
                        else:
                            should_continue_scrolling = False
                            break

                    except Exception as e:
                        continue

                if should_continue_scrolling:
                    last_height = driver.execute_script("return document.body.scrollHeight")
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    new_height = driver.execute_script("return document.body.scrollHeight")

                    if new_height == last_height:
                        break

            df = pd.DataFrame(jobs_data)
            return df

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return pd.DataFrame()

        finally:
            if 'driver' in locals():
                driver.quit()