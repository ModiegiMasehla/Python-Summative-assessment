# Python Summative Assessment

## Learning Outcomes assessed

- Data Structures
- Data Manipulation
- String Formatting
- Loops
- CLI Commands
- APIs

--

## Assessment Structure

The following Assessment has two sections:

- [Coding Assessment (Questions are below)](#fundamentals-coding-assessment)
- [Long Questions (Questions are below)](#long-format-questions) - `answers.txt`

You can answer them in any order.


## Your Goal

Read the instructions below for each [coding question](#fundamentals-coding-assessment), then complete each function in `summative.py` while ensuring that:

- The code is valid Python
- Each function behaves according to the instructions
- All unit tests pass successfully

Read the instructions below for each [long format question](#long-format-questions), then add your answer under each relevant comment in `answers.txt` while ensuring that:

- You DO NOT remove the comments
- Read each question carefully before answering the question

---

### How to run your tests

To run all your tests

```bash
python3 -m pytest tests/test_summative.py -v
```

To run your tests individually

```bash
python3 -m pytest tests/test_summative.py::<test_method> -v
```

or for more information within the stacktrace use

```bash
python3 -m pytest tests/test_summative.py::<test_method> -vv
```

> **Note:** Run the tests from the root of the project (the folder that contains `summative.py` and `weatherwarnings.json`), otherwise the JSON file cannot be found.

## Scoring & Weighting

| Component                                     | Weight  |
| --------------------------------------------- | ------- |
| Coding Section (unit tests)                   | **50%** |
| Long-format Question (answers.txt)            | **50%** |


--

## Fundamentals Coding Assessment

This assessment consists of five Python functions. Each function has a partially written
implementation. Your task is to **fix the bugs**, **complete the missing logic**, and **ensure all tests pass**.

### Project Structure

```text

├── summative.py                    # <-- This is where you write your solutions
├── answers.txt                     # <-- This is where you write your answers to the long questions
├── weatherwarnings.json            # <-- Data used by Question 4
├── tests/
│   └── test_summative.py           # <-- These are the tests you must make pass
└── README.md                       # <-- Assessment instructions (this file) 
```

### Question 1 - `batch_result_dispatcher(learner_ids)`

The Department of Basic Education needs to send out SMS notifications to learners letting them know that their results are ready to collect. To keep the system running smoothly and avoid "crashing" it, the SMS gateway has a strict limit: *it can only process a maximum of 6 learners at a time in a single "batch" request*.

You have a list (or tuple) of `learner_ids` that need their notifications sent. Your job is to help the IT team at the provincial office in *Polokwane* organise these IDs into smaller groups (sublists) so the system can process them without any errors.

Apply your logic to the `batch_result_dispatcher()` function. The function should take the full collection of IDs and break them down into a nested list where each internal "batch" contains a maximum of 6 IDs. If the total number of learners isn't a perfect multiple of 6, the final batch will simply contain the remaining IDs. Every batch must be a `list`, even when the input is a tuple, and the original input must not be changed.

- **Input:**

```python
['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7']
```

- **Output:**

```python
[['L1', 'L2', 'L3', 'L4', 'L5', 'L6'], ['L7']]
```

Constraint: No sublist should ever exceed 6 items.


### Question 2 - `longest_dry_spell(days)`

Farmers around *Citrusdal* in the Western Cape depend on the winter rains to fill their dams. The local farmers' association keeps a daily record of the weather where `"R"` stands for a day with rain and `"D"` stands for a dry day. After a long season they want to know how serious the dry periods were, so they need the longest run of consecutive dry days.

Apply your logic to the `longest_dry_spell()` function which analyses a list of daily records. The function must count how many times `"D"` appears in a row and return the highest count found.

- **Input:** A list of strings (e.g., ["D", "R", "D", "D", "R", "D", "D", "D"])
- **Output:** An integer representing the longest dry spell (e.g., 3)

If the list is empty, or contains no dry days, the function must return `0`.

---

### Question 3 - `dip_finder(prices)`

A spaza shop owner in *Soweto* buys a 10 kg bag of maize meal from a wholesaler every morning. The price changes from day to day, and she has noticed that some days the price drops sharply before going back up. She wants to identify every "Local Dip" in the price history so she can see which days were the best days to stock up.

A "Local Dip" occurs when one day's price is strictly lower than the day before it **and** the day after it. She has a list of daily wholesale prices (in rands) recorded over the last few weeks.

Apply your logic to the `dip_finder()` function which looks through the list of prices. It should identify any price that is strictly lower than the one immediately before it and the one immediately after it. The first and last prices in the list can never be dips, because they only have one neighbour.

- **Input:** A list of integers (e.g., [95, 92, 94, 90, 93, 89, 91, 96, 88, 90])
- **Output:** A list of the identified dip prices, in the order they appear (e.g., [92, 90, 89, 88])

---


### Question 4 - `warning_summary(records)`

The South African Weather Service (SAWS) issues severe weather warnings for heavy rain, and each warning is given a **level** (`1` being the least severe and `4` being the most severe). Following a stormy November, the SAWS API was taken offline for maintenance, but a junior developer on your team managed to save a snapshot of the warnings before it went down. The data has been saved locally as `weatherwarnings.json` — a list of warnings issued across South African towns, each showing the warning level and the amount of rainfall (in millimetres) that was forecast.

Your team lead needs a quick report: **how many millimetres of rain were forecast in total for each warning level, across all towns and all dates?**

Apply your logic to the `warning_summary()` function. It receives the list of warning records (already loaded from the JSON) and must return a dictionary where each key is a level label (`"Level 1"`, `"Level 2"`, etc.) and each value is the **total rainfall in mm** recorded for that level — rounded to 2 decimal places.

Only include levels that actually appear in the data. If the input is empty, return an empty dictionary.

- **Input:** A list of warning dictionaries, e.g.:
```python
[
    {"warning_id": "SAWS-20251101-001", "town": "Soweto", "municipality": "City of Johannesburg", "province": "Gauteng", "level": 2, "rainfall_mm": 12.5, "date": "2025-11-01", "start_time": "06:00", "end_time": "14:00", "status": "expired", "people_affected": 14200},
    {"warning_id": "SAWS-20251101-002", "town": "Sandton", "municipality": "City of Johannesburg", "province": "Gauteng", "level": 4, "rainfall_mm": 85.0, "date": "2025-11-01", "start_time": "08:00", "end_time": "16:00", "status": "expired", "people_affected": 8750}
]
```

- **Output:**
```python
{"Level 2": 12.5, "Level 4": 85.0}
```

> **Note:** The order of keys in the returned dictionary does not matter. Your function only needs the `level` and `rainfall_mm` fields — the rest of the data is there for context. Remember that adding decimal numbers in Python can produce results like `97.70000000000002`, so make sure your totals are rounded.


### Question 5 - `draw_diamond(size)`

A jewellery shop in *Kimberley*, the home of the famous Big Hole diamond mine, is building a small terminal app that prints diamond-shaped price tags for its window display. The bigger the diamond, the more valuable the item.

Your job is to generate the tag shape. Apply your logic to the `draw_diamond()` function which takes a single integer `size` and returns a **list of strings**, where each string is one row of a hollow diamond made of `*` characters.

#### Rules:
- The diamond must be **centred** — each row is padded with leading spaces so that the points sit in the middle.
- The diamond has `2 * size - 1` rows. The top half (the first `size` rows) grows wider, and the bottom half mirrors the top half.
- The **first row** and the **last row** have exactly one `*`.
- Every other row has exactly two `*` characters with spaces in between.
- The **widest row** is the middle row and its width is `2 * size - 1`.
- If `size` is `1`, the diamond is just a single `*`.
- Rows must **not** have trailing spaces.
- If `size` is less than `1`, the function must raise a `ValueError`.

- **Input:** `4`
- **Output:**

```
   *
  * *
 *   *
*     *
 *   *
  * *
   *
```

Returned as:
```python
[
    "   *",
    "  * *",
    " *   *",
    "*     *",
    " *   *",
    "  * *",
    "   *"
]
```


## Long-Format Questions

Please answer these in the `answers.txt` file (**DO NOT REMOVE THE COMMENTS AND DO NOT CHANGE THE FORMAT**)

### Comprehension Question 1 — Linux Navigation & File Management (10 Points)

You have just been given access to a remote Linux server at a logistics company in Durban. Your manager has given you the following tasks to complete:

1. Find out which folder you are currently in and see what files and folders are inside it
2. Move into a folder called `reports`
3. Read the last 20 lines of a very large file called `sales.log`
4. Create a new folder called `archive`
5. Move a file called `old_sales.csv` into the `archive` folder
6. Permanently delete a folder called `temp_files` and everything inside it

Describe **exactly how you would complete each task** — what command you would use, what it does, and why you chose it. Also explain any risks involved in any of your steps and how you would handle them carefully.


### Comprehension Question 2 — Loops (10 Points)

A junior developer at a Port Elizabeth software company wrote a program to look for a customer in a list of 50 000 records. The program works, but it keeps checking every record even after the customer has been found, and last week a different loop they wrote never stopped running and froze a server.

Your tech lead has asked you to explain to the junior developer how to control the flow of a loop and keep it safe. In your own words, explain how `break` and `continue` work, what causes an infinite loop and how to prevent one, and what nested loops are and when they are (and are not) a good idea. Make sure your explanation is grounded in realistic situations a developer might actually find themselves in, not just theory.


### Comprehension Question 3 — Mutable Data and Side Effects (10 Points)

A colleague at a Pretoria fintech company is confused. They wrote a function that takes a list of transactions, removes the cancelled ones and returns the result. The function works, but afterwards the original list in the rest of their program has also lost those transactions, and nobody understands why. When they wrote the same kind of function with a string, the original was never affected.

Explain to your colleague what is going on. Your explanation should cover how Python passes objects into functions, the difference between mutable and immutable types when they are changed inside a function, the difference between assigning a list to a new variable and actually copying it (including shallow vs deep copies), and how to write functions that avoid this kind of surprise.


### Comprehension Question 4 — APIs, JSON and Status Codes (10 Points)

A developer at a Cape Town startup has to fetch live weather data from a third-party weather service and show it in the company's app. They have never used an API before and ask you to guide them through what to expect.

Explain to this developer how consuming an API works in practice. Your explanation should cover what JSON is and why APIs use it, what the common HTTP request methods (GET, POST, PUT, PATCH, DELETE) are used for, how to read the HTTP status codes that come back (for example 200, 201, 400, 401, 404 and 500) and what each family of codes means, what an API key and request parameters are, and how you would write code in Python to make a request and handle the situation where something goes wrong.
