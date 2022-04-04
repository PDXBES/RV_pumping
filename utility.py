import logging
import sys, os
import logging.config
import arcpy


# https://stackoverflow.com/questions/6386698/how-to-write-to-a-file-using-the-logging-python-module
def Logger(file_name):
    formatter = logging.Formatter(fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                  datefmt='%Y/%m/%d %H:%M:%S')  # %I:%M:%S %p AM|PM format
    logging.basicConfig(filename='%s.log' % (file_name),
                        format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S', filemode='a', level=logging.INFO)
    log_obj = logging.getLogger()
    log_obj.setLevel(logging.DEBUG)
    # log_obj = logging.getLogger().addHandler(logging.StreamHandler())

    # console printer
    screen_handler = logging.StreamHandler(stream=sys.stdout)  # stream=sys.stdout is similar to normal print
    screen_handler.setFormatter(formatter)
    logging.getLogger().addHandler(screen_handler)

    log_obj.info("Starting log session..")
    return log_obj

def get_field_value_as_dict(input, key_field, value_field):
    value_dict = {}
    with arcpy.da.SearchCursor(input, (key_field, value_field)) as cursor:
        for row in cursor:
            value_dict[row[0]] = row[1]
    #print(value_dict)
    return value_dict

def assign_field_value_from_dict(input_dict, target, target_key_field, target_field):
    with arcpy.da.UpdateCursor(target, (target_key_field, target_field)) as cursor:
        for row in cursor:
            for key, value in input_dict.items():
                #print(str(row[1]) + " = " + str(input_dict[row[0]]))
                if row[0] == key:
                    row[1] = value
            cursor.updateRow(row)

def get_and_assign_field_value(source, source_key_field, source_field, target, target_key_field, target_field):
    value_dict = get_field_value_as_dict(source, source_key_field, source_field)
    assign_field_value_from_dict(value_dict, target, target_key_field, target_field)

def delete_fields(existing_table, keep_fields_list):
    field_name_required_dict = get_field_names_and_required(existing_table)
    remove_list = create_remove_list(field_name_required_dict, keep_fields_list)
    arcpy.DeleteField_management(existing_table, remove_list)

def get_field_names_and_required(input):
    name_and_required_dict = {}
    fields = arcpy.ListFields(input)
    for field in fields:
        name_and_required_dict[field.name] = field.required
    return name_and_required_dict

def create_remove_list(existing_names_and_required, field_list):
    remove_field_list = []
    for key, value in existing_names_and_required.items():
        # second param tests for required fields (OID, Shape, etc), don't want to include these as we cannot modify them
        if key not in field_list and key not in ('Shape', 'OBJECTID') and value != True:
            remove_field_list.append(key)
    return remove_field_list

# create start date for month specified (1st of input month)
def format_monthly_start_date(month, year):
    if month <= 9:
        date = '{}-0{}-01'.format(year, month)
    else:
        date = '{}-{}-01'.format(year, month)
    return date

# create end date for month specifed (1st of month following input month)
def format_monthly_end_date(month, year):
    if month + 1 > 12:
        month = 1
        year = year + 1
        if month <= 9:
            date = '{}-0{}-01'.format(year, month)
        else:
            date = '{}-{}-01'.format(year, month)
        return date
    else:
        month = month + 1
        if month <= 9:
            date = '{}-0{}-01'.format(year, month)
        else:
            date = '{}-{}-01'.format(year, month)
        return date

# create start date of 3 months prior to the month specified (eg 4/2022 returns 1/1/2022)
def format_quarterly_start_date(month, year):
    if month > 3:
        start_month = month - 3
        start_year = year
    elif month == 3:
        start_month = 12
        start_year = year - 1
    elif month == 2:
        start_month = 11
        start_year = year - 1
    elif month == 1:
        start_month = 10
        start_year = year - 1
    start_date = format_monthly_start_date(start_month, start_year)
    return start_date

# create end date of 1 month prior to the month specifiied (eg 4/2022 ruturns 4/1/2022)
def format_quarterly_end_date(month, year):
    end_month = month - 1
    end_date = format_monthly_end_date(end_month, year)
    return end_date