import os
import glob
from datetime import datetime, timedelta
import re
import argparse


def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"


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
    parser = argparse.ArgumentParser(description="Calculate build and evaluation times")
    parser.add_argument(
        "--asc", action="store_true", help="Sort times in ascending order"
    )
    parser.add_argument(
        "--limit", type=int, default=100, help="Limit the number of results printed"
    )
    parser.add_argument(
        "--dir",
        type=str,
        default="all_100",
        help="Directory name under logs/run_evaluation to process",
    )
    args = parser.parse_args()

    log_files = glob.glob(
        f"logs/run_evaluation/{args.dir}/gold/*/image_build_dir/build_image.log"
    )
    results = []

    for file_path in log_files:
        project, duration = process_log_file(file_path)
        if project and duration:
            results.append((project, duration))

    # Process run_instance.log files
    run_instance_logs = glob.glob(
        f"logs/run_evaluation/{args.dir}/gold/*/run_instance.log"
    )
    evaluation_results = []

    for file_path in run_instance_logs:
        project = os.path.dirname(file_path)
        duration = process_run_instance_log(file_path)
        if duration:
            evaluation_results.append((project, duration))

    # Create a dictionary to store all times for each project
    project_times = {}

    # Process build times
    for file_path in log_files:
        project, build_duration = process_log_file(file_path)
        if project and build_duration:
            project_name = project.replace(
                f"logs/run_evaluation/{args.dir}/gold/", ""
            ).replace("/image_build_dir", "")
            project_times[project_name] = {"build": build_duration}

    # Process run_instance times
    for file_path in run_instance_logs:
        project = os.path.dirname(file_path)
        instance_duration = process_run_instance_log(file_path)
        if instance_duration:
            project_name = project.replace(f"logs/run_evaluation/{args.dir}/gold/", "")
            if project_name in project_times:
                project_times[project_name]["instance"] = instance_duration
            else:
                project_times[project_name] = {"instance": instance_duration}

    # Calculate total times and prepare results
    table_results = []
    for project, times in project_times.items():
        build_time = times.get("build", timedelta(0))
        instance_time = times.get("instance", timedelta(0))
        total_time = build_time + instance_time
        table_results.append((project, total_time, build_time, instance_time))

    # Sort results based on the --asc flag
    table_results.sort(key=lambda x: x[1], reverse=not args.asc)

    # Print table
    print(
        "{:<35} {:<15} {:<15} {:<15}".format(
            "Project", "Total Time", "Build Time", "Instance Time"
        )
    )
    print("-" * 85)
    for project, total, build, instance in table_results[: args.limit]:
        print(
            "{:<35} {:<15} {:<15} {:<15}".format(
                project,
                format_timedelta(total),
                format_timedelta(build) if build else "N/A",
                format_timedelta(instance) if instance else "N/A",
            )
        )


if __name__ == "__main__":
    main()
