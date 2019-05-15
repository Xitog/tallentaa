UNIT_DEFINITIONS = {
    'all' : [
        'barrack',
        'factory',
        'generator',
        'extractor',
        'soldier',
    ],
    'buildings' : [
        'barrack',
        'factory',
        'generator',
        'extractor',
    ],
    'soldier' : {
        'vision' : 3,
        'speed' : 3,
        'width' : 1,
        'height' : 1,
        'mod_x' : 0,
        'mod_y' : 0,
        'creation_time' : 150,
        'available_orders': [Move, Attack],
        'life' : 50,
        'regen_life' : 0,
        'shield' : 0,
        'regen_shield' : 0,
        'mana' : 0,
        'regen_mana' : 0,
        'armor' : 0,
        'cost' : {
            'energy' : 20,
            'matter' : 10,
        }
        'weapon' : 'laser2000',
        'reload' : 3,
        'shadow' : False,
        'is_aerial' : False,
        'is_movable' : True,
        'is_building' : False,
        'is_builder' : False,
        'is_creator' : False,
        'is_producer' : False
    },
    'barrack' : {
        'speed' : 0,
        'width' : 3,
        'height' : 3,
        'mod_x' : 0,
        'mod_y' : 0,
        'order_start_row_mod' : 3,
        'order_start_col_mod' : 1,
        'available_orders': [Move, Attack, CreateSoldier, CreateScout, CreateBuilder],
        'max_life' : 300,
        'cost' : {
            'energy' : 20,
            'matter' : 10,
        }
    },
    'factory' : {
        'speed' : 0,
        'width' : 3,
        'height' : 3,
        'mod_x' : 0,
        'mod_y' : 0,
        'order_start_row_mod' : 3,
        'order_start_col_mod' : 1,
        'available_orders': [Move, Attack, CreateSoldier, CreateScout, CreateBuilder],
        'max_life' : 450,
        'cost' : {
            'energy' : 40,
            'matter' : 20,
        }
    },
    'generator' : {
        'speed' : 100,
        'width' : 1,
        'height' : 1,
        'mod_x' : 0,
        'mod_y' : -32,
        'order_start_row_mod' : 3,
        'order_start_col_mod' : 1,
        'available_orders': [],
        'max_life' : 100,
        'cost' : {
            'energy' : 20,
            'matter' : 10,
        }
    },
    'extractor' : {
        'speed' : 100,
        'width' : 1,
        'height' : 1,
        'mod_x' : 0,
        'mod_y' : -32,
        'order_start_row_mod' : 3,
        'order_start_col_mod' : 1,
        'available_orders': [],
        'max_life' : 100,
        'cost' : {
            'energy' : 20,
            'matter' : 10,
        }
    }
}
WEAPON_DEFINITIONS = {
    'laser2000' : {
        'name' : 'laser2000',
        'range' : 4,
        'dommage' : 10,
        'kind' : 'laser'
    }
}
