from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import xlsxwriter
import configparser
from PIL import Image
import os
import shutil
from libs import utilities
from libs import navigation
from libs import testing

config = utilities.get_configs()

result_dir =  config['DEFAULT']['RESULT_DIR']
report_name = config['DEFAULT']['REPORT_NAME']
pre_validation_report_name = config['DEFAULT']['PRE_VALIDATION_REPORT_NAME']
config_delimiter = config['DEFAULT']['DELIMITER']
conservative_traversal = config['DEFAULT']['CONSERVATIVE_TRAVERSAL'].lower() == 'true'
save_screenshots = config['DEFAULT']['SAVE_SCREENSHOTS'].lower() == 'true'

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
pre_validation_checklist_report = {}  
pre_validation_checklist_dict = {}
pre_validation_checklist_dict["DATA_ANALYSER_OPENS"]="CHECK MANUALLY"
pre_validation_checklist_dict["DATA_ANALYSER_RUN_QRY"]="CHECK MANUALLY"
pre_validation_checklist_dict["JCP_JOB_PAUSED"]="CHECK MANUALLY"
pre_validation_checklist_dict["JCP_SCHEDULE_REMOVED"]="CHECK MANUALLY"
pre_validation_checklist_dict["CONNECTION_TEST_ALL"]="CHECK MANUALLY"

def start_feature_based_testing():
    for feature_name in features:
        feature_name = feature_name.strip()
        try:
            print("\nTesting started for - "+feature_name)
            test_result = {}
            feature_testing_success = True
            if(feature_name=="CONNECTIONS"):
                test_result = testing.check_connections(driver)
            elif(feature_name=="DATA_ANALYZER"):
                test_result = testing.check_data_analyzer(driver)
            elif(feature_name=="JCP"):
                test_result = testing.check_jcp(driver)
            elif(feature_name=="MS_CONFIG"):
                test_result = testing.check_ms_config(driver)
            elif(feature_name=="CERTIFICATION"):
                test_result = testing.check_certification(driver)
            elif(feature_name=="CERT_MANAGEMENT"):
                test_result = testing.check_cert_management(driver)
            else:
                print("Unsupported FEATURE - "+feature_name)
                feature_testing_success = False
            if(feature_testing_success):
                master_report.update(test_result['DETAILED_REPORT'])
                pre_validation_checklist_dict.update(test_result['MASTER_CHECKLIST'])
        except Exception as error1:
            print("Error while testing - "+feature_name) 
            print(error1) 

def main():
    utilities.create_result_dirs(result_dir)
    testing.eic_login(driver,username,password)
    start_feature_based_testing()
    driver.close()
    utilities.prepare_xlsx_report(result_dir+"/"+report_name,master_report)
    utilities.prepare_xlsx_report(result_dir+"/"+pre_validation_report_name,utilities.prepare_pre_validation_checklist_report(pre_validation_checklist_dict))

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