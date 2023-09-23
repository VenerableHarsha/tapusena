from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By

# start = input('enter starting point')
# end = input('enter end point')


def retrieve_data(start, end):
    place_lst = []
    chrome_driverlink = "/Users/krishhashia/Downloads/chromedriver_mac_arm64/chromedriver"
    driver = webdriver.Chrome(executable_path=chrome_driverlink)
    driver.implicitly_wait(15)

    driver.get("https://www.google.com")


    search_field = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')

    try:
        search_field.click()
        search_field.send_keys(f'restaurants on {start} {end} highway')

        search_field.send_keys(Keys.ENTER)

    except ElementClickInterceptedException:
        pass


    more_places = driver.find_element(by=By.XPATH, value='/html/body/div[7]/div/div[11]/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/div[2]/g-more-link/a/div')

    more_places.click()


    elements = driver.find_elements(by=By.CLASS_NAME, value='OSrXXb')

    for element in elements:
        # restaurant_tag = driver.find_element(by=By.XPATH, value='/html/body/div[6]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/div/a[1]/div/div/div[1]/span')
        # restaurant_tag.click()
        # address = driver.find_element(by=By.XPATH, value='//*[@id="akp_tsuid_9"]/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[5]/g-flippy-carousel/div/div/ol/li[1]/span/div/div/div/div[3]/div/div/span[2]')
        place_lst.append(element.text)

    # i = 0
    # for key in place_lst.keys():
    #     while i< 7:
    #         key_to_delete = key
    #         del place_lst[key_to_delete]
    #         i += 1

    for i in range(7):
        place_lst.pop(i)

    driver.quit()
    return place_lst



# field = [f'{start}-{end} restaurants']
# filename = "place_records.txt"
#
# # writing to txt file
# with open(filename, 'w') as textfile:
#
#     # writing the fields
#     textfile.writelines(field)
#
#     # writing the data rows
#     textfile.writelines(place_lst)