from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By

TIMEOUT = 30
MAX_ATTEMPT = 3

url = "http://giaothong.hochiminhcity.gov.vn/Map.aspx"


def setup_driver(web_driver='chrome', executable_path=None):
    if web_driver == 'safari':
        driver = webdriver.Safari()
    elif web_driver == 'firefox':
        driver = webdriver.Firefox()
    else:
        try:
            driver = webdriver.Chrome(executable_path)
        except:
            driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver


def write_to_file(idx, content, file):
    f = open(file, 'a')
    f.write(idx + ' ' + content + '\n')
    f.close()
    print('write to file: ' + content)


def clickAndCatchStaleRefException(driver, xpath):
    attempts = 0
    while attempts < MAX_ATTEMPT:
        try:
            element = driver.find_element_by_xpath(xpath)
            webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
            break
        except StaleElementReferenceException:
            print('Click element at xpath ' + xpath + ' fail: ' + str(attempts + 1))
            # raise StaleElementReferenceException
        finally:
            attempts += 1
            driver.implicitly_wait(TIMEOUT)


def findElement(driver, option, value):
    attempts = 0
    while attempts < MAX_ATTEMPT:
        try:
            if option == 'id':
                element = driver.find_element_by_id(value)
            elif option == 'xpath':
                element = driver.find_element_by_xpath(value)
            else:
                element = driver.find_element_by_class_name(value)
            webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
            break
        except InvalidSelectorException:
            print('Find element with value ' + value + ' fail: ' + str(attempts + 1))
        finally:
            attempts += 1
            driver.implicitly_wait(TIMEOUT)


driver = setup_driver(executable_path='./chromedriver')
driver.get(url)
driver.implicitly_wait(TIMEOUT)
clickAndCatchStaleRefException(driver, '//*[@id="checkbox-1206-inputEl"]')
driver.implicitly_wait(TIMEOUT)
cameras = driver.find_elements(By.XPATH, '//*[@id="map-panel-1015"]/div[2]/div/div[2]/div/div[2]/div[2]/div')
number_of_camera = len(cameras)
for i in range(1, number_of_camera + 1):
    clickAndCatchStaleRefException(driver, f'//*[@id="map-panel-1015"]/div[2]/div/div[2]/div/div[2]/div[2]/div[{i}]')
    driver.implicitly_wait(TIMEOUT)
    camera_id = driver.find_element(By.XPATH, '//img[starts-with(@class, "camImg-")]')
    write_to_file(str(i), camera_id.get_attribute('src'), './camera_source.txt')
    driver.implicitly_wait(TIMEOUT)
    clickAndCatchStaleRefException(driver, '//*[starts-with(@id, "map-panel-")]/div[2]/div/div[2]/div/div[2]/div[4]/div/div[3]')
    driver.implicitly_wait(TIMEOUT)

