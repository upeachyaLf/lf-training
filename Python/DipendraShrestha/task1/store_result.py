import argparse
import json

subjects = ["English", "Nepali", "Mathematics"]
parser = argparse.ArgumentParser()

arg_options = [(("--name", "-n"), {"type": str, "required": True}),
               (("--dob", "-d"), {"type": str, "required": True}),
               (("--score", "-s"), {"type": float, "required": True}),
               (("--total", "-t"), {"type": int, "required": True}),
               (("--subject", "-sub"), {"type": str,
                                        "required": True, "choices": subjects}),
               (("--store", "-S"), {"type": str, "required": True})]

for option in arg_options:
    parser.add_argument(*option[0], **option[1])

arg_values = parser.parse_args()
record_key = (arg_values.name, arg_values.dob, arg_values.subject)
results = {}

try:
    with open(arg_values.store, "r") as results_file:
        results = json.load(results_file)
except json.JSONDecodeError:
    pass

results[str(record_key)] = vars(arg_values)

with open("results.txt", "w") as results_file:
    json.dump(results, results_file)
