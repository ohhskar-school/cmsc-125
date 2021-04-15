# Machine Problem 2
# Po, Justin Andre
# Valles, Oscar Vian
#
# This machine problem was implement through pair programming

from typing import List, Callable
from functools import cmp_to_key
from copy import deepcopy
from math import floor


class Process:
    def __init__(self, id, arrival, burst, priority):
        self._id: int = id
        self._arrival: int = arrival
        self._burst: int = burst
        self._priority: int = priority
        self._waiting: int = 0
        self._turnaround: int = 0
        self._currBurst: int = burst

    def id(self):
        return self._id

    def arrival(self):
        return self._arrival

    def burst(self):
        return self._burst

    def priority(self):
        return self._priority

    def waiting(self):
        return self._waiting

    def turnaround(self):
        return self._turnaround

    def currBurst(self):
        return self._currBurst

    def decCurrBurst(self):
        self._currBurst -= 1

    def addWaiting(self, add: int):
        self._waiting += add

    def setTurnaround(self, turnaround: int):
        self._turnaround += turnaround

    def setWaiting(self, waiting: int):
        self._waiting = waiting

    def __str__(self):
        return (
            str(self._id)
            + "\t\t"
            + str(self._arrival)
            + "\t\t"
            + str(self._burst)
            + "\t\t"
            + str(self._priority)
            + "\t\t\t"
            + str(self._waiting)
            + "\t\t\t"
            + str(self._turnaround)
        )


class Gantt:
    def __init__(
        self,
        ganttProceses: List[Process],
        processes: List[Process],
        avgWaiting: int,
        avgTurnaround: int,
    ):
        self._processes: List[Process] = processes
        self._ganttProcesses = ganttProceses
        self._avgWaiting: int = avgWaiting
        self._avgTurnaround: int = avgTurnaround

    def print(self):
        greatestLength = max(
            process.turnaround()
            - (0 if index == 0 else self._ganttProcesses[index - 1].turnaround())
            for index, process in enumerate(self._ganttProcesses)
        )
        totalLength = self._ganttProcesses[-1].turnaround()
        divisionFactor = greatestLength / totalLength * 0.75
        prevLength = 0
        for index, process in enumerate(self._ganttProcesses):
            length = floor((process.turnaround() - prevLength) * divisionFactor)
            pid = "p" + str(process.id())
            total = 10 - len(pid)
            first = floor(total / 2)
            second = total - first
            if index == 0:
                print("┌──────────┬── " + str(prevLength))
            else:
                print("├──────────┼── " + str(prevLength))

            for i in range(length):
                print("│          │")
            print("│" + " " * first + pid + " " * second + "│")
            for i in range(length):
                print("│          │")

            if index == len(self._ganttProcesses) - 1:
                turnaround = str(process.turnaround())
                print("└──────────┴── " + str(turnaround))
            prevLength = process.turnaround()

        print("\nProcess\tArrival\tBurst\tPriority\tWaiting\t\tTurnaround")
        for process in self._processes:
            print(process)
        print("\nAverage Waiting Time: " + str(self._avgWaiting) + "ms")
        print("Average Turnaround Time: " + str(self._avgTurnaround) + "ms")


def parse(filename: str) -> List[Process]:
    processes: List[Process] = []
    with open(filename) as f:
        lines = f.readlines()

        for index, line in enumerate(lines):
            if index == 0:
                continue

            props = [int(prop) for prop in line.split()]

            processes.append(Process(props[0], props[1], props[2], props[3]))

    return processes


def simple(processes: List[Process], key: Callable) -> Gantt:
    newProcesses = deepcopy(processes)
    newProcesses.sort(key=key)

    currWaiting: int = 0
    avgWaiting: int = 0
    avgTurnaround: int = 0
    for process in newProcesses:
        process.addWaiting(currWaiting)

        turnaround = currWaiting + process.burst()
        process.setTurnaround(turnaround)

        avgTurnaround += turnaround
        avgWaiting += currWaiting

        currWaiting += process.burst()

    lenProcesses = len(newProcesses)
    avgWaiting /= lenProcesses
    avgTurnaround /= lenProcesses

    finished = deepcopy(newProcesses)
    finished.sort(key=lambda x: x.id())

    return Gantt(newProcesses, finished, avgWaiting, avgTurnaround)


def fcfs(processes) -> Gantt:
    return simple(processes, lambda x: x.id())


def priorityCompare(process1: Process, process2: Process):
    if process1.priority() == process2.priority():
        return process1.id() - process2.id()

    return process1.priority() - process2.priority()


def priority(processes) -> Gantt:
    return simple(processes, cmp_to_key(priorityCompare))


def sjfCompare(process1: Process, process2: Process):
    if process1.currBurst() == process2.currBurst():
        return process1.id() - process2.id()

    return process1.currBurst() - process2.currBurst()


def sjf(processes) -> Gantt:
    return simple(processes, cmp_to_key(sjfCompare))


def srptCompare(process1: Process, process2: Process):
    if process1.arrival() == process2.arrival():
        return process1.currBurst() - process1.currBurst()

    return process1.arrival() - process2.arrival()


def srpt(processes) -> Gantt:
    newProcesses = deepcopy(processes)
    newProcesses.sort(key=cmp_to_key(srptCompare))

    sjf: List[Process] = []
    gantt: List[Process] = [deepcopy(newProcesses[0])]
    finished: List[Process] = []

    currTime: int = 0
    currProcess: Process = None
    while len(sjf) != 0 or len(newProcesses) != 0:
        if len(sjf) > 0:
            currProcess = sjf[0]
            if sjf[0].currBurst() == 0:
                sjf[0].setTurnaround(currTime)
                finished.append(sjf[0])
                sjf.pop(0)

        while len(newProcesses) > 0 and newProcesses[0].arrival() == currTime:
            sjf.append(newProcesses.pop(0))

        if len(sjf) > 0:
            sjf.sort(key=cmp_to_key(sjfCompare))
            if currProcess != None and sjf[0] != currProcess:
                gantt[-1].setTurnaround(currTime)
                gantt.append(deepcopy(sjf[0]))

            sjf[0].decCurrBurst()

        currTime += 1

    gantt[-1].setTurnaround(currTime - 1)

    avgWaiting: int = 0
    avgTurnaround: int = 0
    for process in finished:
        waiting = process.turnaround() - process.burst() - process.arrival()
        process.setWaiting(waiting)
        avgWaiting += waiting
        avgTurnaround += process.turnaround()

    finished.sort(key=lambda x: x.id())
    lenProcesses: int = len(finished)
    avgWaiting /= lenProcesses
    avgTurnaround /= lenProcesses

    return Gantt(gantt, finished, avgWaiting, avgTurnaround)


def roundRobin(processes) -> Gantt:
    newProcesses = deepcopy(processes)
    newProcesses.sort(key=lambda x: x.id())

    finished: List[Process] = []
    gantt: List[Process] = [deepcopy(newProcesses[0])]
    currTime: int = 4
    totalTime: int = 0

    while len(newProcesses) > 0:
        if newProcesses[0].currBurst() == 0:
            newProcesses[0].setTurnaround(totalTime)
            finished.append(newProcesses[0])
            newProcesses.pop(0)
            currTime = 4

            gantt[-1].setTurnaround(totalTime)

            if len(newProcesses) > 0:
                gantt.append(deepcopy(newProcesses[0]))

        if currTime == 0:
            newProcesses.append(newProcesses.pop(0))
            gantt[-1].setTurnaround(totalTime)
            gantt.append(deepcopy(newProcesses[0]))
            currTime = 4

        if len(newProcesses) > 0:
            newProcesses[0].decCurrBurst()

        totalTime += 1
        currTime -= 1

    avgWaiting: int = 0
    avgTurnaround: int = 0
    for process in finished:
        waiting = process.turnaround() - process.burst()
        process.setWaiting(waiting)
        avgWaiting += waiting
        avgTurnaround += process.turnaround()

    finished.sort(key=lambda x: x.id())
    lenProcesses = len(finished)
    avgWaiting /= lenProcesses
    avgTurnaround /= lenProcesses

    return Gantt(gantt, finished, avgWaiting, avgTurnaround)


if __name__ == "__main__":
    # Add additional text files here to be processed
    inputFiles = ["process1.txt", "process2.txt"]
    for file in inputFiles:
        processes = parse(file)
        print("-" * 5 + " " + file + " " + "-" * 5)
        print("\n------ FCFS -----")
        fcfs(processes).print()
        print("\n------ SJF -----")
        sjf(processes).print()
        print("\n------ SRPT -----")
        srpt(processes).print()
        print("\n------ PRIORITY -----")
        priority(processes).print()
        print("\n------ ROUND ROBIN -----")
        roundRobin(processes).print()
