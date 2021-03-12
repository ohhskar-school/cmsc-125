from random import randint, randrange
from time import sleep

MAX_VAL: int = 5
DEBUG: bool = True


class Process:
    def __init__(self, user, resource):
        self._user: int = user
        self._resource: int = resource
        self._curr_time: int = randint(1, MAX_VAL)
        self._time_to_use: int = 0
        self._is_active: bool = False

    def user(self):
        return self._user

    def resource(self):
        return self._resource

    def curr_time(self):
        return self._curr_time

    def activate(self):
        self._is_active: True

    def tick(self):
        self._curr_time -= 1
        if self._curr_time == 0:
            self._is_active = False

    def __str__(self):
        return ("[ process ]" +
            "\nUser: " + str(self._user) + "\nResource: " +
                str(self._resource) + "\nCurrent Time: " +
                str(self._curr_time)) + "\n"


class OS:
    def __init__(self):
        self._users_count: int = randint(1, MAX_VAL)
        self._resources_count: int = randint(1, MAX_VAL)
        self._active_processes: list[Process] = []
        self._processes: list[list[Process]] = [
            [] for i in range(self._resources_count)
        ]

    def create_processes(self):
        for index, resource in enumerate(self._processes, 1):
            max_processes: int = randint(0, self._users_count)
            users_index = [i for i in range(1, self._users_count + 1)]

            if DEBUG:
                print("[ create_processes ] max_processes: " +
                      str(max_processes))
                print("[ create_processes ] users_index: " + str(users_index))

            for j in range(max_processes):
                user: int = users_index[randrange(0, len(users_index))]

                resource.append(Process(user, index))

                users_index.remove(user)

            resource.sort(key=lambda x: x.user())

    def calculate_estimated_time(self):
        for resource_index, outer_resource in enumerate(self._processes):
            for outer_process in outer_resource:
                for search_index, inner_resource in enumerate(self._processes):
                    if search_index > resource_index:
                        break
                    for inner_process in inner_resource:
                        if outer_process.user() > inner_process.user():
                            break




                

    def print_processes(self):
        for index, resource in enumerate(self._processes, 1):
            print("-" * 20 + "\nResource " + str(index))
            for p in resource:
                print(p)
    
            

    def __str__(self):
        return "Users: " + str(self._users_count) + "\nResources: " + str(
            self._resources_count)


def main():
    os: OS = OS()
    print(os)
    os.create_processes()
    os.print_processes()

    # print_init(resource, users)
    # print_after_assign(users)


main()
