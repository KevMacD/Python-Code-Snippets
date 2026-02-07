import BandConditions

VANCOUVER_LAT = 49.2827

conditions = BandConditions.calculate_band_conditions(
   solar_flux=178,
   k_index=4,
   utc_hour=23,
   latitude_deg=VANCOUVER_LAT
)
print(conditions)