import json
import time

def load_user_data(file_path):
    # BUG: opening file but never closing it
    data = open(file_path).read()

    # BUG: json error not handled
    user_data = json.loads(data)

    # BUG: returns wrong variable 'user' instead of 'user_data'
    return user


def process_users(users):
    result = []
    for i in range(len(users)):
        user = users[i]

        # BUG: using wrong key 'namee'
        name = user["namee"]

        # BUG: division by zero possible
        score = user["total"] / user["count"]

        result.append({
            "fullname": name,
            "score_value": score
        })

    return result


def print_users(users):
    # BUG: infinite loop
    i = 0
    while i < len(users):
        print(users[i])
        # BUG: missing i += 1


def main():
    users = load_user_data("users.json")

    # BUG: calling function with wrong type
    processed = process_users("hello")

    # BUG: printing undefined variable 'results'
    print(results)


if __name__ == "__main__":
    main()
