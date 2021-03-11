from random import randint
from time import sleep

# Constants
MAX_NUMBERS: int = 7
DEBUG: bool = False

# Types
Users = list[list[int]]


class Resource:
    def __init__(self, id: int):
        self._id: int = id
        self._init_timer: int = randint(1, MAX_NUMBERS)
        self._timer: int = self._init_timer
        self._is_active: bool = False

    def __str__(self):
        return (
            "[ Resource "
            + str(self._id)
            + " ]\ninit_timer: "
            + str(self._init_timer)
            + " \ncurrent_timer: "
            + str(self._timer)
            + "\nactive: "
            + str(self._is_active)
        )

    def id(self):
        return self._timer

    def timer(self):
        return self._timer

    def init_timer(self):
        return self._init_timer

    def is_active(self):
        return self._is_active

    def tick(self):
        self._timer -= 1
        if self._timer == -1:
            self._active = False
            self._timer = self._init_timer

    def activate(self):
        self._is_active = True


class User:
    def __init__(self, id: int):
        self._id: int = id
        self._assigned_resources: list[Resource] = []
        self._active_resource: Resource = None

    def __str__(self):
        return (
            "[ User "
            + str(self._id)
            + " ]\nassigned_resources: "
            + str(self._assigned_resources)
            + "\nactive_resource: "
            + str(self._active_resource)
        )

    def id(self):
        return self._id

    def assigned_resources(self):
        return self._assigned_resources

    def active_resource(self):
        return self._active_resource

    def assign_resource(self, resource: Resource):
        self._assigned_resources.append(resource)

    def use_resource(self):
        if self._active_resource is None:
            for i in self._assigned_resources:
                if not i.is_active():
                    self._active_resource = i
                    self._active_resource.activate()
                    break

    def tick(self):
        if self._active_resource is not None:
            self._active_resource.tick()
            if not self._active_resource.is_active():
                self._active_resource = None

    def print_status(self):
        if self._active_resource is not None:
            print(
                "[ User "
                + str(self._id)
                + " ] Resource "
                + str(self._active_resource.id())
                + ": "
                + str(self._active_resource.timer())
                + "/"
                + str(self._active_resource.init_timer())
            )
        else:
            print("[ User " + str(self._id) + " ] No Active Resource")


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
    for user in users:
        resources_amt: int = randint(1, len(resources))
        resources_index = [i for i in range(0, len(resources))]

        if DEBUG:
            print("[ assign_resource ] user: " + str(user.id()))
            print("[ assign_resource ] resources_amt: " + str(resources_amt))
            print("[ assign_resource ] resources_index: " + str(resources_index))

        for random_resource in range(resources_amt):
            chosen_resource_index: int = randint(0, len(resources_index) - 1)
            chosen_resource: int = resources_index[chosen_resource_index]

            user.assign_resource(resources[chosen_resource])
            del resources_index[chosen_resource_index]

            if DEBUG:
                print(
                    "[ assign_resource_loop ] chosen_resource_index: "
                    + str(chosen_resource_index)
                )
            if DEBUG:
                print(
                    "[ assign_resource_loop ] chosen_resource: " + str(chosen_resource)
                )
            if DEBUG:
                print(
                    "[ assign_resource_loop ] resources_index: " + str(resources_index)
                )
                print("[ assign_resource_loop ] resources: " + str(resources))


def countdown_resources(users: Users):
    while True:
        for user in users:
            user.use_resource()
            user.tick()
            user.print_status()

        should_end: bool = True

        for user in users:
            if user.active_resource() is None:
                should_end = should_end and False
            if not should_end:
                break

        if should_end:
            break

        sleep(1)


def main():
    resources: list[Resource] = [
        Resource(i + 1) for i in range(randint(1, MAX_NUMBERS))
    ]
    users: Users = [User(i + 1) for i in range(randint(1, MAX_NUMBERS))]

    print("[ main ] resources: " + str(len(resources)))
    print("[ main ] users: " + str(len(users)))
    # if DEBUG:
    #     print_resources(resources)
    #     print_users(users)

    assign_resource(resources, users)
    countdown_resources(users)

    # print_init(resource, users)
    # print_after_assign(users)


main()
