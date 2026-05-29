if 'transformer':
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    import pandas as pd
    import time
    from datetime import datetime
    import pytz

    @transformer
    def transform_df(df, *args, **kwargs):
        """
        Extrait les informations détaillées des offres d'emploi
        """
        if df is None or df.empty:
            print("Aucune URL à traiter")
            return pd.DataFrame()

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')

        paris_tz = pytz.timezone('Europe/Paris')
        current_date = datetime.now(paris_tz).strftime("%d-%m-%Y")

        data = {
            'entreprise': [],
            'publication': [],
            'poste': [],
            'contrat': [],
            'profil': [],
            'description': [],
            'ville': [],
            'lien': [],
            'source': []
        }

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 10)

        try:
            total_urls = len(df)

            for index, row in df.iterrows():
                url = row['url']

                try:
                    driver.get(url)
                    time.sleep(2)

                    def safe_extract(xpath, attribute=None):
                        try:
                            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                            return element.get_attribute(attribute) if attribute else element.text
                        except Exception:
                            return "Non disponible"

                    data['entreprise'].append(safe_extract('//*[@id="app"]/div/div/div/div/div[3]/section/div[1]/div[1]/a/div/span'))
                    data['publication'].append(current_date)
                    data['poste'].append(safe_extract('//*[@id="app"]/div/div/div/div/div[3]/section/div[1]/h2'))
                    data['contrat'].append(safe_extract('//*[@id="app"]/div/div/div/div/div[3]/section/div[1]/div[2]/div/div/div[1]'))
                    data['profil'].append(safe_extract('//*[@id="the-position-section"]/div/div[2]/div[2]/div/div[1]'))
                    data['description'].append(safe_extract('//*[@id="the-position-section"]/div/div[2]/div[1]/div/div[1]'))
                    data['ville'].append(safe_extract('//*[@id="app"]/div/div/div/div/div[3]/section/div[1]/div[2]/div/div/div[2]/span/span'))
                    data['lien'].append(url)
                    data['source'].append("Welcome to the Jungle")

                except Exception as e:
                    continue

                time.sleep(1)

            extracted_df = pd.DataFrame(data)
            return extracted_df

        except Exception as e:
            return pd.DataFrame()

        finally:
            driver.quit()