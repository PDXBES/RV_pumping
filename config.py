import arcpy
import os


sde_egh_public = r"\\oberon\grp117\DAshney\Scripts\connections"

EGH_PUBLIC = os.path.join(sde_egh_public, "egh_public on gisdb1.rose.portland.local.sde")

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
RV_pumping_fs = "https://services.arcgis.com/quVN97tn06YNGj9s/arcgis/rest/services/RV_pumping_sites/FeatureServer/1"
# index seems fragile - it changed on me from 0 to 1 after republishing/updating the service - didn't think doing that should change it

# test - delete
#RV_pumping_fs = r"\\besfile1\ISM_PROJECTS\Work_Orders\WO_9857_A_Chomowicz\Gdb\RV_Pumping_Dev.gdb\RV_pumping_sites_for_testing"

fc_field_dict = {
                 zipcodes:('ZIPCODE_1','Zipcode')
                 ,sextants:('Sextant_1','Sextant')
                 ,nhoods:('NAME','Neighborhood')
                 ,wsheds:('WATERSHED_1', 'Watershed')
                 ,basins:('BASIN_ID_1', 'Basin_ID')
                 ,block_groups:('FIPS', 'BlockGroup_ID')
                }

log_file = r"\\besfile1\ISM_PROJECTS\Work_Orders\WO_9857_A_Chomowicz\log\data_load_log"