# Machine Problem 3
# Po, Justin Andre
# Valles, Oscar Vian
#
# This machine problem was implemented through pair programming

from typing import List, Tuple
from dataclasses import dataclass
from copy import deepcopy
from time import sleep
from os import system
from math import floor
from termcolor import cprint

@dataclass(order=True)
class Job:
    order: int
    currTime: int
    size: int
    fragmentation: int = 0
    waitingTime: int = 0

@dataclass(order = True) 
class Block:
    order: int
    size: int
    timesUsed: int
    secondsUsed: int = 0

@dataclass(order = True)
class Tick:
    memory: List[List[Job]]
    queueLength: int
    partitionsUsed: float
    fragmentation: int

jobs: List[Job] = [
    Job(1,   5,  5760),
    Job(2,   4,  4190),
    Job(3,   8,  3290),
    Job(4,   2,  2030),
    Job(5,   2,  2550),
    Job(6,   6,  6990),
    Job(7,   8,  8940),
    Job(8,   10, 740),
    Job(9,   7,  3930),
    Job(10,  6,  6890),
    Job(11,  5,  6580),
    Job(12,  8,  3820),
    Job(13,  9,  9140),
    Job(14,  10, 420),
    Job(15,  10, 220),
    Job(16,  7,  7540),
    Job(17,  3,  3210),
    Job(18,  1,  1380),
    Job(19,  9,  9850),
    Job(20,  3,  3610),
    Job(21,  7,  7540),
    Job(22,  2,  2710),
    Job(23,  8,  8390),
    Job(24,  5,  5950),
    Job(25,  10, 760),
]

blocks: List[Block] = [
    Block(1,  9500, 0),
    Block(2,  7000, 0),
    Block(3,  4500, 0),
    Block(4,  8500, 0),
    Block(5,  3000, 0),
    Block(6,  9000, 0),
    Block(7,  1000, 0),
    Block(8,  5500, 0),
    Block(9,  1500, 0),
    Block(10, 500, 0),
]

memoryPoints: [str] = ['0']
cumulativeSize: int = 0 

for x in blocks:
    cumulativeSize += x.size
    memoryPoints.append(str(cumulativeSize))

def calculate(jobs: List[Job], blocks: List[Block]) -> Tuple[List[List[Job]], List[Block], List[Job]]:
    history: List[Tick] = []
    memory: List[Job] = [ None for i in blocks ]

    maxSize: int = max(block.size for block in blocks)

    # Remove jobs that cannot fit in a single partition
    workingJobs = [ job for job in jobs if job.size <= maxSize ]
    totalJobs = len(workingJobs)

    while True:
        for index, job in enumerate(list(memory)):
            if job != None:
                if job.currTime == 0:
                    memory[index] = None
                    totalJobs -= 1
                    continue 

                blocks[index].secondsUsed += 1
                job.currTime -= 1

        if totalJobs == 0:
            break

        for job in list(workingJobs):
            for block in blocks:
                if job.size < block.size and memory[block.order - 1] == None:
                    workingJobs = [ x for x in workingJobs if x.order != job.order ]
                    job.fragmentation = block.size - job.size
                    memory[block.order - 1] = deepcopy(job)
                    block.timesUsed += 1
                    break
        
        for job in workingJobs:
            job.waitingTime += 1

        history.append(Tick(deepcopy(memory), len(workingJobs), len([x for x in memory if x != None]), sum(x.fragmentation if x != None else 0 for x in memory)))

    return (history, blocks, jobs)

def printBlock(string):
    total = 20 - len(string)
    first = floor(total / 2)
    second = total - first

    print("│" + " " * first + string  + " " * second + "│")

def displayTick(history: List[Tick]):
    if history != None:
        for index, memory in enumerate(history.memory):
            jobId = "Job " + str(memory.order) if memory != None else "None"

            if index == 0:
                print("┌────────────────────┬── " + memoryPoints[index])
            else:
                print("├────────────────────┼── " + memoryPoints[index])

            printBlock(jobId)

            if jobId != "None":
                printBlock("JSZ: " + str(memory.size))
                printBlock("IF: " + str(memory.fragmentation))

            if index == len(history.memory) - 1:
                print("└────────────────────┴── " + memoryPoints[index + 1])

        cprint("\nThroughput: ", "cyan", end="")
        print(history.partitionsUsed, end="")
        cprint("\nStorage Utilization: ", "cyan", end="")
        print( "{:.2%}".format(history.partitionsUsed/(len(memoryPoints)-1)), end="")
        cprint("\nWaiting Queue Length: ", "cyan", end="")
        print(history.queueLength, end="")
        cprint("\nTotal Internal Fragmentation: ", "cyan", end="")
        print(history.fragmentation, end="\n\n")

def displayTotal(history: List[Tick], jobs: List[Job], blocks: List[Block]):
    totalTime: int = len(history)
    totalThroughput: int = 0
    totalStorageUtil: int = 0
    totalWaitingQueue: int = 0
    totalWaitingTime: int = 0
    totalInternalFrag: int = 0
    avgTotalInternalFrag: int = 0

    for x in history:
        totalThroughput += x.partitionsUsed
        totalStorageUtil += x.partitionsUsed/(len(memoryPoints)-1)
        totalWaitingQueue += x.queueLength
        avgTotalInternalFrag += x.fragmentation

    for y in jobs:
        totalWaitingTime += y.waitingTime
        totalInternalFrag += y.fragmentation

    blocks.sort(key=lambda x: x.timesUsed)

    leastUsedBlocks = sorted([block for block in blocks if block.timesUsed == blocks[0].timesUsed], key=lambda x: x.order)
    mostUsedBlocks = sorted([block for block in blocks if block.timesUsed == blocks[-1].timesUsed], key=lambda x: x.order)
    usageRate = sorted(blocks, key=lambda x: x.order)

    partitionsNeverUsed = sum(1 for x in blocks if x.timesUsed == 0)/len(blocks)
    partitionsFrequentlyUsed = sum(1 for x in blocks if x.timesUsed == blocks[-1].timesUsed)/len(blocks)

    cprint("\nAverages", attrs=["dark"], end="")
    cprint("\nThroughput: ", "cyan", end="")
    print("{:.2f}".format(totalThroughput/totalTime) + " jobs/s", end="")
    cprint("\nStorage Utilization: ", "cyan", end="")
    print( "{:.0%}".format(totalStorageUtil/totalTime), end="")
    cprint("\nWaiting Queue Length: ", "cyan", end="")
    print("{:.2f}".format(totalWaitingQueue/totalTime) + " jobs/s", end="")
    cprint("\nInternal Fragmentation: ", "cyan", end="")
    print("{:.2f}".format(avgTotalInternalFrag/totalTime) + " blocks/s")

    cprint("\nTotals", attrs=["dark"], end="")
    cprint("\nTime: ", "cyan", end="")
    print(str(totalTime) + "s", end="")
    cprint("\nInternal Fragmentation: ", "cyan", end="")
    print(str(totalInternalFrag) + " blocks", end="")
    cprint("\nWaiting Time In Queue: ", "cyan", end="")
    print("{:.2f}".format(totalWaitingTime) + "s")

    cprint("\nFrequencies", attrs=["dark"], end="")
    cprint("\nPartitions never used: ", "cyan", end="")
    print("{:.2%}".format(partitionsNeverUsed), end="")
    cprint("\nFrequently used partitions: ", "cyan", end="")
    print("{:.2%}".format(partitionsFrequentlyUsed), end="")
    cprint("\nLeast Used Block/s: ", "cyan")
    for x in leastUsedBlocks:
        print("    Block " + str(x.order) + " (" + str(x.timesUsed) + " times)")
    cprint("Most Used Block/s: ", "cyan")
    for y in mostUsedBlocks:
        print("    Block " + str(y.order) + " (" + str(y.timesUsed) + " times)")
    cprint("Storage Utilization: ", "cyan")
    for y in usageRate:
        print("    Block " + str(y.order) + " (" + "{:.2%}".format(y.secondsUsed/totalTime) + ")")
    print("\n")


def run(firstHistory: List[Tick], firstJobs: List[Job], firstBlocks: List[Block], bestHistory: List[Tick], bestJobs: List[Job], bestBlocks: List[Block], worstHistory: List[Tick], worstJobs: List[Job], worstBlocks: List[Block] ):
    seconds: int = 0
    shouldEnd: bool = False

    firstFit: List[Tick] = deepcopy(firstHistory)
    bestFit: List[Tick] = deepcopy(bestHistory)
    worstFit: List[Tick] = deepcopy(worstHistory)
 
    currFirstFit: Tick = None
    currBestFit: Tick = None
    currWorstFit: Tick = None

    while True:
        shouldEnd = len(firstFit) == 0 and len(bestFit) == 0 and len(worstFit) == 0

        system("clear")

        currFirstFit = firstFit.pop(0) if len(firstFit) > 0 else None
        currBestFit = bestFit.pop(0) if len(bestFit) > 0 else None
        currWorstFit = worstFit.pop(0) if len(worstFit) > 0 else None

        cprint("Time elapsed: ", "green", end="")
        cprint(str(seconds) + "s" + "\n", attrs=['bold'])

        cprint("First Fit", "yellow", attrs=['bold', 'underline'])
        if currFirstFit != None:
            displayTick(currFirstFit)
        else:
            displayTotal(firstHistory, firstJobs, firstBlocks)

        cprint("Best Fit", "yellow", attrs=['bold', 'underline'])
        if currBestFit != None:
            displayTick(currBestFit)
        else:
            displayTotal(bestHistory, bestJobs, bestBlocks)

        cprint("Worst Fit", "yellow", attrs=['bold', 'underline'])
        if currWorstFit != None:
            displayTick(currWorstFit)
        else:
            displayTotal(worstHistory, worstJobs, worstBlocks)

        if shouldEnd:
            break

        seconds += 1

        sleep(0.6)

# First Fit
firstHistory, firstBlocks, firstJobs = calculate(deepcopy(jobs), deepcopy(blocks))

# Best Fit
bestHistory, bestBlocks, bestJobs = calculate(deepcopy(jobs), deepcopy(sorted(blocks, key=lambda x: x.size )))

# Worst Fit
worstHistory, worstBlocks, worstJobs = calculate(deepcopy(jobs), deepcopy(sorted(blocks, key=lambda x: x.size, reverse=True)))

run(firstHistory, firstJobs, firstBlocks, bestHistory, bestJobs, bestBlocks, worstHistory, worstJobs, worstBlocks)