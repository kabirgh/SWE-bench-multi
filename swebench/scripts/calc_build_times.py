import os
import glob
from datetime import datetime
import re


def parse_timestamp(line):
    match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})", line)
    if match:
        return datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S,%f")
    return None


def process_log_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        if len(lines) < 2:
            return None, None

        first_line = lines[0]
        second_last_line = lines[-2]

        start_time = parse_timestamp(first_line)
        end_time = parse_timestamp(second_last_line)

        if start_time and end_time:
            duration = end_time - start_time
            return os.path.dirname(file_path), duration

    return None, None


def process_run_instance_log(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        if len(lines) < 2:
            return None

        first_line = lines[0]
        last_line = lines[-1]

        start_time = parse_timestamp(first_line)
        end_time = parse_timestamp(last_line)

        if start_time and end_time:
            duration = end_time - start_time
            return duration

    return None


def main():
    log_files = glob.glob(
        "logs/run_evaluation/all_100/gold/*/image_build_dir/build_image.log"
    )
    results = []

    for file_path in log_files:
        project, duration = process_log_file(file_path)
        if project and duration:
            results.append((project, duration))

    # Sort results by duration in descending order
    results.sort(key=lambda x: x[1], reverse=True)

    # Print results
    print("Top 10 longest build times:")
    for project, duration in results[:10]:
        project_name = project.replace("logs/run_evaluation/all_100/gold/", "").replace(
            "/image_build_dir", ""
        )
        print(f"{project_name}: {duration}")

    # Process run_instance.log files
    run_instance_logs = glob.glob("logs/run_evaluation/all_100/gold/*/run_instance.log")
    evaluation_results = []

    for file_path in run_instance_logs:
        project = os.path.dirname(file_path)
        duration = process_run_instance_log(file_path)
        if duration:
            evaluation_results.append((project, duration))

    # Sort evaluation results by duration in descending order
    evaluation_results.sort(key=lambda x: x[1], reverse=True)

    # Print evaluation results
    print("\nTop 10 longest evaluation times:")
    for project, duration in evaluation_results[:10]:
        project_name = project.replace("logs/run_evaluation/all_100/gold/", "")
        print(f"{project_name}: {duration}")


if __name__ == "__main__":
    main()
