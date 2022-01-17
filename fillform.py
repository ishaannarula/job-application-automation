from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome('/Users/in/Downloads/chromedriver')
driver.get("https://boards.greenhouse.io/bridgewater89/jobs/5086910002?t=qo3vb0u62")


my_details = {
    'first_name': 'Enter first name',
    'last_name': 'Enter last name',
    'email': 'Enter e-mail',
    'phone': 'Enter phone no.',
    'school': 'Enter school name',
    'company': 'Enter company name',
    'linkedin': 'Enter linkedin profile link'
}
if 'greenhouse' in driver.current_url:
    #driver.find_element_by_xpath('//*[@class="btn-agree"]').click() #accept cookies

    # Enter Name and Contact Details
    driver.find_element_by_id('first_name').send_keys(my_details['first_name'])
    driver.find_element_by_id('last_name').send_keys(my_details['last_name'])
    driver.find_element_by_id('email').send_keys(my_details['email'])
    driver.find_element_by_id('phone').send_keys(my_details['phone'])

    # Code for attaching CV does not work for now
    driver.find_element_by_css_selector("[data-source='attach']").click()
    time.sleep(10)

    # Enter Education
    # School
    try:
        driver.find_element_by_id('s2id_education_school_name_0').click()
        driver.find_element_by_xpath("//label[contains(.,'LinkedIn')]").send_keys(my_details['school'])
        time.sleep(3)

    except: pass

    # Degree
    try:
        driver.find_element_by_id('s2id_education_degree_0').click()
        driver.find_element_by_xpath("//label[contains(.,'LinkedIn')]").send_keys("Master's Degree")
        time.sleep(3)

    except: pass

    # Discipline
    try:
        driver.find_element_by_id('s2id_education_discipline_0').click()
        driver.find_element_by_xpath("//label[contains(.,'LinkedIn')]").send_keys('Finance')
        time.sleep(3)

    except: pass

    #Enter LinkedIn Profile Link
    try:
        driver.find_element_by_id('job_application_answers_attributes_0_text_value').send_keys(my_details['linkedin'])

    except: pass
#elif 'workday' in driver.current_url:
    