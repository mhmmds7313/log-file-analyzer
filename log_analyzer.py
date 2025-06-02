import re
from datetime import datetime

LOG_PATTERN = re.compile(r'^(?P<timestamp>[\d\-:\s,]+) - (?P<level>\w+) - (?P<message>.+)$')

def parse_line(line):
    match = LOG_PATTERN.match(line)
    if match:
        timestamp_str = match.group('timestamp')
        level = match.group('level')
        message = match.group('message')
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
        return {
            'timestamp': timestamp,
            'level': level,
            'message': message
        }
    return None





def read_log_file(filename):
    parsed_logs = []
    with open(filename, 'r') as f:
        for line in f:
            parsed = parse_line(line.strip())
            if parsed:
                parsed_logs.append(parsed)
    return parsed_logs







def count_log_levels(logs):
    level_counts = {}
    for log in logs:
        level = log['level']
        level_counts[level] = level_counts.get(level, 0) + 1
    return level_counts





def filter_logs_by_date(logs, start_date, end_date):
    return [
        log for log in logs
        if start_date <= log['timestamp'] <= end_date
    ]







import csv

def export_summary_to_csv(summary, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Level', 'Count'])
        for level, count in summary.items():
            writer.writerow([level, count])








if __name__ == "__main__":
    logs = read_log_file('sample.log')

    start = datetime(2025, 6, 3, 12, 31, 0)
    end = datetime(2025, 6, 3, 12, 34, 0)

    filtered_logs = filter_logs_by_date(logs, start, end)
    level_summary = count_log_levels(filtered_logs)

    print("Log Level Summary (Filtered):")
    for level, count in level_summary.items():
        print(f"{level}: {count}")

    export_summary_to_csv(level_summary, 'report.csv')
    print("Report saved to report.csv")






