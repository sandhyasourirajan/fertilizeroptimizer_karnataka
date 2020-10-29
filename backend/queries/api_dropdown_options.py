

select_micronutrient_ref_tbl = """select crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare from micronutrient_ref_tbl"""

select_fertilizer_ref_tbl = """select fertilizer_name, cost_per_kg, unit_in_kg, bag_cost from fertilizer_ref_tbl"""

select_fertilizer_ref_tbl_npk = "select n_per_unit, p_per_unit, k_per_unit,fertilizer_name,unit_in_kg from fertilizer_ref_tbl where fertilizer_name in {} order by fertilizer_name"
