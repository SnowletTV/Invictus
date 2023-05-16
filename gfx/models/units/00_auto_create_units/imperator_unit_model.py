from jinja2 import Template

"""
	There are 3 entities in a (typical) unit asset file, a spear unit and a light and heavy sword unit.
	Each entity has the following required parameters:
	1. name
	2. mesh
	3. weapon
	4. spear
	5. shield
	6. drill_post

	Each entity has the following optional parameters:
	1. head

"""

unit_model = Template('''
{% if header != "" %}{{header}}{% endif %}
{% if entity_one_name != "" %}entity = {
	name = "{{entity_one_name}}"
	pdxmesh = "{{entity_one_mesh}}"
	Scale = 0.1
	default_state = "idle"
	state = {
		name = "idle"
		animation = "idle_2_base_animation"
		looping = no
		chance = 5
		next_state = "idle"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "idle"
		animation = "idle_2_var_1_animation"
		looping = no
		chance = 1
		next_state = "idle"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "move"
		animation = "moving_2_animation"
		start_event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_generic_walk"}}
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "force_march"
		animation = "force_march_2_animation"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" }
		start_event = { node = THE_RIG:back_node_1 entity = "{{entity_one_shield}}" }
		start_event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_generic_walk"}}
	}
	state = {
		name = "retreat"
		animation = "retreat_2_animation"
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
		start_event = {sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_retreat"}}
	}
	state = {
		name = "raiding"
		animation = "raiding_2_animation"
		looping = no
		next_state = "idle"
		event = { time = 0.0 node = THE_RIG:Right_hand_node_1 entity = "torch_01_entity" attachment_id = "raiding_torch_1" entity_fade_speed = 1.0 life = 5 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
		event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_raiding"}}
		event = { time = 2.8 node = THE_RIG:root particle = "units/raiding_ground_fire_01_effect" keep_particle = yes trigger_once = no life = 1 }
	}
	state = {
		name = "recruiting"
		animation = "recruiting_loop_animation"
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_spear}}" attachment_id = "recruit_banner_1" entity_fade_speed = 0.5 }
	}
	state = {
		name = "recruit"
		animation = "recruiting_action_animation"
		looping = no
		next_state = "idle"
		event = { time = 0.0 node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_spear}}" attachment_id = "recruit_banner_1" entity_fade_speed = 0.5 }
	}
	state = {
		name = "build_road_2"
		animation = "build_road_shoveling_animation"
		looping = no
		event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_build_road_loop"}}
		next_state = "build_road_2"
		chance = {
			if_current_state = {
				"build_road" = 100
				"build_road_2" = 100
			}
		}
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "shovel_01_entity" }
	}
	state = {
		name = "build_road_2"
		animation = "build_road_pre_moving_animation"
		looping = no
		event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_build_road_post"}}
		next_state = "build_road"
		chance = {
			if_current_state = {
				"build_road" = 0
				"build_road_2" = 50
			}
		}
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "shovel_01_entity" }
	}
	state = {
		name = "build_road"
		animation = "build_road_moving_animation"
		looping = no
		start_event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_generic_walk"}}
		next_state = "build_road"
		chance = {
			if_current_state = {
				"build_road" = 100
				"build_road_2" = 100
				"idle" = 100
				"move" = 100
				"retreat" = 100
				"force_march" = 100
			}
		}
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "shovel_01_entity" }
	}
	state = {
		name = "build_road"
		animation = "build_road_post_moving_animation"
		looping = no
		event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_build_road_pre"}}
		next_state = "build_road_2"
		chance = {
			if_current_state = {
				"build_road" = 50
				"build_road_2" = 0
				"idle" = 0
				"move" = 0
				"retreat" = 0
				"force_march" = 0
			}
		}
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "shovel_01_entity" }
	}
	state = {
		name = "combat_ready"
		animation = "combat_ready_2"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "army_drill"
		animation = "army_drill_2_animation"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = army_drill }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
		start_event = { node = THE_RIG:root entity = "{{entity_one_drill_post}}" state = attack }
		event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_drill2"}}
	}
	state = {
		name = "cheer"
		animation = "idle_1_base_animation"
	}
	##############
	#### Offensive combat
	##############
	state = {
		name = "offensive_successful"
		animation = "weapon_2_offensive_successful"
		chance = 1
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = offensive_successful }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "offensive_dodge"
		animation = "weapon_2_offensive_dodge"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = offensive_dodge }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "offensive_block"
		animation = "weapon_2_offensive_block"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = offensive_block }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "offensive_counter"
		animation = "weapon_2_offensive_counter"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = offensive_counter }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	### Alternative attacks (slash) ###
	state = {
		name = "offensive_successful"
		animation = "weapon_2_alt_offensive_successful"
		chance = 1
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = offensive_successful_alt }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "offensive_dodge"
		animation = "weapon_2_alt_offensive_dodge"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = offensive_dodge_alt }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "offensive_block"
		animation = "weapon_2_alt_offensive_block"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = offensive_block_alt }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "offensive_counter"
		animation = "weapon_2_alt_offensive_counter"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = offensive_counter_alt }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "offensive_sequence_1"
		animation = "weapon_2_offensive_sequence_1"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = offensive_sequence_1 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "offensive_sequence_2"
		animation = "weapon_2_offensive_sequence_2"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = offensive_sequence_2 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "offensive_sequence_3"
		animation = "weapon_2_offensive_sequence_3"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" attachment_id = "main_weapon" state = offensive_sequence_3 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
		event = { time = 4.18 node = THE_RIG:world_node_1 entity = "{{entity_one_weapon}}" attachment_id = "main_weapon" life = 2.88 }
		event = { time = 7.05 node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" attachment_id = "main_weapon" life = 0.95 }
		event = { time = 7.95 remove_attachment = "main_weapon" }
	}
	state = {
		name = "offensive_sequence_4"
		animation = "weapon_2_offensive_sequence_4"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = offensive_sequence_4 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "offensive_sequence_5"
		animation = "weapon_2_offensive_sequence_5"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = offensive_sequence_5 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	##############
	# Defensive combat
	##############
	state = {
		name = "defensive_hit"
		animation = "weapon_2_defensive_hit"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = defensive_hit }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "defensive_dodge"
		animation = "weapon_2_defensive_dodge"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = defensive_dodge }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "defensive_block"
		animation = "weapon_2_defensive_block"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = defensive_block }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "defensive_counter"
		animation = "weapon_2_defensive_counter"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = defensive_counter }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "defensive_sequence_1"
		animation = "weapon_2_defensive_sequence_1"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = defensive_sequence_1 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "defensive_sequence_2"
		animation = "weapon_2_defensive_sequence_2"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = defensive_sequence_2 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "defensive_sequence_3"
		animation = "weapon_2_defensive_sequence_3"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = defensive_sequence_3 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "defensive_sequence_4"
		animation = "weapon_2_defensive_sequence_4"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = defensive_sequence_4 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	state = {
		name = "defensive_sequence_5"
		animation = "weapon_2_defensive_sequence_5"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_one_weapon}}" state = defensive_sequence_5 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_one_shield}}" }
	}
	{% if entity_one_head != "" %}attach = { THE_RIG:Character1_Head = "{{entity_one_head}}" }{% endif %}
}{% endif %}
{% if entity_two_name != "" %}
entity = {
	name = "{{entity_two_name}}"
	pdxmesh = "{{entity_two_mesh}}"
	Scale = 0.1
	default_state = "idle"
	state = {
		name = "idle"
		animation = "idle_2_base_animation"
		looping = no
		chance = 5
		next_state = "idle"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "idle"
		animation = "idle_2_var_1_animation"
		looping = no
		chance = 1
		next_state = "idle"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "move"
		animation = "moving_2_animation"
		start_event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_generic_walk"}}
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "force_march"
		animation = "force_march_2_animation"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" }
		start_event = { node = THE_RIG:back_node_1 entity = "{{entity_two_shield}}" }
		start_event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_generic_walk"}}
	}
	state = {
		name = "retreat"
		animation = "retreat_2_animation"
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
		start_event = {sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_retreat"}}
	}
	state = {
		name = "raiding"
		animation = "raiding_2_animation"
		looping = no
		next_state = "idle"
		event = { time = 0.0 node = THE_RIG:Right_hand_node_1 entity = "torch_01_entity" attachment_id = "raiding_torch_1" entity_fade_speed = 1.0 life = 5 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
		event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_raiding"}}
		event = { time = 2.8 node = THE_RIG:root particle = "units/raiding_ground_fire_01_effect" keep_particle = yes trigger_once = no life = 1 }
	}
	state = {
		name = "recruiting"
		animation = "recruiting_loop_animation"
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_spear}}" attachment_id = "recruit_banner_1" entity_fade_speed = 0.5 }
	}
	state = {
		name = "recruit"
		animation = "recruiting_action_animation"
		looping = no
		next_state = "idle"
		event = { time = 0.0 node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_spear}}" attachment_id = "recruit_banner_1" entity_fade_speed = 0.5 }
	}
	state = {
		name = "build_road_2"
		animation = "build_road_shoveling_animation"
		looping = no
		event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_build_road_loop"}}
		next_state = "build_road_2"
		chance = {
			if_current_state = {
				"build_road" = 100
				"build_road_2" = 100
			}
		}
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "shovel_01_entity" }
	}
	state = {
		name = "build_road_2"
		animation = "build_road_pre_moving_animation"
		looping = no
		event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_build_road_post"}}
		next_state = "build_road"
		chance = {
			if_current_state = {
				"build_road" = 0
				"build_road_2" = 50
			}
		}
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "shovel_01_entity" }
	}
	state = {
		name = "build_road"
		animation = "build_road_moving_animation"
		looping = no
		start_event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_generic_walk"}}
		next_state = "build_road"
		chance = {
			if_current_state = {
				"build_road" = 100
				"build_road_2" = 100
				"idle" = 100
				"move" = 100
				"retreat" = 100
				"force_march" = 100
			}
		}
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "shovel_01_entity" }
	}
	state = {
		name = "build_road"
		animation = "build_road_post_moving_animation"
		looping = no
		event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_build_road_pre"}}
		next_state = "build_road_2"
		chance = {
			if_current_state = {
				"build_road" = 50
				"build_road_2" = 0
				"idle" = 0
				"move" = 0
				"retreat" = 0
				"force_march" = 0
			}
		}
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "shovel_01_entity" }
	}
	state = {
		name = "combat_ready"
		animation = "combat_ready_2"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "army_drill"
		animation = "army_drill_2_animation"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = army_drill }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
		start_event = { node = THE_RIG:root entity = "{{entity_two_drill_post}}" state = attack }
		event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_drill2"}}
	}
	state = {
		name = "cheer"
		animation = "idle_1_base_animation"
	}
	##############
	#### Offensive combat
	##############
	state = {
		name = "offensive_successful"
		animation = "weapon_2_offensive_successful"
		chance = 1
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = offensive_successful }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "offensive_dodge"
		animation = "weapon_2_offensive_dodge"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = offensive_dodge }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "offensive_block"
		animation = "weapon_2_offensive_block"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = offensive_block }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "offensive_counter"
		animation = "weapon_2_offensive_counter"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = offensive_counter }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	### Alternative attacks (slash) ###
	state = {
		name = "offensive_successful"
		animation = "weapon_2_alt_offensive_successful"
		chance = 1
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = offensive_successful_alt }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "offensive_dodge"
		animation = "weapon_2_alt_offensive_dodge"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = offensive_dodge_alt }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "offensive_block"
		animation = "weapon_2_alt_offensive_block"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = offensive_block_alt }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "offensive_counter"
		animation = "weapon_2_alt_offensive_counter"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = offensive_counter_alt }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "offensive_sequence_1"
		animation = "weapon_2_offensive_sequence_1"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = offensive_sequence_1 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "offensive_sequence_2"
		animation = "weapon_2_offensive_sequence_2"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = offensive_sequence_2 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "offensive_sequence_3"
		animation = "weapon_2_offensive_sequence_3"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" attachment_id = "main_weapon" state = offensive_sequence_3 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
		event = { time = 4.18 node = THE_RIG:world_node_1 entity = "{{entity_two_weapon}}" attachment_id = "main_weapon" life = 2.88 }
		event = { time = 7.05 node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" attachment_id = "main_weapon" life = 0.95 }
		event = { time = 7.95 remove_attachment = "main_weapon" }
	}
	state = {
		name = "offensive_sequence_4"
		animation = "weapon_2_offensive_sequence_4"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = offensive_sequence_4 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "offensive_sequence_5"
		animation = "weapon_2_offensive_sequence_5"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = offensive_sequence_5 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	##############
	# Defensive combat
	##############
	state = {
		name = "defensive_hit"
		animation = "weapon_2_defensive_hit"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = defensive_hit }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "defensive_dodge"
		animation = "weapon_2_defensive_dodge"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = defensive_dodge }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "defensive_block"
		animation = "weapon_2_defensive_block"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = defensive_block }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "defensive_counter"
		animation = "weapon_2_defensive_counter"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = defensive_counter }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "defensive_sequence_1"
		animation = "weapon_2_defensive_sequence_1"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = defensive_sequence_1 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "defensive_sequence_2"
		animation = "weapon_2_defensive_sequence_2"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = defensive_sequence_2 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "defensive_sequence_3"
		animation = "weapon_2_defensive_sequence_3"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = defensive_sequence_3 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "defensive_sequence_4"
		animation = "weapon_2_defensive_sequence_4"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = defensive_sequence_4 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	state = {
		name = "defensive_sequence_5"
		animation = "weapon_2_defensive_sequence_5"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_two_weapon}}" state = defensive_sequence_5 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_two_shield}}" }
	}
	{% if entity_two_head != "" %}attach = { THE_RIG:Character1_Head = "{{entity_two_head}}" }{% endif %}
}{% endif %}
{% if entity_three_name != "" %}
entity = {
	name = "{{entity_three_name}}"
	pdxmesh = "{{entity_three_mesh}}"
	Scale = 0.1
	default_state = "idle"
	state = {
		name = "idle"
		animation = "idle_2_base_animation"
		looping = no
		chance = 5
		next_state = "idle"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "idle"
		animation = "idle_2_var_1_animation"
		looping = no
		chance = 1
		next_state = "idle"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "move"
		animation = "moving_2_animation"
		start_event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_generic_walk"}}
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "force_march"
		animation = "force_march_2_animation"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" }
		start_event = { node = THE_RIG:back_node_1 entity = "{{entity_three_shield}}" }
		start_event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_generic_walk"}}
	}
	state = {
		name = "retreat"
		animation = "retreat_2_animation"
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
		start_event = {sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_retreat"}}
	}
	state = {
		name = "raiding"
		animation = "raiding_2_animation"
		looping = no
		next_state = "idle"
		event = { time = 0.0 node = THE_RIG:Right_hand_node_1 entity = "torch_01_entity" attachment_id = "raiding_torch_1" entity_fade_speed = 1.0 life = 5 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
		event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_raiding"}}
		event = { time = 2.8 node = THE_RIG:root particle = "units/raiding_ground_fire_01_effect" keep_particle = yes trigger_once = no life = 1 }
	}
	state = {
		name = "recruiting"
		animation = "recruiting_loop_animation"
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_spear}}" attachment_id = "recruit_banner_1" entity_fade_speed = 0.5 }
	}
	state = {
		name = "recruit"
		animation = "recruiting_action_animation"
		looping = no
		next_state = "idle"
		event = { time = 0.0 node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_spear}}" attachment_id = "recruit_banner_1" entity_fade_speed = 0.5 }
	}
	state = {
		name = "build_road_2"
		animation = "build_road_shoveling_animation"
		looping = no
		event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_build_road_loop"}}
		next_state = "build_road_2"
		chance = {
			if_current_state = {
				"build_road" = 100
				"build_road_2" = 100
			}
		}
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "shovel_01_entity" }
	}
	state = {
		name = "build_road_2"
		animation = "build_road_pre_moving_animation"
		looping = no
		event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_build_road_post"}}
		next_state = "build_road"
		chance = {
			if_current_state = {
				"build_road" = 0
				"build_road_2" = 50
			}
		}
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "shovel_01_entity" }
	}
	state = {
		name = "build_road"
		animation = "build_road_moving_animation"
		looping = no
		start_event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_generic_walk"}}
		next_state = "build_road"
		chance = {
			if_current_state = {
				"build_road" = 100
				"build_road_2" = 100
				"idle" = 100
				"move" = 100
				"retreat" = 100
				"force_march" = 100
			}
		}
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "shovel_01_entity" }
	}
	state = {
		name = "build_road"
		animation = "build_road_post_moving_animation"
		looping = no
		event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_build_road_pre"}}
		next_state = "build_road_2"
		chance = {
			if_current_state = {
				"build_road" = 50
				"build_road_2" = 0
				"idle" = 0
				"move" = 0
				"retreat" = 0
				"force_march" = 0
			}
		}
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "shovel_01_entity" }
	}
	state = {
		name = "combat_ready"
		animation = "combat_ready_2"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "army_drill"
		animation = "army_drill_2_animation"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = army_drill }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
		start_event = { node = THE_RIG:root entity = "{{entity_three_drill_post}}" state = attack }
		event = { sound = { soundeffect = "event:/SFX/Animations/Units/Generic/sfx_anim_unit_drill2"}}
	}
	state = {
		name = "cheer"
		animation = "idle_1_base_animation"
	}
	##############
	#### Offensive combat
	##############
	state = {
		name = "offensive_successful"
		animation = "weapon_2_offensive_successful"
		chance = 1
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = offensive_successful }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "offensive_dodge"
		animation = "weapon_2_offensive_dodge"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = offensive_dodge }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "offensive_block"
		animation = "weapon_2_offensive_block"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = offensive_block }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "offensive_counter"
		animation = "weapon_2_offensive_counter"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = offensive_counter }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	### Alternative attacks (slash) ###
	state = {
		name = "offensive_successful"
		animation = "weapon_2_alt_offensive_successful"
		chance = 1
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = offensive_successful_alt }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "offensive_dodge"
		animation = "weapon_2_alt_offensive_dodge"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = offensive_dodge_alt }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "offensive_block"
		animation = "weapon_2_alt_offensive_block"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = offensive_block_alt }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "offensive_counter"
		animation = "weapon_2_alt_offensive_counter"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = offensive_counter_alt }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "offensive_sequence_1"
		animation = "weapon_2_offensive_sequence_1"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = offensive_sequence_1 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "offensive_sequence_2"
		animation = "weapon_2_offensive_sequence_2"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = offensive_sequence_2 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "offensive_sequence_3"
		animation = "weapon_2_offensive_sequence_3"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" attachment_id = "main_weapon" state = offensive_sequence_3 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
		event = { time = 4.18 node = THE_RIG:world_node_1 entity = "{{entity_three_weapon}}" attachment_id = "main_weapon" life = 2.88 }
		event = { time = 7.05 node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" attachment_id = "main_weapon" life = 0.95 }
		event = { time = 7.95 remove_attachment = "main_weapon" }
	}
	state = {
		name = "offensive_sequence_4"
		animation = "weapon_2_offensive_sequence_4"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = offensive_sequence_4 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "offensive_sequence_5"
		animation = "weapon_2_offensive_sequence_5"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = offensive_sequence_5 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	##############
	# Defensive combat
	##############
	state = {
		name = "defensive_hit"
		animation = "weapon_2_defensive_hit"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = defensive_hit }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "defensive_dodge"
		animation = "weapon_2_defensive_dodge"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = defensive_dodge }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "defensive_block"
		animation = "weapon_2_defensive_block"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = defensive_block }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "defensive_counter"
		animation = "weapon_2_defensive_counter"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = defensive_counter }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "defensive_sequence_1"
		animation = "weapon_2_defensive_sequence_1"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = defensive_sequence_1 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "defensive_sequence_2"
		animation = "weapon_2_defensive_sequence_2"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = defensive_sequence_2 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "defensive_sequence_3"
		animation = "weapon_2_defensive_sequence_3"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = defensive_sequence_3 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "defensive_sequence_4"
		animation = "weapon_2_defensive_sequence_4"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = defensive_sequence_4 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	state = {
		name = "defensive_sequence_5"
		animation = "weapon_2_defensive_sequence_5"
		start_event = { node = THE_RIG:Right_hand_node_1 entity = "{{entity_three_weapon}}" state = defensive_sequence_5 }
		start_event = { node = THE_RIG:Left_hand_node_1 entity = "{{entity_three_shield}}" }
	}
	{% if entity_three_head != "" %}attach = { THE_RIG:Character1_Head = "{{entity_three_head}}" }{% endif %}
}{% endif %}
''')

unit_types = Template('''
entity ={
	name = "{{target}}_levy_archers"
	clone = "{{light}}"
}
entity ={
	name = "{{target}}_legion_archers"
	clone = "{{heavy}}"
}
entity ={
	name = "{{target}}_levy_camels"
	clone = "{{light}}"
}
entity ={
	name = "{{target}}_legion_camels"
	clone = "{{heavy}}"
}
entity ={
	name = "{{target}}_levy_chariots"
	clone = "{{light}}"
}
entity ={
	name = "{{target}}_legion_chariots"
	clone = "{{heavy}}"
}
entity ={
	name = "{{target}}_levy_engineer_cohort"
	clone = "{{light}}"
}
entity ={
	name = "{{target}}_legion_engineer_cohort"
	clone = "{{heavy}}"
}
entity ={
	name = "{{target}}_levy_heavy_cavalry"
	clone = "{{light}}"
}
entity ={
	name = "{{target}}_legion_heavy_cavalry"
	clone = "{{heavy}}"
}
entity ={
	name = "{{target}}_levy_heavy_infantry"
	clone = "{{light}}"
}
entity ={
	name = "{{target}}_legion_heavy_infantry"
	clone = "{{heavy}}"
}
entity ={
	name = "{{target}}_levy_horse_archers"
	clone = "{{light}}"
}
entity ={
	name = "{{target}}_legion_horse_archers"
	clone = "{{heavy}}"
}
entity ={
	name = "{{target}}_levy_light_cavalry"
	clone = "{{light}}"
}
entity ={
	name = "{{target}}_legion_light_cavalry"
	clone = "{{heavy}}"
}
entity ={
	name = "{{target}}_levy_light_infantry"
	clone = "{{light}}"
}
entity ={
	name = "{{target}}_legion_light_infantry"
	clone = "{{heavy}}"
}
entity ={
	name = "{{target}}_levy_supply_train"
	clone = "{{light}}"
}
entity ={
	name = "{{target}}_legion_supply_train"
	clone = "{{heavy}}"
}
entity ={
	name = "{{target}}_levy_warelephant"
	clone = "{{light}}"
}
entity ={
	name = "{{target}}_legion_warelephant"
	clone = "{{heavy}}"
}
''')

class UnitModel:
	""" Imperator Rome unit model """

	def __init__(self,
		filename,
		header="",
		entity_one_name="",
		entity_one_mesh="",
		entity_one_weapon="",
		entity_one_spear="",
		entity_one_shield="",
		entity_one_drill_post="",
		entity_one_head="",
		entity_two_name="",
		entity_two_mesh="",
		entity_two_weapon="",
		entity_two_spear="",
		entity_two_shield="",
		entity_two_drill_post="",
		entity_two_head="",
		entity_three_name="",
		entity_three_mesh="",
		entity_three_weapon="",
		entity_three_spear="",
		entity_three_shield="",
		entity_three_drill_post="",
		entity_three_head=""):

		self.filename = filename + ".asset"
		self.unit_model = unit_model.render(
			header=header,
			entity_one_name=entity_one_name,
			entity_one_mesh=entity_one_mesh,
			entity_one_weapon=entity_one_weapon,
			entity_one_spear=entity_one_spear,
			entity_one_shield=entity_one_shield,
			entity_one_drill_post=entity_one_drill_post,
			entity_one_head=entity_one_head,
			entity_two_name=entity_two_name,
			entity_two_mesh=entity_two_mesh,
			entity_two_weapon=entity_two_weapon,
			entity_two_spear=entity_two_spear,
			entity_two_shield=entity_two_shield,
			entity_two_drill_post=entity_two_drill_post,
			entity_two_head=entity_two_head,
			entity_three_name=entity_three_name,
			entity_three_mesh=entity_three_mesh,
			entity_three_weapon=entity_three_weapon,
			entity_three_spear=entity_three_spear,
			entity_three_shield=entity_three_shield,
			entity_three_drill_post=entity_three_drill_post,
			entity_three_head=entity_three_head
		)[1:]

	def write_file(self):
		with open(self.filename, "w") as file:
			file.write(self.unit_model)

	def add_unit_types(self, light, heavy, target):
		with open(self.filename, "a") as file:
			file.write(unit_types.render(light=light, heavy=heavy, target=target))
