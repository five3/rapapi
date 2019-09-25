from RapAPI import *
from RapAPI.api import SaveAsCase, RunWithNormal

# replay()
SaveAsCase.save_as_flow('vr_woerwo')

result = RunWithNormal.apply_flow('vr_brand_outside')
# result = RunWithNormal.apply_flow('vr_brand_audi')
# result = RunWithNormal.apply_flow('vr_brand_benz')
# result = RunWithNormal.apply_flow('vr_brand_bmw')
# result = RunWithNormal.apply_flow('vr_theme_new_engine')
# result = RunWithNormal.apply_flow('vr_theme_station_new_engine')
# print(result)
