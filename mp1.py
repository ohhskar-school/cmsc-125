# Machine Problem 1
# Po, Justin Andre
# Valles, Oscar Vian

from random import randint, randrange
from time import sleep
from typing import Optional, List
from os import system
from math import modf
from termcolor import cprint

MAX_VAL: int = 30
DEBUG: bool = False
DEBUG_DATA: bool = False
DEBUG_DISABLE_LOOP: bool = False
MAX_CHAR_WIDTH: int = 24


class Process:
    def __init__(self,
                 user: int,
                 resource: int,
                 curr_time: Optional[int] = None):
        self._user: int = user
        self._resource: int = resource
        self._curr_time: int = randint(
            1, MAX_VAL) if curr_time is None else curr_time
        self._init_time: int = self._curr_time
        self._time_to_start: int = 0
        self._time_to_end: int = self._curr_time
        self._is_active: bool = False
        self._is_done: bool = False

    def user(self):
        return self._user

    def resource(self):
        return self._resource

    def curr_time(self):
        return self._curr_time

    def time_to_start(self):
        return self._time_to_start

    def time_to_end(self):
        return self._time_to_end

    def is_active(self):
        return self._is_active

    def is_done(self):
        return self._is_done

    def add_time_to_start(self, time: int):
        self._time_to_start += time
        self._time_to_end += time

    def tick(self):
        if self._is_done:
            return

        if not self._is_active:
            if self._time_to_start == 0:
                self._is_active = True
            self._time_to_start -= 1
        else:
            if self._curr_time == 0:
                self._is_active = False
                self._is_done = True
            self._curr_time -= 1

    def print_active_func(self):
        if self._curr_time == 0:
            return "|== DONE ==|"
        elif self._is_active:
            return "|== ACTIVE ==|"
        else:
            return ""

    def print_time_to_start(self):
        return ("Time to Start: " +
                str(self._time_to_start + 1) if not self._is_active else "")

    def print_current_time(self):
        dec: float
        integer: float
        (dec, integer) = modf((self._init_time - self._curr_time) /
                              self._init_time * MAX_CHAR_WIDTH)

        return ("???" * int(integer) + "???" * (MAX_CHAR_WIDTH - int(integer)) +
                "\n" + str(self._init_time - self._curr_time) + "/" +
                str(self._init_time) +
                "\n" if self._is_active else "???" * MAX_CHAR_WIDTH + "\n")

    def __str__(self):
        return (self.print_active_func() + "\n[ process " +
                str(self._resource) + ":" + str(self._user) + " ]" +
                "\nUser: " + str(self._user) + "\n\n" +
                self.print_current_time() + self.print_time_to_start() + "\n")


Resource = List[Process]
Processes = List[Resource]


class OS:
    def __init__(self):
        self._users = self.remove_duplicates(
            [randint(1, MAX_VAL) for i in range(0, randint(1, MAX_VAL))])
        self._resources = self.remove_duplicates(
            [randint(1, MAX_VAL) for i in range(0, randint(1, MAX_VAL))])
        self._users_count: int = len(self._users)
        self._resources_count: int = len(self._resources)
        self._users.sort()
        self._resources.sort()
        self._processes: Processes = [[None for i in range(self._users[-1] + 1)]
                                      for i in range(self._resources[-1] + 1)]

        if DEBUG_DATA:
            self.create_debug_processes()
        else:
            self.create_processes()
            self.clean_processes()
        self.calculate_estimated_time()

    def create_debug_processes(self):
        self._users_count = 3
        self._resources_count = 1
        self._processes = [
            [None, Process(1, 1, 1),
             Process(1, 2, 1),
             Process(1, 3, 1)],
        ]

    def create_processes(self):
        for resource in self._resources:
            max_processes: int = randint(0, self._users_count)
            users = self._users.copy()

            if DEBUG:
                print("[ create_processes ] users: " + str(self._users))
                print("[ create_processes ] resources: " + str(self._resources))
                print("[ create_processes ] processes: " + str(self._processes))
                print("[ create_processes ] max_processes: " +
                      str(max_processes))
                print("[ create_processes ] users: " + str(users))

            for j in range(max_processes):
                user: int = users[randrange(0, len(users))]
                self._processes[resource][user] = Process(user, resource)

                users.remove(user)
        
        if DEBUG:
            print("[ create_processes ] processes: " + str(self._processes))
    
    def clean_processes(self):
        for index, resource in enumerate(self._processes):
            if index not in self._resources:
                if DEBUG:
                    print("[ clean_processes ] index: " + str(index))
                self._processes[index] = None
        
        if DEBUG:
            print("[ clean_processes ] processes: " + str(self._processes))

    def calculate_estimated_time(self):
        if DEBUG:
            print("[ calculate_estimated_time ] initial processes: \n")
            self.print_processes(self._processes)

        for user in self._users:
            user_processes: List[Process] = []
            for resource in self._processes:
                if resource is None:
                    continue
                    
                if resource[user] is not None:
                    self.calculate_tts_in_resource(resource, user)
                    user_processes.append(resource[user])
            self.check_for_concurrency(user_processes)

    def calculate_tts_in_resource(self, resource: Resource, user: int):
        if DEBUG:
            print("[ calculate_tts_in_resource ] user: " +
                  str(user))
            print("[ calculate_tts_in_resource ] resource: " +
                  str(resource[user].resource()))

        for i in range(user - 1, 0, -1):
            process = resource[i]
            
            if DEBUG:
                print(process)

            if process is None:
                continue

            else:
                if DEBUG:
                    print(
                        "[ calculate_tts_in_resource ] process.time_to_end(): "
                        + str(process.time_to_end()))
                    print(
                        "[ calculate_tts_in_resource ] resource[user_index].time_to_start(): "
                        + str(resource[user].time_to_start()))
                resource[user].add_time_to_start(
                    process.time_to_end() -
                    resource[user].time_to_start())
                break

        if DEBUG:
            print("[ calculate_tts_in_resource ] after calculate:\n")
            self.print_processes(self._processes)

    def check_for_concurrency(self, processes: List[Process]):
        processes.sort(key=lambda x: x.time_to_start())
        if DEBUG:
            print("[ check_for_concurrency ] init")
            print("[ check_for_concurrency ] user_process: \n")
            for process in processes:
                if process is not None:
                    print(process)

        for outer_index in range(len(processes)):
            outer_process = processes[outer_index]
            for inner_index in range(outer_index + 1, len(processes)):
                inner_process = processes[inner_index]
                if DEBUG:
                    print("[ check_for_concurrency ] outer_process: \n")
                    print(outer_process)
                    print("[ check_for_concurrency ] inner_process: \n")
                    print(inner_process)
                if (outer_process.time_to_end() >
                        inner_process.time_to_start()
                        and inner_process.time_to_end() >
                        outer_process.time_to_start()):
                    if DEBUG:
                        print(
                            "[ check_for_concurrency ] if: " +
                            str(outer_process.time_to_end() > inner_process.
                                time_to_start() and inner_process.time_to_end(
                                ) > outer_process.time_to_start()))

                    inner_process.add_time_to_start(
                        outer_process.time_to_end() -
                        inner_process.time_to_start())

    def remove_duplicates(self, items):
        return list(dict.fromkeys(items))

    def run(self):
        seconds: int = -1
        new_processes: Processes = [[
            process for process in resource if process is not None
        ] if resource is not None else None for resource in self._processes]
        while True:
            if not DEBUG:
                system("clear")

            cprint("makOS version 11.11 (Big Ser)\n", attrs=["bold"])
            print("Users: ", end="")
            cprint(self._users, attrs=["bold"])
            print("Resources: ", end="")
            cprint(self._resources, attrs=["bold"])
            cprint("\n====== ", "yellow", end="")
            print("TIME: " + str(seconds) + "s", end="")
            cprint(" ======\n", "yellow")
            self.print_processes(new_processes)

            for resources in new_processes:
                if resources is None:
                    continue
                for process in resources:
                    if process is not None:
                        process.tick()
            new_processes[:] = [[
                process for process in resource
                if process is None or not process.is_done()
            ] if resource is not None else None for resource in new_processes]

            should_end: bool = True
            for resources in new_processes:
                if resources is None:
                    continue
                if len(resources) > 0:
                    if DEBUG:
                        print("[ run ] len(resources)" +
                              str(len(resources) > 0))
                    should_end = False

            if should_end:
                break

            seconds += 1

            if not DEBUG:
                sleep(1)

    def print_processes(self, processes: List[Process]):
        for index, resource in enumerate(processes, 0):
            if resource is None:
                continue

            cprint("-" * MAX_CHAR_WIDTH + "\n", "grey")

            if index < 10:
                cprint(
                    "=====| Resource " + str(index) +
                    " |=====\n", "cyan")
            else:
                cprint(
                    "=====| Resource " + str(index) +
                    " |====\n", "cyan")

            if len(resource) > 0:
                for p in resource:
                    if p is not None:
                        if p.curr_time() == 0:
                            cprint(p, "green")
                        elif p.is_active():
                            print(p)
                        else:
                            cprint(p, attrs=["dark"])
            else:
                cprint("\nNo Processes in Queue\n", "blue")
        cprint("\n" + "-" * MAX_CHAR_WIDTH, "grey")

    def processes(self):
        return self._processes

    def __str__(self):
        return ("Users: " + str(self._users_count) + "\nResources: " +
                str(self._resources_count))


def main():
    if DEBUG:
        print("[ main ] init")
    os: OS = OS()
    if DEBUG:
        print("[ main ] after calculate_estimated_time()")
    
    if not DEBUG_DISABLE_LOOP:
        os.run()

    # print_init(resource, users)
    # print_after_assign(users)


main()
