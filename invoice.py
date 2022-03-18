import config
import utility
import arcpy
import os


def create_invoice(month, year):

    month_string = str(month) + "-" + str(year)
    log_obj = utility.Logger(config.log_file)
    log_obj.info("STARTING PROCESS - creating invoice - {}".format(month_string))
    start_date = utility.format_start_date(month, year)
    end_date = utility.format_end_date(month, year)
    date_subset = arcpy.MakeFeatureLayer_management(config.RV_pumping_fs, r"in_memory\monthly_subset",
                                                    "Survey_Date >= timestamp '{}' and Survey_Date < timestamp '{}'".format(
                                                        start_date, end_date))
    # will be "Survey_Date >= timestamp '2022-04-01' and Survey_Date < timestamp '2022-05-01'" for April
    date_subset_in_memory = arcpy.CopyFeatures_management(date_subset, r"in_memory\monthly_in_memory")
    keep_list = ['Survey_Date', 'Activity', 'Activity_Cost']
    utility.delete_fields(date_subset_in_memory, keep_list)
    new_dir_name = month_string + "_invoice"
    new_path = os.path.join(config.invoice_output, new_dir_name)
    os.mkdir(new_path)
    arcpy.conversion.TableToExcel(date_subset_in_memory, os.path.join(new_path, month_string + "_full.xls"), '#',
                                  'DESCRIPTION')
    sums = arcpy.analysis.Statistics(date_subset_in_memory, r"in_memory\sums", [['Activity_Cost', 'SUM']], 'Activity')
    arcpy.conversion.TableToExcel(sums, os.path.join(new_path, month_string + "_sums.xls"), '#', 'DESCRIPTION')
    log_obj.info("STARTING PROCESS - invoice complete - output at ...{}".format(new_path))


month = 3
year = 2022
create_invoice(month, year)

