# classes_data.py

data = {
    "characters": {
        "player": {
            "health": 100,
            "defense": 5,
            "magic": 10,
            "mana": 100,
            "acceleration": 2.0,
            "level": 1,
            "experience": 0,
            "attacks": {
                "basic_attack": 10,
                "special_attack": 20,
            },
            "projectiles": ["fireball", "ice_arrow"],
            "graphic": "player_graphic",  # Name of the graphic resource
        },
    },
    "projectiles": {
        "fireball": {
            "speed": 10,
            "damage": 15,
            "size": (10, 10),
            "color_data": {"active": (255, 0, 0)},
            "graphic": "fireball_graphic",  # Name of the graphic resource
        },
        "ice_arrow": {
            "speed": 8,
            "damage": 20,
            "size": (12, 12),
            "color_data": {"active": (0, 0, 255)},
            "graphic": "ice_arrow_graphic",  # Name of the graphic resource
        },
        # Add more projectiles as needed
    },
}
