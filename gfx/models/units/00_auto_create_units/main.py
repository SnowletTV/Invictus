from imperator_unit_model import UnitModel

pandya_units = UnitModel(
	filename="../tamil/pandya_infantry_01",
	entity_one_name="pandya_sword_infantry_levy",
	entity_one_mesh="dravidian_infantry_01_mesh",
	entity_one_weapon="mauryan_sword_01_entity",
	entity_one_spear="persian_spear_01_entity",
	entity_one_shield="pandya_shield_01_entity",
	entity_one_drill_post="arabian_drill_post_entity",

	entity_two_name="pandya_sword_infantry_legion",
	entity_two_mesh="dravidian_infantry_01_mesh",
	entity_two_weapon="iberian_sword_01_entity",
	entity_two_spear="persian_spear_01_entity",
	entity_two_shield="iberian_shield_01_entity",
	entity_two_drill_post="arabian_drill_post_entity",
	entity_two_head="mauryan_helmet_01_entity",
)

chola_units = UnitModel(
	filename="../tamil/chola_infantry_01",
	entity_one_name="chola_sword_infantry_levy",
	entity_one_mesh="dravidian_infantry_01_mesh",
	entity_one_weapon="mauryan_sword_01_entity",
	entity_one_spear="persian_spear_01_entity",
	entity_one_shield="chola_shield_01_entity",
	entity_one_drill_post="arabian_drill_post_entity",

	entity_two_name="chola_sword_infantry_legion",
	entity_two_mesh="dravidian_infantry_01_mesh",
	entity_two_weapon="iberian_sword_01_entity",
	entity_two_spear="persian_spear_01_entity",
	entity_two_shield="chola_shield_02_entity",
	entity_two_drill_post="arabian_drill_post_entity",
	entity_two_head="mauryan_helmet_01_entity",
)

chera_units = UnitModel(
	filename="../tamil/chera_infantry_01",
	entity_one_name="chera_sword_infantry_levy",
	entity_one_mesh="dravidian_infantry_01_mesh",
	entity_one_weapon="mauryan_sword_01_entity",
	entity_one_spear="persian_spear_01_entity",
	entity_one_shield="chera_shield_01_entity",
	entity_one_drill_post="arabian_drill_post_entity",

	entity_two_name="chera_sword_infantry_legion",
	entity_two_mesh="dravidian_infantry_01_mesh",
	entity_two_weapon="iberian_sword_01_entity",
	entity_two_spear="persian_spear_01_entity",
	entity_two_shield="iberian_shield_01_entity",
	entity_two_drill_post="arabian_drill_post_entity",
	entity_two_head="mauryan_helmet_01_entity",
)

tamil_units = UnitModel(
	filename="../tamil/tamil_infantry_01",
	entity_one_name="tamil_sword_infantry_levy",
	entity_one_mesh="dravidian_infantry_01_mesh",
	entity_one_weapon="mauryan_sword_01_entity",
	entity_one_spear="persian_spear_01_entity",
	entity_one_shield="mauryan_shield_01_entity",
	entity_one_drill_post="arabian_drill_post_entity",

	entity_two_name="tamil_sword_infantry_legion",
	entity_two_mesh="dravidian_infantry_01_mesh",
	entity_two_weapon="iberian_sword_01_entity",
	entity_two_spear="persian_spear_01_entity",
	entity_two_shield="tamil_shield_01_entity",
	entity_two_drill_post="arabian_drill_post_entity",
	entity_two_head="mauryan_helmet_01_entity",
)

lanka_units = UnitModel(
	filename="../lanka/lanka_infantry_01",
	entity_one_name="lanka_sword_infantry_levy",
	entity_one_mesh="mauryan_infantry_01_mesh",
	entity_one_weapon="iberian_sword_01_entity",
	entity_one_spear="persian_spear_01_entity",
	entity_one_shield="lanka_shield_02_entity",
	entity_one_drill_post="mauryan_drill_post_entity",

	entity_two_name="lanka_sword_infantry_legion",
	entity_two_mesh="mauryan_infantry_01_mesh",
	entity_two_weapon="iberian_sword_01_entity",
	entity_two_spear="persian_spear_01_entity",
	entity_two_shield="lanka_shield_01_entity",
	entity_two_drill_post="mauryan_drill_post_entity",
	entity_two_head="mauryan_helmet_01_entity",

	entity_three_name="lankan_generic_infantry_legion",
	entity_three_mesh="mauryan_infantry_01_mesh",
	entity_three_weapon="iberian_sword_01_entity",
	entity_three_spear="persian_spear_01_entity",
	entity_three_shield="numidian_shield_01_entity",
	entity_three_drill_post="mauryan_drill_post_entity",
	entity_three_head="mauryan_helmet_01_entity",
)

if __name__ == '__main__':
	# pandya_units.write_file()
	# pandya_units.add_unit_types("pandya_sword_infantry_levy", "pandya_sword_infantry_legion", "PND")

	# chola_units.write_file()
	# chola_units.add_unit_types("chola_sword_infantry_levy", "chola_sword_infantry_legion", "CHL")

	# chera_units.write_file()
	# chera_units.add_unit_types("chera_sword_infantry_levy", "chera_sword_infantry_legion", "CHR")

	# tamil_units.write_file()
	# tamil_units.add_unit_types("tamil_sword_infantry_levy", "tamil_sword_infantry_legion", "tamil")
	# tamil_units.add_unit_types("tamil_sword_infantry_levy", "tamil_sword_infantry_legion", "cheran")
	# tamil_units.add_unit_types("tamil_sword_infantry_levy", "tamil_sword_infantry_legion", "cholan")
	# tamil_units.add_unit_types("tamil_sword_infantry_levy", "tamil_sword_infantry_legion", "pandyan")

	lanka_units.write_file()
	lanka_units.add_unit_types("lanka_sword_infantry_levy", "lanka_sword_infantry_legion", "ANU")
	lanka_units.add_unit_types("lanka_sword_infantry_levy", "lankan_generic_infantry_legion", "lankan")
