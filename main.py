from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import xlsxwriter
import configparser
from PIL import Image


config = configparser.ConfigParser()
config.read('configurations/config.ini')

report_name = config['DEFAULT']['REPORT_NAME']
config_delimiter = config['DEFAULT']['DELIMITER']

connection_page_url = config['EIC_PAGES']['CONNECTION_SEARCH_PAGE']
data_analyzer_page_url = config['EIC_PAGES']['DATA_ANALYZER_PAGE']

url = config['CLIENT_ENV']['URL']
username = config['CLIENT_ENV']['USERNAME']
password = config['CLIENT_ENV']['PASSWORD']
connections_csv = config['CONNECTIONS']['CONNECTIONS']
connections = []
connections = connections_csv.split(config_delimiter)

features_csv = config['CLIENT_ENV']['FEATURES']
features = features_csv.split(config_delimiter)

driver = webdriver.Chrome()
driver.maximize_window()

def eic_login(url,username,password):
    driver.get(url)
    usernameField = driver.find_element("xpath",'//*[@id="username"]') #id = username
    usernameField.send_keys(username)
    passwordField = driver.find_element("xpath",'//*[@name="j_password"]') #name = j_password
    passwordField.send_keys(password)
    passwordField.submit()
    #time.sleep(2)

def open_connection_page():
    driver.get(url+connection_page_url)
    time.sleep(2)

def open_connection(connection_name):
    connectionSearchField = driver.find_element("xpath",'//*[@id="dtsearch_externelconnecdata"]')
    connectionSearchField.send_keys(connection_name)
    connectionSearchButton = driver.find_element("xpath",'//*[@id="search_externelconnecdata"]')
    connectionSearchButton.click()
    retry = 10
    while(retry>0):
        try:
            time.sleep(2)
            connectionLink = driver.find_element(By.LINK_TEXT, connection_name)
            connectionLink.click()
            break
        except:
            retry = retry - 1
            continue

def perform_save_connection():
    saveButton = driver.find_element("xpath",'//*[@id="saveBtn"]')
    saveButton.click()
    connection_status = "**needs manual intervention**"
    retry = 10
    while(retry>0):
        try:
            time.sleep(2)
            connection_message = driver.find_element("xpath", '//*[@id="ui-id-3"]/div[@class="modal-body"]/table/tbody/tr/td')
            connection_status = connection_message.get_attribute("innerHTML")
            break
        except:
            retry = retry - 1
            continue
    return connection_status.strip()
    
def write_result_xlsx(result_dict):
    workbook = xlsxwriter.Workbook(report_name)
    try:
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'Connection Name')
        worksheet.write('B1', 'Test Connection Result')
        i=2
        for connection_name in result_dict:
            worksheet.write('A'+str(i), connection_name)
            worksheet.write('B'+str(i), result_dict[connection_name])
            i = i + 1
    except:
        print("Error saving the result into the report!")
    finally:
        workbook.close()

def open_data_analyzer_page():
    driver.get(url+data_analyzer_page_url)
    
def run_data_analyzer_query(query):
    queryField = driver.find_element("xpath",'//*[@id="queryArea"]')
    queryField.send_keys(query)
    querySubmitButton = driver.find_element("xpath",'//*[@id="querySubmit"]')
    querySubmitButton.click()
    time.sleep(5)
    
def check_data_analyzer():
    try:
        open_data_analyzer_page()
        driver.save_screenshot("results/data_analyzer/before_running_query.png")
        run_data_analyzer_query("select * from users where username='admin'")
        driver.save_screenshot("results/data_analyzer/after_running_query.png")
    except:
        driver.save_screenshot("results/data_analyzer/unknown_error.png")

def check_connections():
    test_connection_result_dict = {}
    for connection_name in connections:
        try:
            open_connection_page()
            open_connection(connection_name)
            connection_status = perform_save_connection()
            test_connection_result_dict[connection_name] = connection_status
            print(connection_name+" - "+connection_status)
            driver.save_screenshot("results/connections/tested/"+connection_name+".png")
        except:
            driver.save_screenshot("results/connections/intervention_required/"+connection_name+".png")
            test_connection_result_dict[connection_name] = "**Manual intervention required**"
            print("Some error occured for Connection - "+connection_name)
    write_result_xlsx(test_connection_result_dict)

def start_feature_based_testing():
    for feature_name in features:
        if(feature_name=="CONNECTIONS"):
            check_connections()
        elif(feature_name=="DATA_ANALYZER"):
            check_data_analyzer()
    
def print_eta():
    print("ETA : "+"<under construction>")

#####################################################################
#       :::     ::: ::::::::::: :::     ::: :::::::::: :::    ::: 
#      :+:     :+:     :+:     :+:     :+: :+:        :+:   :+:   
#     +:+     +:+     +:+     +:+     +:+ +:+        +:+  +:+     
#    +#+     +:+     +#+     +#+     +:+ +#++:++#   +#++:++       
#    +#+   +#+      +#+      +#+   +#+  +#+        +#+  +#+       
#    #+#+#+#       #+#       #+#+#+#   #+#        #+#   #+#       
#     ###     ###########     ###     ########## ###    ###       
#####################################################################

def main():
    print_eta()
    eic_login(url,username,password)
    start_feature_based_testing()

if __name__ == "__main__":
    main()
