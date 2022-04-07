import config
import utility
import arcpy
import os
from datetime import datetime


def create_invoice(month, year):

    month_year_string = str(month) + "-" + str(year)
    log_obj = utility.Logger(config.log_file)
    log_obj.info("STARTING PROCESS - creating invoice - {}".format(month_year_string))
    start_date = utility.format_monthly_start_date(month, year)
    end_date = utility.format_monthly_end_date(month, year)
    date_subset = arcpy.MakeFeatureLayer_management(config.RV_pumping_fs, r"in_memory\monthly_subset",
                                                    "Survey_Date_PST >= timestamp '{}' "
                                                    "and Survey_Date_PST < timestamp '{}'".format(
                                                        start_date, end_date))
    date_subset_in_memory = arcpy.CopyFeatures_management(date_subset, r"in_memory\monthly_in_memory")
    keep_list = ['Survey_Date_PST', 'Activity', 'Activity_Cost', 'Zipcode']
    utility.delete_fields(date_subset_in_memory, keep_list)
    new_dir_name = month_year_string + "_invoice"
    new_path = os.path.join(config.invoice_output, new_dir_name)
    os.mkdir(new_path)
    arcpy.conversion.TableToExcel(date_subset_in_memory, os.path.join(new_path, month_year_string + "_full.xls"), '#',
                                  'DESCRIPTION')
    sums = arcpy.analysis.Statistics(date_subset_in_memory, r"in_memory\sums", [['Activity_Cost', 'SUM']], 'Activity')
    arcpy.conversion.TableToExcel(sums, os.path.join(new_path, month_year_string + "_sums.xls"), '#', 'DESCRIPTION')
    log_obj.info("END PROCESS - invoice complete - output at ...{}".format(new_path))

#for manual run/ testing
#m = 3
#y = 2022
#create_invoice(m, y)

#assumes this is running within month immediately following invoice report month
now = datetime.now()
month = now.month - 1
year = now.year
create_invoice(month, year)

