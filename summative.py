##################
#   Question 1   #
##################

def batch_result_dispatcher(learner_ids: list | tuple) -> list:
    batches = []

    for i in range(0, len(learner_ids), 6):
        batches.append(list(learner_ids[i:i + 6]))

    return batches


##################
#   Question 2   #
##################

def longest_dry_spell(days: list) -> int:
    longest = 0
    current = 0

    for day in days:
        if day == "D":
            current += 1
            if current > longest:
                longest = current
        else:
            current = 0

    return longest


##################
#   Question 3   #
##################

def dip_finder(prices: list) -> list:
    dips = []

    for i in range(1, len(prices) - 1):
        if prices[i] < prices[i - 1] and prices[i] < prices[i + 1]:
            dips.append(prices[i])

    return dips


##################
#   Question 4   #
##################

def warning_summary(records: list) -> dict:
    totals = {}

    for record in records:
        label = f"Level {record['level']}"
        totals[label] = totals.get(label, 0) + record["rainfall_mm"]

    return {label: round(total, 2) for label, total in totals.items()}


##################
#   Question 5   #
##################

def draw_diamond(size: int) -> list:
    if size < 1:
        raise ValueError("size must be at least 1")

    top = []

    for i in range(size):
        padding = " " * (size - 1 - i)
        if i == 0:
            top.append(padding + "*")
        else:
            top.append(padding + "*" + " " * (2 * i - 1) + "*")

    return top + top[-2::-1]
