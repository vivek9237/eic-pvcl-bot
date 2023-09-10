from . import utilities
import time

config = utilities.get_configs()
url = config['EIC_CLIENT_ENV']['URL']
try:
    login_page = config['EIC_PAGES']['LOGIN_PAGE']
except:
    login_page = ''
conservative_traversal = config['DEFAULT']['CONSERVATIVE_TRAVERSAL'].lower() == 'true'
connection_page_url = config['EIC_PAGES']['CONNECTION_SEARCH_PAGE']
data_analyzer_page_url = config['EIC_PAGES']['DATA_ANALYZER_PAGE']
jcp_page_url = config['EIC_PAGES']['JCP_PAGE']
ms_config_page_url = config['EIC_PAGES']['MS_CONFIG_PAGE']
certification_page_url = config['EIC_PAGES']['CERTIFICATION_PAGE']
cert_management_page_url = config['EIC_PAGES']['CERT_MANAGEMENT_PAGE']

def open_eic_login_page(driver):
    driver.get(url+login_page)

def open_connection_page(driver):
    if(conservative_traversal):
        try:
            connection_list_button = find_element_with_xpath(driver,'//a[@href="/ECM/ecmConfig/externalconfig"]',2,2,True,True)
            connection_list_button.click()
        except:
            try:
                time.sleep(2)
                main_menu_button = find_element_with_xpath(driver,'//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H nav-icon"]',2,10,True,False)
                main_menu_button.click()
                time.sleep(2)
                admin_menu_button = find_element_with_xpath(driver,'//a[@href="/ECM/jobcontrol/joblist"]',2,5,True,False)
                admin_menu_button.click()
                time.sleep(2)
                open_burger_menu = find_element_with_xpath(driver,'//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H"]',2,5,True,False)
                open_burger_menu.click()
                time.sleep(2)
                identity_repo_tab = find_element_with_xpath(driver,'//*[@class="MuiButtonBase-root MuiIconButton-root sidebar-expand-icon" and @tabindex="0" and @type="button"]',2,5,False,False)[0]
                identity_repo_tab.click()
                time.sleep(2)
                connection_page = find_element_with_xpath(driver,'//a[@href="/ECM/ecmConfig/externalconfig"]',2,5,True,False)
                connection_page.click()
            except Exception as error1:
                print(error1)
    else:
        driver.get(url+connection_page_url)
    time.sleep(2)

def open_data_analyzer_page(driver):
    if(conservative_traversal):
        try:
            time.sleep(2)
            main_menu_button = find_element_with_xpath(driver,'//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H nav-icon"]',2,10,True,False)
            main_menu_button.click()
            time.sleep(2)
            admin_menu_button = find_element_with_xpath(driver,'//a[@href="/ECM/jobcontrol/joblist"]',2,5,True,False)
            admin_menu_button.click()
            time.sleep(2)
            open_burger_menu = find_element_with_xpath(driver,'//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H"]',2,5,True,False)
            open_burger_menu.click()
            time.sleep(2)
            identity_repo_tab = find_element_with_xpath(driver,'//*[@class="MuiButtonBase-root MuiIconButton-root sidebar-expand-icon" and @tabindex="0" and @type="button"]',2,5,False,False)[4]
            identity_repo_tab.click()
            time.sleep(2)
            connection_page = find_element_with_xpath(driver,'//a[@href="/ECM/dataAnalyzer/index"]',2,5,True,False)
            connection_page.click()
        except Exception as error1:
            print(error1)
    else:
        driver.get(url+data_analyzer_page_url)
    time.sleep(2)

def open_jcp_page(driver):
    if(conservative_traversal):
        try:
            time.sleep(2)
            main_menu_button = find_element_with_xpath(driver,'//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H nav-icon"]',2,10,True,False)
            main_menu_button.click()
            time.sleep(2)
            admin_menu_button = find_element_with_xpath(driver,'//a[@href="/ECM/jobcontrol/joblist"]',2,5,True,False)
            admin_menu_button.click()
            time.sleep(2)
        except Exception as error1:
            print(error1)
    else:
        driver.get(url+jcp_page_url)
    time.sleep(2)

def open_certification_page(driver):
    if(conservative_traversal):
        try:
            time.sleep(2)
            main_menu_button = find_element_with_xpath(driver,'//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H nav-icon"]',2,10,True,False)
            main_menu_button.click()
            time.sleep(2)
            cert_menu_button = find_element_with_xpath(driver,'//a[@href="/ECM/campaign/list?status=5"]',2,5,True,False)
            cert_menu_button.click()
            time.sleep(2)
        except Exception as error1:
            print(error1)
    else:
        driver.get(url+certification_page_url)
    time.sleep(2)

def open_ms_config_page(driver):
    if(conservative_traversal):
        try:
            time.sleep(2)
            main_menu_button = find_element_with_xpath(driver,'//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H nav-icon"]',2,10,True,False)
            main_menu_button.click()
            time.sleep(2)
            admin_menu_button = find_element_with_xpath(driver,'//a[@href="/ECM/jobcontrol/joblist"]',2,5,True,False)
            admin_menu_button.click()
            time.sleep(2)
            open_burger_menu = find_element_with_xpath(driver,'//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H"]',2,5,True,False)
            open_burger_menu.click()
            time.sleep(2)
            identity_repo_tab = find_element_with_xpath(driver,'//*[@class="MuiButtonBase-root MuiIconButton-root sidebar-expand-icon" and @tabindex="0" and @type="button"]',2,5,False,False)[2]
            identity_repo_tab.click()
            time.sleep(2)
            connection_page = find_element_with_xpath(driver,'//a[@href="/ECM/ecmConfig/microservicesConfig"]',2,5,True,False)
            connection_page.click()
        except Exception as error1:
            print(error1)
    else:
        driver.get(url+ms_config_page_url)
    time.sleep(2)

def open_cert_management_page(driver):
    if(conservative_traversal):
        try:
            time.sleep(2)
            main_menu_button = find_element_with_xpath(driver,'//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H nav-icon"]',2,10,True,False)
            main_menu_button.click()
            time.sleep(2)
            admin_menu_button = find_element_with_xpath(driver,'//a[@href="/ECM/jobcontrol/joblist"]',2,5,True,False)
            admin_menu_button.click()
            time.sleep(2)
            open_burger_menu = find_element_with_xpath(driver,'//button[@class="MuiButtonBase-root MuiIconButton-root Header_iconHover__1Z89H"]',2,5,True,False)
            open_burger_menu.click()
            time.sleep(2)
            identity_repo_tab = find_element_with_xpath(driver,'//*[@class="MuiButtonBase-root MuiIconButton-root sidebar-expand-icon" and @tabindex="0" and @type="button"]',2,5,False,False)[4]
            identity_repo_tab.click()
            time.sleep(2)
            connection_page = find_element_with_xpath(driver,'//a[@href="/ECM/certificateManagement/certificateList"]',2,5,True,False)
            connection_page.click()
        except Exception as error1:
            print(error1)
    else:
        driver.get(url+cert_management_page_url)
    time.sleep(2)

def find_element_with_xpath(driver,xpath,wait_time,num_of_retry,single_element,throw_exception):
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