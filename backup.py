import config
import utility
import arcpy, os
from datetime import datetime


log_obj = utility.Logger(config.log_file)
log_obj.info("STARTING PROCESS - BACKUP RV PUMPING FEATURE SERVICE - ".format())

count = str(arcpy.GetCount_management(config.RV_pumping_fs))
log_obj.info("- feature service has {} records - ".format(count))

today = datetime.today()
formatted_today = today.strftime("%Y%m%d")

file_name = "bak_" + formatted_today
full_output_path = os.path.join(config.backup_gdb, file_name)

log_obj.info("- saving to disk: {} ".format(full_output_path))
arcpy.CopyFeatures_management(config.RV_pumping_fs, full_output_path)

log_obj.info("BACKUP RV PUMPING FEATURE SERVICE - PROCESS COMPLETE".format())

