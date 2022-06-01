import config
import utility
import arcpy
import os
from datetime import datetime

arcpy.env.overwriteOutput = True

def create_last_patrol_by_zipcode():
    log_obj = utility.Logger(config.log_file)
    log_obj.info("STARTING PROCESS - GENERATE LAST PUMP BY ZIPCODE - ".format())

    log_obj.info(" - generate max datetime per zipcode - ".format())
    sums = arcpy.analysis.Statistics(config.patrols_copy, r"in_memory\sums", [['Survey_Date_PST', 'MAX']], 'Zipcode')

    arcpy.AddField_management(sums, 'days_delta', 'SHORT')
    arcpy.AddField_management(sums, 'ZIPCODE_string', 'TEXT')

    log_obj.info(" - calculate days delta - ".format())
    now = datetime.now()
    with arcpy.da.UpdateCursor(sums, ['MAX_Survey_Date_PST', 'days_delta', 'ZIPCODE', 'ZIPCODE_string']) as cursor:
        for row in cursor:
            row[3] = str(row[2])
            if row[0] is not None:
                delta = now - row[0]
                row[1] = delta.days
            cursor.updateRow(row)

    dir_path = os.path.dirname(config.last_pump_report_gdb)
    #arcpy.conversion.TableToExcel(sums, os.path.join(dir_path,'last_pump_by_zipcode.xls'), '#', 'DESCRIPTION')

    log_obj.info(" - create in memory version of zipcode boundaries - ".format())
    zipcodes_copy = arcpy.CopyFeatures_management(config.zipcodes, r"in_memory\zipcodes_copy")

    log_obj.info(" - format fields - ".format())
    keep_fields = ['ZIPCODE']
    utility.delete_fields(zipcodes_copy, keep_fields)

    log_obj.info(" - join days delta with zipcode boundaries - ".format())
    join_fields = ['MAX_Survey_Date_PST', 'days_delta']
    arcpy.JoinField_management(zipcodes_copy, 'ZIPCODE', sums, 'ZIPCODE_string',
                               join_fields)
    with arcpy.da.UpdateCursor(zipcodes_copy, ['days_delta']) as cursor:
        for row in cursor:
            if row[0] is None:
                row[0] = 9999
            cursor.updateRow(row)

    # output to BESDBPROD1.GIS_TRANSFER10 for scheduled nightly - overwrite output
    log_obj.info(" - save result to disk - {}".format(config.GIS_TRANSFER10))
    arcpy.CopyFeatures_management(zipcodes_copy, os.path.join(config.last_pump_report_gdb, "last_patrol_by_zipcode"))
    #arcpy.CopyFeatures_management(zipcodes_copy, os.path.join(config.GIS_TRANSFER10, "last_patrol_by_zipcode"))

    log_obj.info(" - GENERATE LAST PUMP BY ZIPCODE - PROCESS COMPLETE".format())

create_last_patrol_by_zipcode()