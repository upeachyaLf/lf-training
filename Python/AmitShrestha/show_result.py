import argparse
import datetime

parser = argparse.ArgumentParser(description="Result Parser")
parser.add_argument("--store", required=True, help="File Name")


def main(args):
    file_name = vars(args)["store"]

    all_results = read_file(file_name)

    display_results(all_results)


def read_file(file_name):
    all_results = []

    with open(file_name, mode="r") as open_file:
        for line in open_file:
            items = line.split(",")
            index = find_index(all_results, items[0])
            if index is not None:
                all_results[index]["Subjects"].append(
                    {
                        "Name": items[2],
                        "Score": items[3],
                        "Total": items[4],
                        "Percentage": items[5],
                    }
                )
            else:
                all_results.append(
                    {
                        "Name": items[0],
                        "DOB": datetime.datetime.strptime(
                            items[1], "%Y-%m-%d"
                        ).strftime("%d-%b-%Y"),
                        "Subjects": [
                            {
                                "Name": items[2],
                                "Score": items[3],
                                "Total": items[4],
                                "Percentage": items[5],
                            }
                        ],
                    }
                )

    return all_results


def find_index(lst, name):
    for index, dic in enumerate(lst):
        if dic["Name"] == name:
            return index

    return None


def display_results(results):
    for result in results:
        for key, value in result.items():
            if key != "Subjects":
                print(key + ": " + value)
            else:
                percentage = []
                print("Subjects:")
                for subject in value:
                    percentage.append(float(subject["Percentage"]))
                    print("\t" + subject["Name"] + ":")
                    print("\t\tScore: " + subject["Score"])
                    print("\t\tTotal: " + subject["Total"])
                    print("\t\tPercentage: " + subject["Percentage"])
                print(
                    "Average Percentage: ", calc_average_percentage(percentage), "\n\n"
                )


def calc_average_percentage(percentage_list):
    return sum(percentage_list) / len(percentage_list)


if __name__ == "__main__":
    main(parser.parse_args())

