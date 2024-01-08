import argparse
import json
import datetime
import sys
from random import randint


def generate_id(path):
    new_id = randint(0, 100000)
    ids = []
    try:
        with open(path, "r") as file_handle:
            file = json.load(file_handle)
            for row in file:
                id = row["id"]
                ids.append(id)
        while new_id in ids:
            new_id = randint(0, 100000)
    except:  # noqa
        json.decoder.JSONDecodeError
    return new_id


def read_diary(path):
    data = []
    try:
        with open(path, "r") as file_handle:
            data = json.load(file_handle)
    except:
        json.decoder.JSONDecodeError
    return data


def search_diary_by_date(path, date):
    try:
        searching_date = datetime.date.fromisoformat(date)
        with open(path, "r") as file_handle:
            file = json.load(file_handle)
            for row in file:
                date = row["date"]
                date_split = date.split(" ")
                date_time = datetime.date.fromisoformat(date_split[0])
                if searching_date == date_time:
                    id = row["id"]
                    content = row["content"]
                    content_first_line = content.split("\\n")
                    date = row["date"]
                    info = f"{id}, {content_first_line[0]}, {date}"
                    print(info)
    except:
        json.decoder.JSONDecodeError


def add(path, content):
    data = read_diary(path)
    with open(path, "w") as file_handle:
        posted_content = " ".join(content)
        new_data = {
            "id": generate_id(path),
            "content": posted_content,
            "date": str(datetime.datetime.now()),
        }
        data.append(new_data)
        json.dump(data, file_handle, indent=4)


def search_by_id(path, id):
    try:
        with open(path, "r") as file_handler:
            file = json.load(file_handler)
            for row in file:
                if row["id"] == int(id):
                    lines = row["content"].split("\\n")
                    for line in lines:
                        print(line)
    except:
        json.decoder.JSONDecodeError


def delete_post(path, id):
    try:
        with open(path, "r") as file_handler:
            file = json.load(file_handler)
            for row in file:
                if row["id"] == int(id):
                    file.remove(row)
                    new_content = file
        with open(path, "w") as file_handler:
            json.dump(new_content, file_handler, indent=4)

    except:
        json.decoder.JSONDecodeError


def stats(path, k):
    try:
        dates = []
        dates_dict = {}
        num_of_entries = 0
        num_of_days_with_entries = 0
        with open(path, "r") as file_handler:
            file = json.load(file_handler)
            for row in file:
                date = row["date"]
                date_without_hour = date.split(" ")[0]
                num_of_entries += 1
                if date_without_hour not in dates:
                    dates.append(date_without_hour)
                    num_of_days_with_entries += 1
                    dates_dict.update({date_without_hour: 1})
                else:
                    counter = dates_dict.get(date_without_hour)
                    counter += 1
                    dates_dict.update({date_without_hour: counter})

            first_date = datetime.datetime.fromisoformat(min(dates))
            last_date = datetime.datetime.fromisoformat(max(dates))
            how_long = (last_date - first_date).days + 1
            avg_entries = num_of_entries / how_long
            num_of_days_without_entries = how_long - num_of_days_with_entries
            nums_of_entries = dates_dict.values()
            days_with_kavg = 0
            for num in nums_of_entries:
                if num > avg_entries * int(k):
                    days_with_kavg += 1
            print(avg_entries)
            print(num_of_days_without_entries)
            print(days_with_kavg)

    except:
        json.decoder.JSONDecodeError


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("diary")
    parser.add_argument("--add", nargs="+")
    parser.add_argument("--day")
    parser.add_argument("--id")
    parser.add_argument("--delete")
    parser.add_argument("--stats")
    args = parser.parse_args(arguments[1:])
    path = args.diary
    new_content = args.add
    day = args.day
    id = args.id
    delete = args.delete
    k = args.stats
    if args.add:
        add(path, new_content)
    if args.day:
        search_diary_by_date(path, day)
    if args.id:
        search_by_id(path, id)
    if delete:
        delete_post(path, delete)
    if args.stats:
        stats(path, k)


if __name__ == "__main__":
    main(sys.argv)
