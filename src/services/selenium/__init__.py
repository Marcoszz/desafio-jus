from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

class SeleniumService:
    def __init__(self):
        self.selenium_url = "http://selenium:4444/wd/hub"
        self.chrome_options = webdriver.ChromeOptions()

        self.browser = None

    def open_browser(self):
        if self.browser is None:
            self.browser = webdriver.Remote(command_executor=self.selenium_url, options=self.chrome_options)

    def close_browser(self):
        if self.browser is not None:
            self.browser.quit()
            self.browser = None
    
    def get_process_urls(self, court_urls, process):
        process_urls = []
        process_formatted = self.format_process_to_search(process)

        try:
            self.open_browser()

            process_urls.append(self.handle_process_search_action(court_urls[0], process_formatted))
            process_urls.append(self.handle_process_search_action(court_urls[1], process_formatted, True))    

        except Exception as e:
            print(e)

        finally:
            self.close_browser()

        return process_urls

    def handle_process_search_action(self, court_url, process, second_degree=False):
        self.browser.get(court_url)

        WebDriverWait(self.browser, 5).until(ec.visibility_of_element_located(('xpath', '//*[@id="numeroDigitoAnoUnificado"]')))

        self.browser.find_element('xpath', '//*[@id="numeroDigitoAnoUnificado"]').send_keys(process)
        self.browser.find_element('xpath', '//*[@id="botaoConsultarProcessos"] | //*[@id="pbConsultar"]').click()

        if second_degree:
            try:
                WebDriverWait(self.browser, 5).until(ec.visibility_of_element_located(('xpath', '//*[@id="processoSelecionado"]')))

                self.browser.find_element('xpath', '//*[@id="processoSelecionado"]').click()
                self.browser.find_element('xpath', '//*[@id="botaoEnviarIncidente"]').click()
            except Exception as e:
                print(e)
        
        WebDriverWait(self.browser, 5).until(ec.visibility_of_element_located(('xpath', '//*[@id="numeroProcesso"]')))
        return self.browser.current_url

    def format_process_to_search(self, process):
        process_splitted = process.split("-")
        process_number = process_splitted[0]
        process_identifiers = process_splitted[1].split(".")
        
        identifiers_without_tr = [process_identifiers[i] for i in range(len(process_identifiers)) if i not in [2, 3]]

        return process_number + ''.join(identifiers_without_tr)

selenium_service = SeleniumService()