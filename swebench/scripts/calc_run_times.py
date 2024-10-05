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
    # Add argument parser
    parser = argparse.ArgumentParser(description="Calculate build and evaluation times")
    parser.add_argument(
        "--asc", action="store_true", help="Sort times in ascending order"
    )
    parser.add_argument(
        "--limit", type=int, default=100, help="Limit the number of results printed"
    )
    args = parser.parse_args()

    log_files = glob.glob(
        "logs/run_evaluation/all_100/gold/*/image_build_dir/build_image.log"
    )
    results = []

    for file_path in log_files:
        project, duration = process_log_file(file_path)
        if project and duration:
            results.append((project, duration))

    # Sort results based on the --asc flag
    results.sort(key=lambda x: x[1], reverse=not args.asc)

    # Print results
    print("Build times ({}):".format("ascending" if args.asc else "descending"))
    for project, duration in results[: args.limit]:
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

    # Sort evaluation results based on the --asc flag
    evaluation_results.sort(key=lambda x: x[1], reverse=not args.asc)

    # Print evaluation results
    print("\nEvaluation times ({}):".format("ascending" if args.asc else "descending"))
    for project, duration in evaluation_results[: args.limit]:
        project_name = project.replace("logs/run_evaluation/all_100/gold/", "")
        print(f"{project_name}: {duration}")

    # Create a dictionary to store all times for each project
    project_times = {}

    # Process build times
    for file_path in log_files:
        project, build_duration = process_log_file(file_path)
        if project and build_duration:
            project_name = project.replace(
                "logs/run_evaluation/all_100/gold/", ""
            ).replace("/image_build_dir", "")
            project_times[project_name] = {"build": build_duration}

    # Process run_instance times
    for file_path in run_instance_logs:
        project = os.path.dirname(file_path)
        instance_duration = process_run_instance_log(file_path)
        if instance_duration:
            project_name = project.replace("logs/run_evaluation/all_100/gold/", "")
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
        "\nTotal, Build, and Instance Times ({}):".format(
            "ascending" if args.asc else "descending"
        )
    )
    print(
        "{:<30} {:<20} {:<20} {:<20}".format(
            "Project", "Total Time", "Build Time", "Instance Time"
        )
    )
    print("-" * 90)
    for project, total, build, instance in table_results[: args.limit]:
        print(
            "{:<30} {:<20} {:<20} {:<20}".format(
                project,
                format_timedelta(total),
                format_timedelta(build) if build else "N/A",
                format_timedelta(instance) if instance else "N/A",
            )
        )

    # Create a set to store unique project names
    unique_projects = set()

    # Process build times
    for file_path in log_files:
        project, _ = process_log_file(file_path)
        if project:
            project_name = project.replace(
                "logs/run_evaluation/all_100/gold/", ""
            ).replace("/image_build_dir", "")
            unique_projects.add(project_name)

    # Process run_instance times
    for file_path in run_instance_logs:
        project = os.path.dirname(file_path)
        project_name = project.replace("logs/run_evaluation/all_100/gold/", "")
        unique_projects.add(project_name)

    # Sort project names alphabetically and print the first 50
    sorted_projects = sorted(unique_projects)
    print("\nFirst 50 project names (alphabetically):")
    print(" ".join(sorted_projects[:50]))

    # Create a dictionary to store all times for each project
    project_times = {}

    # Process build times
    for file_path in log_files:
        project, build_duration = process_log_file(file_path)
        if project and build_duration:
            project_name = project.replace(
                "logs/run_evaluation/all_100/gold/", ""
            ).replace("/image_build_dir", "")
            project_times[project_name] = {"build": build_duration}

    # Process run_instance times
    for file_path in run_instance_logs:
        project = os.path.dirname(file_path)
        instance_duration = process_run_instance_log(file_path)
        if instance_duration:
            project_name = project.replace("logs/run_evaluation/all_100/gold/", "")
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
        "\nTotal, Build, and Instance Times ({}):".format(
            "ascending" if args.asc else "descending"
        )
    )
    print(
        "{:<30} {:<20} {:<20} {:<20}".format(
            "Project", "Total Time", "Build Time", "Instance Time"
        )
    )
    print("-" * 90)
    for project, total, build, instance in table_results[: args.limit]:
        print(
            "{:<30} {:<20} {:<20} {:<20}".format(
                project,
                format_timedelta(total),
                format_timedelta(build) if build else "N/A",
                format_timedelta(instance) if instance else "N/A",
            )
        )

    # Create a set to store unique project names
    unique_projects = set()

    # Process build times
    for file_path in log_files:
        project, _ = process_log_file(file_path)
        if project:
            project_name = project.replace(
                "logs/run_evaluation/all_100/gold/", ""
            ).replace("/image_build_dir", "")
            unique_projects.add(project_name)

    # Process run_instance times
    for file_path in run_instance_logs:
        project = os.path.dirname(file_path)
        project_name = project.replace("logs/run_evaluation/all_100/gold/", "")
        unique_projects.add(project_name)

    # Sort project names alphabetically and print the first 50
    sorted_projects = sorted(unique_projects)
    print("\nFirst 50 project names (alphabetically):")
    print(" ".join(sorted_projects[:50]))

    # ... rest of the existing code ...


if __name__ == "__main__":
    main()
