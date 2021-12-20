


sect = arcpy.analysis.Intersect((target_feature, intersecting_list), r"memory\sect", "ALL")


value_dict = {}
def get_field_value_as_dict(input, value_field):
    with arcpy.da.SearchCursor(input, ("OBJECTID", value_field)) as cursor:
        for row in cursor:
            value_dict[row[0]] = row[1]
    return value_dict

def assign_field_value_from_dict(input_dict, target, target_field):
    with arcpy.da.UpdateCursor(target, ("OBJECTID", target_field)) as cursor:
        for row in cursor:
            if row[0] in input_dict.keys():
                row[1] = input_dict[row[0]]
            cursor.updateRow(row)

def get_and_assign_field_value(source, source_field, target, target_field):
	value_dict = get_field_value_as_dict(source, source_field)
	assign_field_value_from_dict(value_dict, target, target_field)