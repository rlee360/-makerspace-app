

machine_docs = [
    ["FDM 1", "FDM", "FDM", "Prusa", "i3 MK3", [210, 210, 250], False, [], []],
    ["FDM 2", "FDM", "Prusa", "i3 MK3", [210, 210, 250], False, [], []],
    ["FDM 3", "FDM", "Prusa", "i3 MK3", [210, 210, 250], False, [], []],
    ["FDM 4", "FDM", "Prusa", "i3 MK3", [210, 210, 250], True, ["x belt is too loose."], []],
    ["FDM 5", "FDM", "Prusa", "i3 MK3", [210, 210, 250], False, [], []],
    ["FDM 6", "FDM", "Prusa", "i3 MK3", [210, 210, 250], False, [], []],
    ["FDM 7", "FDM", "Tinkerine", "Ditto Pro", [215, 165, 220], True, ["bed needs to be leveled", "nozzle is clogged"], []],

    ["SLA 1", "SLA", "Elegoo", "Mars", [120, 68, 155], False, [], []],

    ["Laser 1", "Laser", "Glowforge", "Pro", [304, 518, 0.6], False, [], []]
]

material_docs = [
    {
        "type": "filament",
        "material": "PLA",
        "color": "black",
        "brand": "Inland",
        "grams_remaining": 300,
        "link": "https://www.microcenter.com/product/632388/inland-175mm-black-pla-pro-3d-printer-filament-1kg-spool-(22-lbs)",
        "notes": [],
        "valid_machines": ["FDM 1", "FDM 2", "FDM 3", "FDM 4", "FDM 5", "FDM 6"],
        "price": 18.99,
        "operator_notes": []
    },
    {
        "type": "filament",
        "material": "PLA",
        "color": "black",
        "brand": "Inland",
        "grams_remaining": 950,
        "link": "https://www.microcenter.com/product/632389/inland-175mm-white-pla-pro-3d-printer-filament-1kg-spool-(22-lbs)",
        "notes": [],
        "valid_machines": ["FDM 1", "FDM 2", "FDM 3", "FDM 4", "FDM 5", "FDM 6"],
        "price": 18.99,
        "operator_notes": ["Seem to have complaints about poor outer wall finish. Might be inaccurate filament"]
    },
    {
        "type": "filament",
        "material": "PETG",
        "color": "white",
        "brand": "Atomic",
        "grams_remaining": 1000,
        "link": "https://atomicfilament.com/products/bright-white-opaque-petg-pro?_pos=1&_sid=b3a57fe67&_ss=r&variant=11046098497",
        "notes": [],
        "valid_machines": ["FDM 4", "FDM 5", "FDM 6"],
        "price": 32.99,
        "operator_notes": ["Expensive, but prints really well"]
    },
    {
        "type": "filament",
        "material": "ABS",
        "color": "blue",
        "brand": "Hatchbox",
        "grams_remaining": 800,
        "link": "https://www.amazon.com/HATCHBOX-3D-Filament-Dimensional-Accuracy/dp/B00J0H3PG0/?th=1",
        "notes": ["Models with small bases prone to failing due to warping."],
        "valid_machines": ["FDM 6"],
        "price": 21.99,
        "operator_notes": ["Excessive warping, do not buy again."]
    }
]
