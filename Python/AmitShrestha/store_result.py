import os
import datetime
import argparse
import collections


def dob_parser(string_date):
    try:
        return datetime.datetime.strptime(string_date, "%d/%m/%Y").date()
    except:
        raise


parser = argparse.ArgumentParser(description="Result Parser")
parser.add_argument("--name", required=True, type=str, help="Name")
parser.add_argument(
    "--dob", required=True, type=dob_parser, help="Date of Birth in dd/mm/YYYY format"
)
parser.add_argument("--score", required=True, type=float, help="Score")
parser.add_argument("--total", required=True, type=float, help="Total")
parser.add_argument(
    "--subject",
    required=True,
    choices=["English", "Nepali", "Mathematics", "Science"],
    type=str,
    help="Subject",
)
parser.add_argument("--store", required=True, type=str, help="File Name")


def main(args):
    raw_result = vars(args)

    update_or_create_file(process_result(raw_result), raw_result["store"])


def process_result(values):
    processed_result = []
    ordered_result = collections.OrderedDict(
        name=values["name"],
        dob=values["dob"],
        subject=values["subject"],
        score=values["score"],
        total=values["total"],
        store=values["store"],
    )

    for key, value in ordered_result.items():
        if key != "store":
            processed_result.append(str(value))

    processed_result.append(str(calc_percentage(values["score"], values["total"])))

    return ",".join(processed_result)


def calc_percentage(score, total):
    return (score / total) * 100


def update_or_create_file(result, file_name):
    if os.path.exists(file_name):
        file_updated = False
        new_result = result.split(",")
        with open(file_name, mode="r") as open_file:
            lines = open_file.readlines()
            if len(lines):
                for index, line in enumerate(lines):
                    items = line.split(",")

                    if items[0] == new_result[0] and items[2] == new_result[2]:
                        lines[index] = result + "\n"
                        write_lines(lines, file_name)
                        file_updated = True
                        break
                if file_updated is not True:
                    create_file(result, file_name)
            else:
                create_file(result, file_name)
    else:
        create_file(result, file_name)


def write_lines(lines, file_name):
    with open(file_name, mode="w") as open_file:
        for line in lines:
            open_file.write(line)


def create_file(result, file_name):
    with open(file_name, mode="a") as open_file:
        open_file.write(result + "\n")


if __name__ == "__main__":
    main(parser.parse_args())

