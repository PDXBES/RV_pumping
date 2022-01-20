import config
import utility
import arcpy
import os


def get_field_value_as_dict(input, value_field):
    value_dict = {}
    with arcpy.da.SearchCursor(input, ("OBJECTID", value_field)) as cursor:
        for row in cursor:
            value_dict[row[0]] = row[1]
    #print(value_dict)
    return value_dict

def assign_field_value_from_dict(input_dict, target, target_field):
    with arcpy.da.UpdateCursor(target, ("OBJECTID", target_field)) as cursor:
        for row in cursor:
            if row[0] in input_dict.keys():
                #print(str(row[1]) + " = " + str(input_dict[row[0]]))
                row[1] = input_dict[row[0]]
            cursor.updateRow(row)

def get_and_assign_field_value(source, source_field, target, target_field):
    value_dict = get_field_value_as_dict(source, source_field)
    assign_field_value_from_dict(value_dict, target, target_field)


# -------------------------------------------------------------------------
#print("STARTING PROCESS to fill out location fields")

log_obj = utility.Logger(config.log_file)

log_obj.info("STARTING PROCESS - fill out location fields".format())

for key, value in config.fc_field_dict.items():
    intersecting_list = (config.RV_pumping_fs, key)
    #print("intersecting features - " + str(value[1]))
    msg1 = "intersecting features - " + str(value[1])
    log_obj.info(msg1.format())
    in_memory_name = r"memory\sect_" + value[1]
    sect = arcpy.analysis.Intersect(intersecting_list, in_memory_name, "ALL")
    #print("filling field - " + str(value[1]))
    msg2 = "filling field - " + str(value[1])
    log_obj.info(msg2.format())
    get_and_assign_field_value(sect, value[0], config.RV_pumping_fs, value[1])

#print("filling Age")
log_obj.info("- filling Age".format())
with arcpy.da.UpdateCursor(config.RV_pumping_fs, ['created_date', 'DOB', 'Age']) as cursor:
    for row in cursor:
        if row[0] is not None and row[1] is not None:
            row[2] = row[0].year - row[1].year
        cursor.updateRow(row)

#print("PROCESS ENDED")

log_obj.info("PROCESS COMPLETE - fill out location fields".format())