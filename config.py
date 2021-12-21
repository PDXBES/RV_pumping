
import os


sde_egh_public = r"\\oberon\grp117\DAshney\Scripts\connections"

EGH_PUBLIC = os.path.join(sde_egh_public, "egh_public on gisdb1.rose.portland.local.sde")

#reference connections
sextants = EGH_PUBLIC + r"\EGH_Public.ARCMAP_ADMIN.sextants_pdx"
zipcodes = EGH_PUBLIC + r"\EGH_PUBLIC.ARCMAP_ADMIN.zipcode_metro"
wsheds = EGH_PUBLIC + r"\EGH_PUBLIC.ARCMAP_ADMIN.watersheds_topography_bes_pdx"
nhoods = EGH_PUBLIC + r"\EGH_PUBLIC.ARCMAP_ADMIN.neighborhoods_pdx"
basins = EGH_PUBLIC + r"\EGH_PUBLIC.ARCMAP_ADMIN.sewer_basins_bes_pdx"

RV_pumping_fs = "https://services.arcgis.com/quVN97tn06YNGj9s/arcgis/rest/services/RV_pumping_sites/FeatureServer/0"
