import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("-S", "--store", type=str, required=True)
arg_values = parser.parse_args()
results = {}

try:
    with open(arg_values.store, "r") as results_file:
        results = json.load(results_file)
        results = {eval(key): value for key, value in results.items()}
except FileNotFoundError:
    print(f"{arg_values.store} doesn't exists!")
except json.JSONDecodeError:
    print(f"{arg_values.store} doesn't contain any result records!")

grouped_results = {}

for record_key in results:
    group_key = (record_key[0], record_key[1])

    if group_key in grouped_results:
        grouped_results[group_key].append(results[record_key])
    else:
        grouped_results[group_key] = [results[record_key]]

for group_key in grouped_results:
    print("==========================================================")

    total_score = 0
    total_fullmarks = 0

    print(f"Name: {group_key[0]}")
    print(f"DOB: {group_key[1]}")

    for record in grouped_results[group_key]:
        total_score += record["score"]
        total_fullmarks += record["total"]

        print(f"{record['subject']}:")
        print(f"\tScore: {record['score']}")
        print(f"\tTotal: {record['total']}")
        print(f"\tPercentage: {record['score'] * 100 / record['total']}")

    print(f"Total Percentage: {total_score * 100/ total_fullmarks}")
    print("==========================================================\n")
