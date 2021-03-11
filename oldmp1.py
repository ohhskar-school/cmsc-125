from random import randint
from time import sleep

# Constants
MAX_NUMBERS: int = 7
DEBUG: bool = False

class User:
    def __init__(self, id: int):
        self._id: int = id

    def __str__(self):
        return (
            "[ User "
            + str(self._id)
            + " ]"
        )

    def id(self):
        return self._id


class Resource:
    def __init__(self, id: int):
        self._id: int = id
        self._init_timer: int = randint(1, MAX_NUMBERS)
        self._timer: int = self._init_timer
        self._users: User = []

    def __str__(self):
        return (
            "-" * 20 
            + "\n[ resource "
            + str(self._id)
            + " ]\ninit_timer: "
            + str(self._init_timer)
            + " \ncurrent_timer: "
            + str(self._timer)
            + "\nactive: "
            + str(self._is_active)
            + "\nusers:\n"
            + '\n'.join([str(i) for i in self._users])
        )

    def id(self):
        return self._id

    def timer(self):
        return self._timer

    def init_timer(self):
        return self._init_timer

    def is_active(self):
        return self._is_active

    def tick(self):
        if len(self._users) > 0:
            self._users[0].activate()
            self._timer -= 1
            if self._timer == 0:
                self._is_active = False
                self._timer = self._init_timer

    def assign_user(self, user: User):
        self._users.append(user)
    
    def sort_users(self):
        self._users.sort(key = lambda x: x.id())

# Print Functions
def print_resources(resources: Resource):
    for i in resources:
        print(i)

def print_users(users: User):
    for i in users:
        print(i)

        
# def print_init(resource: int, users: Users):
#     print("Generating Resources and Users")
#     print("Resources: " + str(resource))
#     print("Users: " + str(len(users)))

# def print_after_assign(users: Users):
#     print("Assigned Resources:")
#     for count, user in enumerate(users, 1):
#         print("User " + str(count) + ": " + str(user))

# Logical Functions
def assign_resource(resources: Resource, users: User):
    for resource in resources:
        users_amt: int = randint(1, len(users))
        users_index= [i for i in range(0, len(users))]

        if DEBUG:
            print("[ assign_resource ] resource: " + str(resource.id()))
            print("[ assign_resource ] users_amt: " + str(users_amt))
            print("[ assign_resource ] users_index: " + str(users_index))

        for i in range(users_amt):
            chosen_user_index: int = randint(0, len(users_index) - 1)
            chosen_user: int = users_index[chosen_user_index]

            resource.assign_user(users[chosen_user])
            users[chosen_user].assign_resource(resource)
            del users_index[chosen_user_index]

            if DEBUG:
                print(
                    "[ assign_resource_loop ] chosen_resource_index: "
                    + str(chosen_user_index)
                )
            if DEBUG:
                print(
                    "[ assign_resource_loop ] chosen_user: " + str(chosen_user)
                )
            if DEBUG:
                print(
                    "[ assign_resource_loop ] chosen_user_index: " + str(chosen_user_index)
                )
        
        resource.sort_users()

def countdown_resources(users: User):
    current_time = 0


def main():
    resources: list[Resource] = [
        Resource(i + 1) for i in range(randint(1, MAX_NUMBERS))
    ]
    users: User = [User(i + 1) for i in range(randint(1, MAX_NUMBERS))]

    print("[ main ] resources: " + str(len(resources)))
    print("[ main ] users: " + str(len(users)))

    assign_resource(resources, users)

    countdown_resources(users)

    # print_init(resource, users)
    # print_after_assign(users)


main()
