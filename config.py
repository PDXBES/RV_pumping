import arcpy
import os


connections = r"\\besfile1\CCSP\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\connection_files"
EGH_PUBLIC = os.path.join(connections, "GISDB1.EGH_PUBLIC.sde")
GIS_TRANSFER10 = os.path.join(connections, "BESDBPROD1.GIS_TRANSFER10.GIS.sde")

#reference connections
sextants = EGH_PUBLIC + r"\EGH_Public.ARCMAP_ADMIN.sextants_pdx"
zipcodes = EGH_PUBLIC + r"\EGH_PUBLIC.ARCMAP_ADMIN.zipcode_metro"
wsheds = EGH_PUBLIC + r"\EGH_PUBLIC.ARCMAP_ADMIN.watersheds_topography_bes_pdx"
nhoods = EGH_PUBLIC + r"\EGH_PUBLIC.ARCMAP_ADMIN.neighborhoods_pdx"
basins = EGH_PUBLIC + r"\EGH_PUBLIC.ARCMAP_ADMIN.sewer_basins_bes_pdx"
block_groups = EGH_PUBLIC + r"\EGH_PUBLIC.ARCMAP_ADMIN.census_blockgroup_2010_metro"

username = "DASHNEY_PDX_pyscript"
password = "PurpleHawk23"
arcpy.SignInToPortal("https://pdx.maps.arcgis.com/", username, password)
RV_pumping_fs = "https://services.arcgis.com/quVN97tn06YNGj9s/arcgis/rest/services/RV_pumping_sites/FeatureServer/0"
# index seems fragile - it changed on me from 0 to 1 after republishing/updating the service - didn't think doing that should change it

patrols = arcpy.MakeFeatureLayer_management(RV_pumping_fs, r"in_memory\patrols", "Activity = 'Patrol'")
patrols_copy = arcpy.CopyFeatures_management(patrols, r"in_memory\patrols_copy")

fc_field_dict = {
                 zipcodes:('ZIPCODE_1','Zipcode')
                 ,sextants:('Sextant_1','Sextant')
                 ,nhoods:('NAME','Neighborhood')
                 ,wsheds:('WATERSHED_1', 'Watershed')
                 ,basins:('BASIN_ID_1', 'Basin_ID')
                 ,block_groups:('FIPS', 'BlockGroup_ID')
                }

invoice_output = r"\\besfile1\ISM_PROJECTS\Work_Orders\WO_9857_A_Chomowicz\Reports\Invoices"
quarterly_output = r"\\besfile1\ISM_PROJECTS\Work_Orders\WO_9857_A_Chomowicz\Reports\Quarterly"
last_pump_report_gdb = r"\\besfile1\ISM_PROJECTS\Work_Orders\WO_9857_A_Chomowicz\Reports\LastPump_by_Zipcode\output.gdb"
backup_gdb = r"\\besfile1\ISM_PROJECTS\Work_Orders\WO_9857_A_Chomowicz\backups\RV_pumping_fs_backups.gdb"
log_file = r"\\besapp4\GIS\Scripts\Python\Production\RV_pumping\RV_pumping_log"
