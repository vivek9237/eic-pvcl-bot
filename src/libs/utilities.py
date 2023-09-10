import xlsxwriter
import os
import configparser

def get_configs():
    config = configparser.ConfigParser()
    config.read('../configurations/config.ini')
    return config

def create_result_dirs(result_dir):
    if os.path.exists(result_dir) and os.path.isdir(result_dir):
        print(f"The folder '{result_dir}' exists.")
        print("Deleting underlying files....")
        for item in os.listdir(result_dir):
            item_path = os.path.join(result_dir, item)
            # Check if it's a file or a subdirectory
            if os.path.isfile(item_path):
                os.remove(item_path)  # Delete file
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Delete subdirectory and its contents
    else:
        print(f"The folder '{result_dir}' does not exist.")
        print("Creating a new folder "+result_dir+"....")
        os.makedirs(result_dir)

def prepare_xlsx_report(abs_report_name,master_dict):
    xlsxFile = xlsxwriter.Workbook(abs_report_name)
    bold_format = xlsxFile.add_format({'bold': True})
    for sheet_name in master_dict:
        temp_sheet = xlsxFile.add_worksheet(sheet_name)
        row = 0
        for record in master_dict[sheet_name]:
            column = 0
            for data in record:
                if(row ==0):
                    temp_sheet.write(row,column,data,bold_format)
                else:
                    temp_sheet.write(row,column,data)
                column = column + 1
            row = row + 1
    xlsxFile.close()

def prepare_pre_validation_checklist_report(test_result_dict):
    pre_validation_checklist_report_dict = {}
    pre_validation_checklist_report_list = []
    pre_validation_checklist_report_header = ["Validation Item","Test Performed","Outcome","Comments","Test Result","Additional Comments"]    
    pre_validation_checklist_report_list.append(pre_validation_checklist_report_header)
    test1 = ["Data Analyser","Data Analyser page opens","","",test_result_dict['DATA_ANALYSER_OPENS'],""]
    test2 = ["Data Analyser","Running queries to generate output","","",test_result_dict['DATA_ANALYSER_RUN_QRY'],""]
    test3 = ["Job Control Panel","All Jobs should be paused in the migrated EIC instance","","",test_result_dict['JCP_JOB_PAUSED'],""]
    test4 = ["Job Control Panel","Job schedules are removed","","",test_result_dict['JCP_SCHEDULE_REMOVED'],""]
    test5 = ["SMTP Configuration","SMTP Configuration is updated in EIC","","","",""]
    test6 = ["SMTP Configuration","SMTP Connection is successful","","","",""]
    test7 = ["Connections","Endpoint Identification is disabled","","","",""]
    test8 = ["Connections","DNS Resolver is setup","","","",""]
    test9 = ["Connections","Drivers are uploaded to EIC","","","",""]
    test10 = ["Connections","Save and Test Connection is successful","","",test_result_dict['CONNECTION_TEST_ALL'],""]
    test11 = ["Connections","SaviyntForSaviynt DB Connection credentials are updated","","","",""]
    test12 = ["Microservice Configuration","Microservice Configuration page is updated","","",test_result_dict['MS_CONFIG_UPDATED'],""]
    test13 = ["Microservice Configuration","MS Sync job is successful","","","",""]
    test14 = ["UI Branding","Customer Branding is applied","","","",""]
    test15 = ["UI Branding","Customer Images are uploaded","","","",""]
    test16 = ["UI Branding","Customer labels are updated","","","",""]
    test17 = ["Certificate Management","Certificate Mangement page shows available certificates","","","",""]
    test18 = ["Certificate Management","Truststore has the same certificates as legacy (Truststore was copied to EIC)","","","",""]
    test19 = ["Configuration File","Ensure that the parameter 'disablejobs' is NOT existing on the externalconfig.properties","","","",""]
    test20 = ["Configuration File","AWS specific paramteres should be removed from Azure deployments","","","",""]
    test21 = ["Single Sign On","Metadata files are imported from legacy environment","","","",""]
    test22 = ["Single Sign On","AuthenticationConfig.groovy is updated as per legacy","","","",""]
    test23 = ["Single Sign On","Check if XML files are editable and downloadable","","","",""]
    test24 = ["File Directory","Extensions are uploaded from legacy to EIC","","","",""]
    test25 = ["File Directory","Extensions connecting directly to the SaviyntDB have their property files updated with new credentials","","","",""]
    test26 = ["File Directory","Customized GSPs are moved from legacy to EIC","","","",""]
    test27 = ["Analytics","Analytics History is available for existing controls","","","",""]
    test28 = ["Certification","Column 'SOURCELASTLOGINDATE' should exists in table 'CERTIFICATION_USER'  in db/data analyzer","","","",""]
    test29 = ["Certification","Existing Certifications open successfully","","","",""]
    test30 = ["Certification","Existing Certifications Templates are available","","","",""]
    test31 = ["Sav Roles","Clear Homepage field from existing Sav Roles","","","",""]
    test32 = ["Sav Roles","No duplicate features available","","","",""]
    test33 = ["Misc","Ensure On-Demand SOD Configs are not present in EIC post migration for AZURE CUSTOMERS ONLY","","","",""]
    test34 = ["Infra","Ensure stage server tomcat is shutdown and not pointing to eic db","","","",""]
    test35 = ["Log Viewer","Able to see the log","","","",""]
    pre_validation_checklist_report_list.append(test1)
    pre_validation_checklist_report_list.append(test2)
    pre_validation_checklist_report_list.append(test3)
    pre_validation_checklist_report_list.append(test4)
    pre_validation_checklist_report_list.append(test5)
    pre_validation_checklist_report_list.append(test6)
    pre_validation_checklist_report_list.append(test7)
    pre_validation_checklist_report_list.append(test8)
    pre_validation_checklist_report_list.append(test9)
    pre_validation_checklist_report_list.append(test10)
    pre_validation_checklist_report_list.append(test11)
    pre_validation_checklist_report_list.append(test12)
    pre_validation_checklist_report_list.append(test13)
    pre_validation_checklist_report_list.append(test14)
    pre_validation_checklist_report_list.append(test15)
    pre_validation_checklist_report_list.append(test16)
    pre_validation_checklist_report_list.append(test17)
    pre_validation_checklist_report_list.append(test18)
    pre_validation_checklist_report_list.append(test19)
    pre_validation_checklist_report_list.append(test20)
    pre_validation_checklist_report_list.append(test21)
    pre_validation_checklist_report_list.append(test22)
    pre_validation_checklist_report_list.append(test23)
    pre_validation_checklist_report_list.append(test24)
    pre_validation_checklist_report_list.append(test25)
    pre_validation_checklist_report_list.append(test26)
    pre_validation_checklist_report_list.append(test27)
    pre_validation_checklist_report_list.append(test28)
    pre_validation_checklist_report_list.append(test29)
    pre_validation_checklist_report_list.append(test30)
    pre_validation_checklist_report_list.append(test31)
    pre_validation_checklist_report_list.append(test32)
    pre_validation_checklist_report_list.append(test33)
    pre_validation_checklist_report_list.append(test34)
    pre_validation_checklist_report_list.append(test35)
    pre_validation_checklist_report_dict['CHECKLIST'] = pre_validation_checklist_report_list
    return pre_validation_checklist_report_dict
