import json
import random
from pathlib import Path

names = [{"name": "speed", "unit": "km/h"}, {"name": "max_torque", "unit": "Nm"}, {"name": "min_torque", "unit": "Nm"}, {"name": "thermal_limit", "unit": "°C"}, {"name": "max_power", "unit": "kW"}, {"name": "min_power", "unit": "kW"}, {"name": "motor_efficiency", "unit": "%"}, {"name": "gear_ratio", "unit": ""}, {"name": "voltage", "unit": "V"}, {"name": "current", "unit": "A"}, {"name": "temperature", "unit": "°C"}, {"name": "vibration_level", "unit": "mm/s"}, {"name": "noise_level", "unit": "dB"}, {"name": "load_capacity", "unit": "kg"}, {"name": "duty_cycle", "unit": "%"}, {"name": "operating_time", "unit": "hours"}, {"name": "maintenance_interval", "unit": "km"}]
for name in names:
    name["min"] = random.randint(-100, 100)
    name["max"] = random.randint(name["min"], 500)
    name["value"] = random.randint(name["min"], name["max"])

maps =[{"name": "temp_curve", "unit":"C"}, {"name": "torque_curve", "unit":"Nm"}, {"name": "power_curve", "unit":"kW"}]
for map in maps:
    map["min"] = random.randint(-100, 100)
    map["max"] = random.randint(map["min"], 500)
    map["points"] = [{"x": i, "y": random.randint(map["min"], map["max"])} for i in range(10)]


data = names + maps
n=1
script_dir = Path(__file__).parent
file_name = script_dir / f"params_v{n}.json"
while Path(file_name).exists():
    n += 1
    file_name = script_dir / f"params_v{n}.json"
with open(file_name, "w") as f:
    json.dump(data, f, indent=4)
