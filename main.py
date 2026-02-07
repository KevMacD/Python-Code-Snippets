import BandConditions
import get_noaa_weather

VANCOUVER_LAT = 49.2827

data = get_noaa_weather.get_noaa_space_weather(timeout_s=8)
print(data)

solar_flux = data['solar_flux']
k_index = data['k_index']
SSN = data['SSN']
conditions = data['conditions']


conditions = BandConditions.calculate_band_conditions(
   solar_flux=solar_flux,
   k_index=k_index,
   utc_hour=23,
   latitude_deg=VANCOUVER_LAT
)
print(conditions)