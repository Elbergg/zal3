import argparse
import requests
import sys
import json
from matplotlib import pyplot as plt


def reset():
    todo_js = requests.get("https://jsonplaceholder.typicode.com/todos").json()
    with open("todos.json", "w") as file_handler:
        json.dump(todo_js, file_handler, indent=4)


def list_user(user, path):
    with open(path, "r") as file_handler:
        file = json.load(file_handler)
        for row in file:
            if row["userId"] == int(user):
                print(row["title"])


def list_not_completed(user, path):
    with open(path, "r") as file_handler:
        file = json.load(file_handler)
        for row in file:
            if row["userId"] == int(user):
                if row["completed"] is False:
                    print(row["title"])


def toogle_reminder(id, path):
    with open(path, "r") as file_handler:
        old_data = json.load(file_handler)
        for row in old_data:
            if row["id"] == int(id):
                if row["completed"] is True:
                    row["completed"] = False
                    break
                else:
                    row["completed"] = True
    with open(path, "w") as file_handler:
        json.dump(old_data, file_handler, indent=4)


def get_stats(path):
    with open(path, "r") as file_handler:
        data = json.load(file_handler)
        num_of_completed = 0
        num_of_not_completed = 0
        for row in data:
            if row["completed"] is True:
                num_of_completed += 1
            elif row["completed"] is False:
                num_of_not_completed += 1
    return num_of_completed, num_of_not_completed


def plot_pie(path):
    stats = get_stats(path)
    labels = ("completed", "not completed")
    plt.pie(stats, labels=labels)
    plt.show()


def plot_bar(path):
    stats = get_stats(path)
    plt.bar(0, stats[0], label="completed")
    plt.bar(2, stats[1], label="not completed")
    plt.legend()
    plt.show()


def list_all(path):
    with open(path, "r") as file_handler:
        data = json.load(file_handler)
        for row in data:
            userid = row["userId"]
            id = row["id"]
            title = row["title"]
            completed = row["completed"]
            if completed is False:
                completed = "not completed"
            elif completed is True:
                completed = "completed"
            info = f'Task {id} for user {userid}: "{title}" is {completed}.'
            print(info)


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("path", default="todos.json", nargs="?")
    parser.add_argument(
        "--reset",
        action="store_true",
    )
    parser.add_argument("--list-not-completed", dest="list_not_completed")
    parser.add_argument("--user")
    parser.add_argument("--toogle-todo", dest="toogle_todo")
    parser.add_argument("--bar-plot", action="store_true", dest="bar_plot")
    parser.add_argument("--pie-plot", action="store_true", dest="pie_plot")
    args = parser.parse_args(arguments[1:])
    user_id = args.user
    path = args.path
    not_completed = args.list_not_completed
    toogle = args.toogle_todo
    if len(arguments[1:]) == 0:
        list_all(path)
    if args.reset:
        reset()
    if args.user:
        list_user(user_id, path)
    if not_completed:
        list_not_completed(not_completed, path)
    if toogle:
        toogle_reminder(toogle, path)
    if args.bar_plot:
        plot_bar(path)
    if args.pie_plot:
        plot_pie(path)


if __name__ == "__main__":
    main(sys.argv)
