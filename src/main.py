from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import xlsxwriter
import configparser
from PIL import Image

config = configparser.ConfigParser()
config.read('../configurations/config.ini')

report_name = config['DEFAULT']['REPORT_NAME']
config_delimiter = config['DEFAULT']['DELIMITER']
conservative_traversal = config['DEFAULT']['CONSERVATIVE_TRAVERSAL'].lower() == 'true'

connection_page_url = config['EIC_PAGES']['CONNECTION_SEARCH_PAGE']
data_analyzer_page_url = config['EIC_PAGES']['DATA_ANALYZER_PAGE']
jcp_page_url = config['EIC_PAGES']['JCP_PAGE']
ms_config_page_url = config['EIC_PAGES']['MS_CONFIG_PAGE']
certification_page_url = config['EIC_PAGES']['CERTIFICATION_PAGE']
cert_management_page_url = config['EIC_PAGES']['CERT_MANAGEMENT_PAGE']
try:
    login_page = config['EIC_PAGES']['LOGIN_PAGE']
except:
    login_page = ''

url = config['EIC_CLIENT_ENV']['URL']
username = config['EIC_CLIENT_ENV']['USERNAME']
password = config['EIC_CLIENT_ENV']['PASSWORD']
features_csv = config['EIC_CLIENT_ENV']['FEATURES']
features = features_csv.split(config_delimiter)

connections_csv = config['CONNECTIONS']['CONNECTIONS']
connections = []
connections = connections_csv.split(config_delimiter)


driver = webdriver.Chrome()
driver.maximize_window()

master_report = {}

def eic_login(url,username,password):
    driver.get(url+login_page)
    usernameField = driver.find_element("xpath",'//*[@id="username"]') #id = username
    usernameField.send_keys(username)
    passwordField = driver.find_element("xpath",'//*[@name="j_password"]') #name = j_password
    passwordField.send_keys(password)
    passwordField.submit()
    #time.sleep(2)

def find_element_with_xpath(xpath,wait_time,num_of_retry,single_element,throw_exception):
    retry = num_of_retry
    while(retry>0):
        try:
            if(single_element):
                element_obj = driver.find_element("xpath",xpath)
                return element_obj
            else:
                element_obj = driver.find_elements("xpath",xpath)
                return element_obj
            break
        except:
            retry = retry - 1
            time.sleep(wait_time)
            continue
    if(retry==0 and throw_exception):
        raise ValueError("Not able to find "+str(xpath))

def open_connection_page():
    if(conservative_traversal):
        try:
            connection_list_button = find_element_with_xpath('//a[@href="/ECM/ecmConfig/externalconfig"]',2,2,True,True)
            connection_list_button.click()
        except:
            try:
                time.sleep(2)
                main_menu_button = find_element_with_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H nav-icon"]',2,10,True,False)
                main_menu_button.click()
                time.sleep(2)
                admin_menu_button = find_element_with_xpath('//a[@href="/ECM/jobcontrol/joblist"]',2,5,True,False)
                admin_menu_button.click()
                time.sleep(2)
                open_burger_menu = find_element_with_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H"]',2,5,True,False)
                open_burger_menu.click()
                time.sleep(2)
                identity_repo_tab = find_element_with_xpath('//*[@class="MuiButtonBase-root MuiIconButton-root sidebar-expand-icon" and @tabindex="0" and @type="button"]',2,5,False,False)[0]
                identity_repo_tab.click()
                time.sleep(2)
                connection_page = find_element_with_xpath('//a[@href="/ECM/ecmConfig/externalconfig"]',2,5,True,False)
                connection_page.click()
            except Exception as error1:
                print(error1)
    else:
        driver.get(url+connection_page_url)
    time.sleep(2)

def open_data_analyzer_page():
    if(conservative_traversal):
        try:
            time.sleep(2)
            main_menu_button = find_element_with_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H nav-icon"]',2,10,True,False)
            main_menu_button.click()
            time.sleep(2)
            admin_menu_button = find_element_with_xpath('//a[@href="/ECM/jobcontrol/joblist"]',2,5,True,False)
            admin_menu_button.click()
            time.sleep(2)
            open_burger_menu = find_element_with_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H"]',2,5,True,False)
            open_burger_menu.click()
            time.sleep(2)
            identity_repo_tab = find_element_with_xpath('//*[@class="MuiButtonBase-root MuiIconButton-root sidebar-expand-icon" and @tabindex="0" and @type="button"]',2,5,False,False)[4]
            identity_repo_tab.click()
            time.sleep(2)
            connection_page = find_element_with_xpath('//a[@href="/ECM/dataAnalyzer/index"]',2,5,True,False)
            connection_page.click()
        except Exception as error1:
            print(error1)
    else:
        driver.get(url+data_analyzer_page_url)
    time.sleep(2)

def open_jcp_page():
    if(conservative_traversal):
        try:
            time.sleep(2)
            main_menu_button = find_element_with_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H nav-icon"]',2,10,True,False)
            main_menu_button.click()
            time.sleep(2)
            admin_menu_button = find_element_with_xpath('//a[@href="/ECM/jobcontrol/joblist"]',2,5,True,False)
            admin_menu_button.click()
            time.sleep(2)
        except Exception as error1:
            print(error1)
    else:
        driver.get(url+jcp_page_url)
    time.sleep(2)

def open_certification_page():
    if(conservative_traversal):
        try:
            time.sleep(2)
            main_menu_button = find_element_with_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H nav-icon"]',2,10,True,False)
            main_menu_button.click()
            time.sleep(2)
            cert_menu_button = find_element_with_xpath('//a[@href="/ECM/campaign/list?status=5"]',2,5,True,False)
            cert_menu_button.click()
            time.sleep(2)
        except Exception as error1:
            print(error1)
    else:
        driver.get(url+certification_page_url)
    time.sleep(2)

def open_ms_config_page():
    if(conservative_traversal):
        try:
            time.sleep(2)
            main_menu_button = find_element_with_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H nav-icon"]',2,10,True,False)
            main_menu_button.click()
            time.sleep(2)
            admin_menu_button = find_element_with_xpath('//a[@href="/ECM/jobcontrol/joblist"]',2,5,True,False)
            admin_menu_button.click()
            time.sleep(2)
            open_burger_menu = find_element_with_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H"]',2,5,True,False)
            open_burger_menu.click()
            time.sleep(2)
            identity_repo_tab = find_element_with_xpath('//*[@class="MuiButtonBase-root MuiIconButton-root sidebar-expand-icon" and @tabindex="0" and @type="button"]',2,5,False,False)[2]
            identity_repo_tab.click()
            time.sleep(2)
            connection_page = find_element_with_xpath('//a[@href="/ECM/ecmConfig/microservicesConfig"]',2,5,True,False)
            connection_page.click()
        except Exception as error1:
            print(error1)
    else:
        driver.get(url+ms_config_page_url)
    time.sleep(2)

def open_cert_management_page():
    if(conservative_traversal):
        try:
            time.sleep(2)
            main_menu_button = find_element_with_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H nav-icon"]',2,10,True,False)
            main_menu_button.click()
            time.sleep(2)
            admin_menu_button = find_element_with_xpath('//a[@href="/ECM/jobcontrol/joblist"]',2,5,True,False)
            admin_menu_button.click()
            time.sleep(2)
            open_burger_menu = find_element_with_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H"]',2,5,True,False)
            open_burger_menu.click()
            time.sleep(2)
            identity_repo_tab = find_element_with_xpath('//*[@class="MuiButtonBase-root MuiIconButton-root sidebar-expand-icon" and @tabindex="0" and @type="button"]',2,5,False,False)[4]
            identity_repo_tab.click()
            time.sleep(2)
            connection_page = find_element_with_xpath('//a[@href="/ECM/certificateManagement/certificateList"]',2,5,True,False)
            connection_page.click()
        except Exception as error1:
            print(error1)
    else:
        driver.get(url+cert_management_page_url)
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
    if(conservative_traversal):
        driver.refresh()
    return connection_status.strip()
    
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
        driver.save_screenshot("../results/data_analyzer/before_running_query.png")
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
                    driver.save_screenshot("../results/data_analyzer/after_running_query"+str(count)+".png")
                    count = count + 1
    except Exception as error1:
        driver.save_screenshot("../results/data_analyzer/unknown_error.png")
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
            driver.save_screenshot("../results/connections/tested/"+connection_name+".png")
        except:
            driver.save_screenshot("../results/connections/intervention_required/"+connection_name+".png")
            temp_result_list = [connection_name,"**Manual intervention required**"]
            master_connection_list.append(temp_result_list)
            print("Some error occured for Connection - "+connection_name)
    master_report["CONNECTION"] = master_connection_list

def check_jcp():
    jcp_check_list = []
    jcp_report_header = ["Test Case","Result"]
    jcp_check_list.append(jcp_report_header)
    try:
        open_jcp_page()
        resumeAllJobsButtonPresent = True
        driver.save_screenshot("../results/job_control_panel/jcp.png")
        addNewJobButton = driver.find_element("xpath",'//*[@onclick="createFlatJob()"]')
        try:
            resumeAllJobsButton = driver.find_element("xpath",'//*[@onclick="disableAllJobs(false)"]')
        except:
            resumeAllJobsButtonPresent = False
        if(addNewJobButton.is_enabled()):
            jcp_check_list.append(["Add New Job button is disabled","Fail"])
        else:
            jcp_check_list.append(["Add New Job button is disabled","Pass"])
        if(resumeAllJobsButtonPresent):
            jcp_check_list.append(["Resume Job button is present","Pass"])
        else:
            jcp_check_list.append(["Resume Job button is present","Fail"])
        if(not(addNewJobButton.is_enabled()) and resumeAllJobsButtonPresent):
            jcp_check_list.append(["All jobs are paused","Pass"])
        else:
            jcp_check_list.append(["All jobs are paused","Fail"])
        job_schedule_removed = True
        job_schedule_time = driver.find_elements("xpath",'//span[@class="UTCDATETIME"]')
        count = 0
        for schedule_time_obj in job_schedule_time:
            count = count + 1
            if(count%2 == 0):
                schedule_time = schedule_time_obj.get_attribute("innerHTML")
                print(schedule_time)
                if("2099" in schedule_time):
                    continue
                else:
                    job_schedule_removed = False
        if(job_schedule_removed):
            jcp_check_list.append(["Job Schedule Removed","Pass"])
        else:
            jcp_check_list.append(["Job Schedule Removed","Fail"])
    except Exception as error1:
        print(error1)
    master_report["JCP"] = jcp_check_list

def check_certification():
    certification_list = []
    certification_report_header = ["Test Case","Result"]
    certification_list.append(certification_report_header)
    try:
        open_certification_page()
    except Exception as error1:
        print(error1)
    master_report["CERTIFICATION"] = certification_list

def check_cert_management():
    cert_management_list = []
    cert_management_report_header = ["Test Case","Result"]
    cert_management_list.append(cert_management_report_header)
    try:
        open_cert_management_page()
    except Exception as error1:
        print(error1)
    master_report["CERT_MANAGEMENT"] = cert_management_list

def check_ms_config():
    ms_config_check_list = []
    ms_config_report_header = ["Test Case","Result"]
    ms_config_check_list.append(ms_config_report_header)
    try:
        open_ms_config_page()
        time.sleep(2)
        ms_gateway_url = find_element_with_xpath('//input[@id="MS_GATEWAY_URL"]',2,5,True,False)
        ms_tenant_id = find_element_with_xpath('//input[@id="MS_TENANT_ID"]',2,5,True,False)
        ecm_instance_url = find_element_with_xpath('//input[@id="ECM_INSTANCE_URL"]',2,5,True,False)
        ms_creds = find_element_with_xpath('//input[@id="validateMsUser"]',2,5,True,False)
        enable_ms = find_element_with_xpath('//input[@id="ENABLE_MS"]',2,5,True,False)
        connectorms_enable = find_element_with_xpath('//input[@id="CONNECTORMS.ENABLE"]',2,5,True,False)
        userms_enable = find_element_with_xpath('//input[@id="USERMS.ENABLE"]',2,5,True,False)
        rulems_enable = find_element_with_xpath('//input[@id="RULEMS.ENABLE"]',2,5,True,False)

        ms_gateway_url_text = ms_gateway_url.get_attribute("value")
        ms_tenant_id_text = ms_tenant_id.get_attribute("value")
        ecm_instance_url_text = ecm_instance_url.get_attribute("value")
        ms_creds_text = ms_creds.get_attribute("value")

        enable_ms_checked = enable_ms.is_selected()
        connectorms_enable_checked = connectorms_enable.is_selected()
        userms_enable_checked = userms_enable.is_selected() #not yet used
        rulems_enable_checked = rulems_enable.is_selected() #not yet used

        if(ms_gateway_url_text == (str(url)+"ECMv6/api")):
            ms_config_check_list.append(["MS Gateway Url is correctly updated","Pass"])
        else:
            ms_config_check_list.append(["MS Gateway Url is correctly updated","Fail"])

        if(ms_tenant_id_text == ("DEFAULT")):
            ms_config_check_list.append(["Tenant ID is correctly updated","Pass"])
        else:
            ms_config_check_list.append(["Tenant ID is correctly updated","Fail"])

        if(ecm_instance_url_text == (str(url)+"ECM")):
            ms_config_check_list.append(["ECM Instance Url is correctly updated","Pass"])
        else:
            ms_config_check_list.append(["ECM Instance Url is correctly updated","Fail"])
        if(ms_creds_text == ("**********")):
            ms_config_check_list.append(["MS Credentials is updated","Pass"])
        else:
            ms_config_check_list.append(["MS Credentials is updated","Fail"])
        if(enable_ms_checked):
            ms_config_check_list.append(["Enable Microservice is ON","Pass"])
        else:
            ms_config_check_list.append(["Enable Microservice is ON","Fail"])
        if(connectorms_enable_checked):
            ms_config_check_list.append(["Enable Connector MicroService is ON","Pass"])
        else:
            ms_config_check_list.append(["Enable Connector MicroService is ON","Fail"])       
    except Exception as error1:
        print(error1)
    master_report["MS_CONFIG"] = ms_config_check_list    

def start_feature_based_testing():
    for feature_name in features:
        feature_name = feature_name.strip()
        try:
            print("\nTesting started for - "+feature_name)
            if(feature_name=="CONNECTIONS"):
                check_connections()
            elif(feature_name=="DATA_ANALYZER"):
                check_data_analyzer()
            elif(feature_name=="JCP"):
                check_jcp()
            elif(feature_name=="MS_CONFIG"):
                check_ms_config()
            elif(feature_name=="CERTIFICATION"):
                check_certification()
            elif(feature_name=="CERT_MANAGEMENT"):
                check_cert_management()
            else:
                print("Unsupported FEATURE - "+feature_name)
        except:
            print("Error while testing - "+feature_name)  
        
def prepare_master_report(master_dict):
    xlsxFile = xlsxwriter.Workbook("../results/"+report_name)
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

def main():
    print_eta()
    create_result_dirs()
    eic_login(url,username,password)
    start_feature_based_testing()
    driver.close();
    prepare_master_report(master_report)

if __name__ == "__main__":
    main()

#####################################################################
#       :::     ::: ::::::::::: :::     ::: :::::::::: :::    ::: 
#      :+:     :+:     :+:     :+:     :+: :+:        :+:   :+:   
#     +:+     +:+     +:+     +:+     +:+ +:+        +:+  +:+     
#    +#+     +:+     +#+     +#+     +:+ +#++:++#   +#++:++       
#    +#+   +#+      +#+      +#+   +#+  +#+        +#+  +#+       
#    #+#+#+#       #+#       #+#+#+#   #+#        #+#   #+#       
#     ###     ###########     ###     ########## ###    ###       
#####################################################################