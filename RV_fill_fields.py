import config
import utility
import arcpy
from datetime import timedelta

#takes about 8 min to run


# -------------------------------------------------------------------------

log_obj = utility.Logger(config.log_file)

log_obj.info("STARTING PROCESS - FILLING FIELDS - ".format())

for key, value in config.fc_field_dict.items():
    intersecting_list = [config.RV_pumping_fs, key]
    msg1 = "intersecting features - " + str(value[1])
    log_obj.info(msg1.format())
    in_memory_name = r"in_memory\sect_" + value[1]
    sect = arcpy.analysis.PairwiseIntersect(intersecting_list, in_memory_name, "ALL")
    msg2 = "filling field - " + str(value[1])
    log_obj.info(msg2.format())
    source_key_field = "FID_L1RV_pumping_sites" #comes from result of intersect #fragile - L1 refers to service index number
    target_key_field = "OBJECTID"
    utility.get_and_assign_field_value(sect, source_key_field, value[0], config.RV_pumping_fs, target_key_field, value[1])

log_obj.info("filling field - Survey Date PST (Survey Date - 8hrs)".format())
with arcpy.da.UpdateCursor(config.RV_pumping_fs, ['Survey_Date', 'Survey_Date_PST']) as cursor:
    for row in cursor:
        if row[0] is not None:
            row[1] = row[0] - timedelta(hours = 8)
        cursor.updateRow(row)

log_obj.info("filling field - Age (Survey Date - DOB)".format())
with arcpy.da.UpdateCursor(config.RV_pumping_fs, ['Survey_Date_PST', 'DOB', 'Age']) as cursor:
    for row in cursor:
        if row[0] is not None and row[1] is not None:
            row[2] = row[0].year - row[1].year
        cursor.updateRow(row)

log_obj.info(" - FILLING FIELDS - PROCESS COMPLETE".format())

