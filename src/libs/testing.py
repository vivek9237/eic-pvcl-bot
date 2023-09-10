from . import navigation
from . import utilities
import time
from selenium.webdriver.common.by import By

config = utilities.get_configs()
config_delimiter = config['DEFAULT']['DELIMITER']
url = config['EIC_CLIENT_ENV']['URL']
connections_csv = config['CONNECTIONS']['CONNECTIONS']
connections = []
connections = connections_csv.split(config_delimiter)
conservative_traversal = config['DEFAULT']['CONSERVATIVE_TRAVERSAL'].lower() == 'true'
save_screenshots = config['DEFAULT']['SAVE_SCREENSHOTS'].lower() == 'true'
result_dir =  config['DEFAULT']['RESULT_DIR']

def eic_login(driver,username,password):
    navigation.open_eic_login_page(driver)
    usernameField = driver.find_element("xpath",'//*[@id="username"]') #id = username
    usernameField.send_keys(username)
    passwordField = driver.find_element("xpath",'//*[@name="j_password"]') #name = j_password
    passwordField.send_keys(password)
    passwordField.submit()

def check_certification(driver):
    master_report = {}
    check_certification_result = {}
    certification_list = []
    certification_report_header = ["Test Case","Result"]
    certification_list.append(certification_report_header)
    try:
        navigation.open_certification_page(driver)
    except Exception as error1:
        print(error1)
    master_report["CERTIFICATION"] = certification_list
    check_certification_result['DETAILED_REPORT'] = master_report
    check_certification_result['MASTER_CHECKLIST'] = {}
    return check_certification_result

def check_cert_management(driver):
    check_cert_management_result = {}
    master_report = {}
    cert_management_list = []
    cert_management_report_header = ["Test Case","Result"]
    cert_management_list.append(cert_management_report_header)
    try:
        navigation.open_cert_management_page(driver)
    except Exception as error1:
        print(error1)
    master_report["CERT_MANAGEMENT"] = cert_management_list
    check_cert_management_result['DETAILED_REPORT'] = master_report
    check_cert_management_result['MASTER_CHECKLIST'] = {}
    return check_cert_management_result

def check_data_analyzer(driver):
    check_data_analyzer_result = {}
    master_query_list = []
    master_query_list_dict = {}
    data_analyzer_report_header = ["Query","Result"]
    master_query_list.append(data_analyzer_report_header)
    master_report = {}
    master_checklist_dict = {}
    master_checklist_dict['DATA_ANALYSER_OPENS'] = "FAIL"
    master_checklist_dict['DATA_ANALYSER_RUN_QRY'] = "FAIL"
    try:
        navigation.open_data_analyzer_page(driver)
        master_checklist_dict['DATA_ANALYSER_OPENS'] = "PASS"
        if(save_screenshots):
            driver.save_screenshot(result_dir+"/data_analyzer_before_running_query.png")
        query_csv = config['DATA_ANALYZER']['QUERY']
        query_list = query_csv.split(";")
        count = 1
        for query_string in query_list:
            if (query_string.strip() != ""):
                try:
                    result = run_data_analyzer_query(driver,query_string.strip())
                    temp_result_list = [query_string.strip(),str(result)]
                    master_query_list.append(temp_result_list)
                    print(query_string.strip() +" = "+str(result))
                    master_checklist_dict['DATA_ANALYSER_RUN_QRY'] = "PASS"
                except Exception as error:
                    temp_result_list = [query_string.strip(),"**Unknown Exception**"]
                    master_query_list.append(temp_result_list)
                    print(query_string.strip() +" = "+str(error))
                finally:
                    if(save_screenshots):
                        driver.save_screenshot(result_dir+"/data_analyzer_after_running_query"+str(count)+".png")
                    count = count + 1
    except Exception as error1:
        if(save_screenshots):
            driver.save_screenshot("../results/data_analyzer_unknown_error.png")
        print(error1)
    master_report["DATA_ANALYZER"] = master_query_list
    check_data_analyzer_result['DETAILED_REPORT'] = master_report
    check_data_analyzer_result['MASTER_CHECKLIST'] = master_checklist_dict
    return check_data_analyzer_result

def perform_save_connection(driver):
    saveButton = navigation.find_element_with_xpath(driver,'//*[@id="saveBtn"]',2,10,True,True)
    saveButton.click()
    connection_status = "**needs manual intervention**"
    retry = 10
    while(retry>0):
        try:
            time.sleep(2)
            connection_message = driver.find_element("xpath", '//*[@id="ui-id-3"]/div[@class="modal-body"]/table/tbody/tr/td')
            connection_status = connection_message.get_attribute("innerHTML")
            if "color:red" in connection_status:
                connection_status = "FAILED"
            else:
                connection_status = "PASS"
            break
        except:
            retry = retry - 1
            continue
    if(conservative_traversal):
        driver.refresh()
    return connection_status.strip()

def open_connection(driver,connection_name):
    print("Trying to open connection "+str(connection_name))
    connectionSearchField = navigation.find_element_with_xpath(driver,'//*[@id="dtsearch_externelconnecdata"]',2,2,True,True)
    connectionSearchField.send_keys(connection_name)
    print("Entered connection name in the search field")
    connectionSearchButton = navigation.find_element_with_xpath(driver,'//*[@id="search_externelconnecdata"]',2,2,True,True)
    connectionSearchButton.click()
    print("Clicked Search button")
    retry = 10
    while(retry>0):
        try:
            time.sleep(2)
            print("Trying to find Connection - "+str(connection_name))
            connectionLink = driver.find_element(By.LINK_TEXT, connection_name)
            connectionLink.click()
            break
        except:
            retry = retry - 1
            continue
    
def check_connections(driver):
    print("Check connection")
    check_connections_dict = {}
    master_checklist_dict = {}
    master_checklist_dict['CONNECTION_TEST_ALL'] = "PASS"

    detailed_connection_test_dict = {}
    detailed_connection_test = []
    connection_report_header = ["Connection Name","Test Result"]
    detailed_connection_test.append(connection_report_header)
    for connection_name in connections:
        try:
            print("Before navigation.open_connection_page")
            navigation.open_connection_page(driver)
            open_connection(driver,connection_name)
            connection_status = perform_save_connection(driver)
            if "PASS" != connection_status:
                master_checklist_dict['CONNECTION_TEST_ALL'] = "FAIL"
            temp_result_list = [connection_name,connection_status]
            detailed_connection_test.append(temp_result_list)
            print(connection_name+" - "+connection_status)
            if(save_screenshots):
                driver.save_screenshot(result_dir+"/connections_tested_"+connection_name+".png")
        except Exception as error1:
            print(error1)
            master_checklist_dict['CONNECTION_TEST_ALL'] = "FAIL"
            if(save_screenshots):
                driver.save_screenshot(result_dir+"/connections_intervention_required_"+connection_name+".png")
            temp_result_list = [connection_name,"**Manual intervention required**"]
            detailed_connection_test.append(temp_result_list)
            print("Some error occured for Connection - "+connection_name)
    detailed_connection_test_dict['CONNECTIONS'] = detailed_connection_test
    check_connections_dict['DETAILED_REPORT'] = detailed_connection_test_dict
    check_connections_dict['MASTER_CHECKLIST'] = master_checklist_dict
    return check_connections_dict

def run_data_analyzer_query(driver,query):
    queryField = navigation.find_element_with_xpath(driver,'//*[@id="queryArea"]',2,2,True,True)
    queryField.clear()
    queryField.send_keys(query)
    time.sleep(5)
    querySubmitButton = navigation.find_element_with_xpath(driver,'//*[@id="querySubmit"]',2,2,True,True)
    querySubmitButton.click()
    time.sleep(5)
    results = navigation.find_element_with_xpath(driver,'//*[@id="resultTable"]/tbody/tr/td',2,2,True,True)
    nextButton = driver.find_element(By.LINK_TEXT, "Next")
    nextButton.click()
    return results.text

def check_jcp(driver):
    jcp_check_list = []
    check_jcp_dict = {}
    master_report = {}
    jcp_report_header = ["Test Case","Result"]
    jcp_check_list.append(jcp_report_header)
    check_jcp_master_check_list = {}
    check_jcp_master_check_list['JCP_JOB_PAUSED'] = "PASS"
    check_jcp_master_check_list['JCP_SCHEDULE_REMOVED'] = "PASS"
    try:
        navigation.open_jcp_page(driver)
        resumeAllJobsButtonPresent = True
        if(save_screenshots):
            driver.save_screenshot(result_dir+"/job_control_panel_jcp.png")
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
            check_jcp_master_check_list['JCP_JOB_PAUSED'] = "PASS"
        else:
            check_jcp_master_check_list['JCP_JOB_PAUSED'] = "FAIL"
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
            check_jcp_master_check_list['JCP_SCHEDULE_REMOVED'] = "PASS"
        else:
            jcp_check_list.append(["Job Schedule Removed","Fail"])
            check_jcp_master_check_list['JCP_SCHEDULE_REMOVED'] = "FAIL"
    except Exception as error1:
        print(error1)
    master_report["JCP"] = jcp_check_list
    check_jcp_dict['DETAILED_REPORT'] = master_report
    check_jcp_dict['MASTER_CHECKLIST'] = check_jcp_master_check_list
    return check_jcp_dict

def check_ms_config(driver):
    master_report = {}
    check_ms_config_dict = {}
    check_ms_config_checklist = {}
    check_ms_config_checklist['MS_CONFIG_UPDATED'] = "FAIL"
    ms_config_check_list = []
    ms_config_report_header = ["Test Case","Result"]
    ms_config_check_list.append(ms_config_report_header)
    try:
        navigation.open_ms_config_page(driver)
        time.sleep(2)
        ms_gateway_url = navigation.find_element_with_xpath(driver,'//input[@id="MS_GATEWAY_URL"]',2,5,True,False)
        ms_tenant_id = navigation.find_element_with_xpath(driver,'//input[@id="MS_TENANT_ID"]',2,5,True,False)
        ecm_instance_url = navigation.find_element_with_xpath(driver,'//input[@id="ECM_INSTANCE_URL"]',2,5,True,False)
        ms_creds = navigation.find_element_with_xpath(driver,'//input[@id="validateMsUser"]',2,5,True,False)
        enable_ms = navigation.find_element_with_xpath(driver,'//input[@id="ENABLE_MS"]',2,5,True,False)
        connectorms_enable = navigation.find_element_with_xpath(driver,'//input[@id="CONNECTORMS.ENABLE"]',2,5,True,False)
        userms_enable = navigation.find_element_with_xpath(driver,'//input[@id="USERMS.ENABLE"]',2,5,True,False)
        rulems_enable = navigation.find_element_with_xpath(driver,'//input[@id="RULEMS.ENABLE"]',2,5,True,False)

        ms_gateway_url_text = ms_gateway_url.get_attribute("value")
        ms_tenant_id_text = ms_tenant_id.get_attribute("value")
        ecm_instance_url_text = ecm_instance_url.get_attribute("value")
        ms_creds_text = ms_creds.get_attribute("value")

        enable_ms_checked = enable_ms.is_selected()
        connectorms_enable_checked = connectorms_enable.is_selected()
        userms_enable_checked = userms_enable.is_selected() #not yet used
        rulems_enable_checked = rulems_enable.is_selected() #not yet used
        ms_config_updated = True
        if(ms_gateway_url_text == (str(url)+"ECMv6/api")):
            ms_config_check_list.append(["MS Gateway Url is correctly updated","Pass"])
        else:
            ms_config_check_list.append(["MS Gateway Url is correctly updated","Fail"])
            ms_config_updated = False
        if(ms_tenant_id_text == ("DEFAULT")):
            ms_config_check_list.append(["Tenant ID is correctly updated","Pass"])
        else:
            ms_config_check_list.append(["Tenant ID is correctly updated","Fail"])
            ms_config_updated = False
        if(ecm_instance_url_text == (str(url)+"ECM")):
            ms_config_check_list.append(["ECM Instance Url is correctly updated","Pass"])
        else:
            ms_config_check_list.append(["ECM Instance Url is correctly updated","Fail"])
            ms_config_updated = False
        if(ms_creds_text == ("**********")):
            ms_config_check_list.append(["MS Credentials is updated","Pass"])
        else:
            ms_config_check_list.append(["MS Credentials is updated","Fail"])
            ms_config_updated = False
        if(enable_ms_checked):
            ms_config_check_list.append(["Enable Microservice is ON","Pass"])
        else:
            ms_config_check_list.append(["Enable Microservice is ON","Fail"])
            ms_config_updated = False
        if(connectorms_enable_checked):
            ms_config_check_list.append(["Enable Connector MicroService is ON","Pass"])
        else:
            ms_config_check_list.append(["Enable Connector MicroService is ON","Fail"])
            ms_config_updated = False
        if(ms_config_updated):
            check_ms_config_checklist['MS_CONFIG_UPDATED'] = "PASS"    
    except Exception as error1:
        print(error1)
    master_report["MS_CONFIG"] = ms_config_check_list
    check_ms_config_dict['DETAILED_REPORT'] = master_report
    check_ms_config_dict['MASTER_CHECKLIST'] = check_ms_config_checklist
    return check_ms_config_dict