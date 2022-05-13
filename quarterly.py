import config
import utility
import arcpy
import os
from datetime import datetime


def create_quarterly_report(month, year):
    quarter_year_string = utility.quarter_string_format(month, year)
    #month_year_string = str(month) + "-" + str(year)
    log_obj = utility.Logger(config.log_file)
    log_obj.info("STARTING PROCESS - creating quarterly - {}".format(quarter_year_string))
    start_date = utility.format_quarterly_start_date(month, year)
    print("quarter start: " + str(start_date))
    end_date = utility.format_quarterly_end_date(month, year)
    print("quarter end: " + str(end_date))
    date_subset = arcpy.MakeFeatureLayer_management(config.RV_pumping_fs, r"in_memory\quarterly_subset",
                                                    "Survey_Date_PST >= timestamp '{}' "
                                                    "and Survey_Date_PST < timestamp '{}'".format(
                                                        start_date, end_date))
    date_subset_in_memory = arcpy.CopyFeatures_management(date_subset, r"in_memory\quarterly_in_memory")
    keep_list = ['OBJECTID', 'Zipcode', 'Survey_Date_PST'] #will require more fields if we do more than just a count
    utility.delete_fields(date_subset_in_memory, keep_list)

    new_dir_name = quarter_year_string + "_{}".format('quarterly')
    new_dir = os.path.join(config.quarterly_output, new_dir_name)
    os.mkdir(new_dir)

    output1 = os.path.join(new_dir, quarter_year_string + "_full.xls")
    arcpy.conversion.TableToExcel(date_subset_in_memory, output1, '#',
                                  'DESCRIPTION')

    sums = arcpy.analysis.Statistics(date_subset_in_memory, r"in_memory\sums", [['OBJECTID', 'COUNT']], 'Zipcode')

    output2 = os.path.join(new_dir, quarter_year_string + "_sums.xls")
    arcpy.conversion.TableToExcel(sums, output2, '#', 'DESCRIPTION')
    log_obj.info("END PROCESS - quarterly complete - output at ...{}".format(output2))

#for manual run/ testing
#m = 11
#y = 2021
#create_quarterly_report(m, y)

#assumes this is running within quarter immediately following quarterly report months
#eg Q1 report would ideally run in April
now = datetime.now()
month = now.month
year = now.year
create_quarterly_report(month, year)