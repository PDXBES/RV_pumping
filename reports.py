import config
import utility
import arcpy
import os


def create_invoice(month, year):

    month_year_string = str(month) + "-" + str(year)
    log_obj = utility.Logger(config.log_file)
    log_obj.info("STARTING PROCESS - creating invoice - {}".format(month_year_string))
    start_date = utility.format_monthly_start_date(month, year)
    end_date = utility.format_monthly_end_date(month, year)
    date_subset = arcpy.MakeFeatureLayer_management(config.RV_pumping_fs, r"in_memory\monthly_subset",
                                                    "Survey_Date >= timestamp '{}' and Survey_Date < timestamp '{}'".format(
                                                        start_date, end_date))
    # will be "Survey_Date >= timestamp '2022-04-01' and Survey_Date < timestamp '2022-05-01'" for April
    date_subset_in_memory = arcpy.CopyFeatures_management(date_subset, r"in_memory\monthly_in_memory")
    keep_list = ['Survey_Date', 'Activity', 'Activity_Cost']
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

# in theory both of these could be setup to read current month from datetime and automatically run reports - then that could be scheduled (2nd of month, 15th of every 3rd month)
# this provides more flexibility though


def create_quarterly_report(month, year):
    month_year_string = str(month) + "-" + str(year)
    log_obj = utility.Logger(config.log_file)
    log_obj.info("STARTING PROCESS - creating quarterly - {}".format(month_year_string))
    start_date = utility.format_quarterly_start_date(month, year)
    end_date = utility.format_quarterly_end_date(month, year)
    date_subset = arcpy.MakeFeatureLayer_management(config.RV_pumping_fs, r"in_memory\quarterly_subset",
                                                    "Survey_Date >= timestamp '{}' and Survey_Date < timestamp '{}'".format(
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
m = 4
y = 2022
create_quarterly_report(m, y)