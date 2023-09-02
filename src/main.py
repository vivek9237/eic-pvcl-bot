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

master_report = {}

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


def open_data_analyzer_page():
    driver.get(url+data_analyzer_page_url)
    
def run_data_analyzer_query(query):
    queryField = driver.find_element("xpath",'//*[@id="queryArea"]')
    queryField.clear()
    queryField.send_keys(query)
    time.sleep(5)
    querySubmitButton = driver.find_element("xpath",'//*[@id="querySubmit"]') # add retry mechanism here with delay
    querySubmitButton.click()
    time.sleep(5)
    results = driver.find_element("xpath",'//*[@id="resultTable"]/tbody/tr/td') # add retry mechanism here with delay
    nextButton = driver.find_element(By.LINK_TEXT, "Next")
    nextButton.click()
    return results.text
    
def check_data_analyzer():
    master_query_list = []
    data_analyzer_report_header = ["Query","Result"]
    master_query_list.append(data_analyzer_report_header)
    try:
        open_data_analyzer_page()
        driver.save_screenshot("results/data_analyzer/before_running_query.png")
        query_csv = config['DATA_ANALYZER']['QUERY']
        query_list = query_csv.split(";")
        count = 1
        for query_string in query_list:
            if (query_string.strip() != ""):
                try:
                    result = run_data_analyzer_query(query_string.strip())
                    temp_result_list = [query_string.strip(),str(result)]
                    master_query_list.append(temp_result_list)
                    print(query_string.strip() +" = "+str(result))
                except Exception as error:
                    temp_result_list = [query_string.strip(),"**Unknown Exception**"]
                    master_query_list.append(temp_result_list)
                    print(query_string.strip() +" = "+str(error))
                finally:
                    driver.save_screenshot("results/data_analyzer/after_running_query"+str(count)+".png")
                    count = count + 1
    except Exception as error1:
        driver.save_screenshot("results/data_analyzer/unknown_error.png")
        print(error1)
    master_report["DATA_ANALYZER"] = master_query_list

def check_connections():
    master_connection_list = []
    connection_report_header = ["Connection Name","Test Result"]
    master_connection_list.append(connection_report_header)
    for connection_name in connections:
        try:
            open_connection_page()
            open_connection(connection_name)
            connection_status = perform_save_connection()
            temp_result_list = [connection_name,connection_status]
            master_connection_list.append(temp_result_list)
            print(connection_name+" - "+connection_status)
            driver.save_screenshot("results/connections/tested/"+connection_name+".png")
        except:
            driver.save_screenshot("results/connections/intervention_required/"+connection_name+".png")
            temp_result_list = [connection_name,"**Manual intervention required**"]
            master_connection_list.append(temp_result_list)
            print("Some error occured for Connection - "+connection_name)
    master_report["CONNECTION"] = master_connection_list

def start_feature_based_testing():
    for feature_name in features:
        feature_name = feature_name.strip()
        try:
            print("\nTesting started for - "+feature_name)
            if(feature_name=="CONNECTIONS"):
                check_connections()
            elif(feature_name=="DATA_ANALYZER"):
                check_data_analyzer()
            else:
                print("Unsupported FEATURE - "+feature_name)
        except:
            print("Error while testing - "+feature_name)  
        
def prepare_master_report(master_dict):
    xlsxFile = xlsxwriter.Workbook("results/"+report_name)
    for sheet_name in master_dict:
        temp_sheet = xlsxFile.add_worksheet(sheet_name)
        row = 0
        for record in master_dict[sheet_name]:
            column = 0
            for data in record:
                temp_sheet.write(row,column,data)
                column = column + 1
            row = row + 1
    xlsxFile.close()

def create_result_dirs():
    print("Creating result directories <under construction>")

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
    create_result_dirs()
    eic_login(url,username,password)
    start_feature_based_testing()
    driver.close();
    prepare_master_report(master_report)

if __name__ == "__main__":
    main()
