import numpy as np

# input_file = "test_input_02.txt"
input_file = "input_02.txt"

def next_line_as_report(file):
    with open(file, "r") as f:
        for line in f:
            yield list(map(int, line.strip().split()))

report_generator = next_line_as_report(input_file)

def safe_report_count():
    safe_report_count = 0
    for report in report_generator:
        safe_report_count += 1 if is_report_safe(report) or is_dampened_report_safe(report) else 0
    print(f"safe reports = {safe_report_count}")

def is_report_safe(report):
    diffs = np.diff(report)
    is_negative = diffs[0] < 0
    if is_negative:
        diffs = [i * -1 for i in diffs]
    for i, diff in enumerate(diffs):
        if not 0 < diff <= 3:
            return False
    return True

def is_dampened_report_safe(report):
    for i in range(len(report)):
        dampened_report = report[:i] + report[i + 1:]
        if is_report_safe(dampened_report):
            return True
    return False

safe_report_count()
