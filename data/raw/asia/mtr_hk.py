# Transcribed MTR Corporation figures (HK$ million, thousand car-km, thousand passengers).
# Ten-year statistics, Annual Report 2025 (source mtr_ar2025_ten_year_stats), years 2016-2025.
YEARS = [2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016]
TEN_YEAR = {
    "car_km_domestic_cross_boundary": [299062, 298180, 291212, 265209, 268050, 268492, 301552, 308742, 301541, 287828],
    "car_km_airport_express": [23150, 23274, 19681, 12328, 10165, 12631, 22971, 23190, 23202, 23276],
    "car_km_light_rail": [10565, 10683, 10316, 9727, 10245, 10385, 10592, 11139, 11145, 11152],
    "pax_domestic": [1594407, 1601690, 1586646, 1334591, 1421737, 1145035, 1568196, 1669973, 1637898, 1586522],
    "pax_cross_boundary": [106673, 98386, 71518, 429, 486, 7647, 104183, 117448, 112549, 113274],
    "avg_trip_km_domestic_cross_boundary": [11.4, 11.3, 11.1, 10.7, 10.5, 10.5, 10.6, 10.8, 10.8, 10.9],
    "staff_hk_transport_operations": [12777, 12392, 11728, 11492, 11688, 11983, 12211, 11948, 11591, 11349],
    "opex_per_car_km_hk_rail_excl_hsr": [36.4, 35.7, 34.3, 36.0, 34.4, 33.3, 33.0, 28.2, 28.5, 27.7],
    "opex_per_passenger_hk_rail_excl_hsr": [6.42, 6.29, 6.00, 6.98, 6.28, 7.60, 5.99, 4.89, 4.93, 4.73],
}
# P&L, "Expenses relating to Hong Kong transport operations" and revenue, from results announcements.
# year -> (source_id, revenue, staff_costs, total_expenses)
PNL = {
    2016: ("mtr_results_2017", 17655, 5191, 10022),
    2017: ("mtr_results_2017", 18201, 5748, 10726),
    2018: ("mtr_results_2018", 19490, 5847, 11319),
    2019: ("mtr_results_2020", 19938, 6489, 14029),
    2020: ("mtr_results_2020", 11896, 6317, 12318),
    2021: ("mtr_results_2021", 13177, 6155, 12343),
    2022: ("mtr_results_2023", 13404, 6341, 12713),
    2023: ("mtr_results_2023", 20131, 6917, 14177),
    2024: ("mtr_results_2025", 23013, 7636, 15319),
    2025: ("mtr_results_2025", 23595, 8077, 15691),
}
