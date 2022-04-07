import config
import utility
import arcpy
import os
from datetime import datetime


def create_quarterly_report(month, year):
    month_year_string = str(month) + "-" + str(year)
    log_obj = utility.Logger(config.log_file)
    log_obj.info("STARTING PROCESS - creating quarterly - {}".format(month_year_string))
    start_date = utility.format_quarterly_start_date(month, year)
    end_date = utility.format_quarterly_end_date(month, year)
    date_subset = arcpy.MakeFeatureLayer_management(config.RV_pumping_fs, r"in_memory\quarterly_subset",
                                                    "Survey_Date_PST >= timestamp '{}' "
                                                    "and Survey_Date_PST < timestamp '{}'".format(
                                                        start_date, end_date))
    date_subset_in_memory = arcpy.CopyFeatures_management(date_subset, r"in_memory\quarterly_in_memory")
    keep_list = ['OBJECTID', 'Zipcode'] #will require more fields if we do more than just a count
    utility.delete_fields(date_subset_in_memory, keep_list)
    #sect = arcpy.analysis.PairwiseIntersect([date_subset_in_memory, config.zipcodes], r"in_memory\sect", "ALL", "#", "POINT")
    sums = arcpy.analysis.Statistics(date_subset_in_memory, r"in_memory\sums", [['OBJECTID', 'COUNT']], 'Zipcode')
    output = os.path.join(config.quarterly_output, month_year_string + "_quarterly.xls")
    arcpy.conversion.TableToExcel(sums, output, '#', 'DESCRIPTION')
    log_obj.info("END PROCESS - quarterly complete - output at ...{}".format(output))

#for manual run/ testing
#m = 4
#y = 2022
#create_quarterly_report(m, y)

#assumes this is running within month immediately following quarterly report months
#eg Q1 report would run within April
now = datetime.now()
month = now.month
year = now.year
create_quarterly_report(month, year)