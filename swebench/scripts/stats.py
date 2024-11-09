import json
import re
from collections import defaultdict
import statistics


def count_lines_updated(patch):
    added = sum(
        1
        for line in patch.split("\n")
        if line.startswith("+") and not line.startswith("+++")
    )
    removed = sum(
        1
        for line in patch.split("\n")
        if line.startswith("-") and not line.startswith("---")
    )
    return added + removed


def count_files_updated(patch):
    return len(re.findall(r"diff --git", patch))


def count_tests(test_patch):
    if not test_patch:
        return 0
    return len(re.findall(r"(new file|index|similarity index)", test_patch))


REPO_LENGTH = 30
ISSUE_TEXT_LENGTH = 12
CODEBASE_LINES_LENGTH = 15
CODEBASE_FILES_LENGTH = 15
LINES_UPDATED_LENGTH = 14
FILES_UPDATED_LENGTH = 14
F2P_TESTS_LENGTH = 10
P2P_TESTS_LENGTH = 10


def main():
    print(
        f"|{'Repository'.ljust(REPO_LENGTH)}|{'Issue text'.ljust(ISSUE_TEXT_LENGTH)}|{'Codebase lines'.ljust(CODEBASE_LINES_LENGTH)}|{'Codebase files'.ljust(CODEBASE_FILES_LENGTH)}|{'Lines Updated'.ljust(LINES_UPDATED_LENGTH)}|{'Files Updated'.ljust(FILES_UPDATED_LENGTH)}|{'F2P Tests'.ljust(F2P_TESTS_LENGTH)}|{'P2P Tests'.ljust(P2P_TESTS_LENGTH)}|"
    )
    print(
        f"|{'-' * REPO_LENGTH}|{'-' * ISSUE_TEXT_LENGTH}|{'-' * CODEBASE_LINES_LENGTH}|{'-' * CODEBASE_FILES_LENGTH}|{'-' * LINES_UPDATED_LENGTH}|{'-' * FILES_UPDATED_LENGTH}|{'-' * F2P_TESTS_LENGTH}|{'-' * P2P_TESTS_LENGTH}|"
    )

    repo_data = defaultdict(lambda: defaultdict(list))
    repo_data["apache/druid"]["line_count"].append(2969856)
    repo_data["apache/druid"]["file_count"].append(10759)

    repo_data["apache/lucene"]["line_count"].append(959224)
    repo_data["apache/lucene"]["file_count"].append(5891)

    repo_data["babel/babel"]["line_count"].append(3703125)
    repo_data["babel/babel"]["file_count"].append(46990)

    repo_data["caddyserver/caddy"]["line_count"].append(52636)
    repo_data["caddyserver/caddy"]["file_count"].append(369)

    repo_data["facebook/docusaurus"]["line_count"].append(979645)
    repo_data["facebook/docusaurus"]["file_count"].append(9944)

    repo_data["gohugoio/hugo"]["line_count"].append(194084)
    repo_data["gohugoio/hugo"]["file_count"].append(1928)

    repo_data["google/gson"]["line_count"].append(36107)
    repo_data["google/gson"]["file_count"].append(297)

    repo_data["hashicorp/terraform"]["line_count"].append(485051)
    repo_data["hashicorp/terraform"]["file_count"].append(3689)

    repo_data["immutable-js/immutable-js"]["line_count"].append(3193382)
    repo_data["immutable-js/immutable-js"]["file_count"].append(17190)

    repo_data["jqlang/jq"]["line_count"].append(222132)
    repo_data["jqlang/jq"]["file_count"].append(327)

    repo_data["micropython/micropython"]["line_count"].append(2079112)
    repo_data["micropython/micropython"]["file_count"].append(9642)

    repo_data["mrdoob/three.js"]["line_count"].append(1971946)
    repo_data["mrdoob/three.js"]["file_count"].append(19247)

    repo_data["nlohmann/json"]["line_count"].append(102396)
    repo_data["nlohmann/json"]["file_count"].append(802)

    repo_data["nushell/nushell"]["line_count"].append(230876)
    repo_data["nushell/nushell"]["file_count"].append(1593)

    repo_data["preactjs/preact"]["line_count"].append(2627871)
    repo_data["preactjs/preact"]["file_count"].append(18435)

    repo_data["projectlombok/lombok"]["line_count"].append(162133)
    repo_data["projectlombok/lombok"]["file_count"].append(2467)

    repo_data["prometheus/prometheus"]["line_count"].append(317733)
    repo_data["prometheus/prometheus"]["file_count"].append(965)

    repo_data["redis/redis"]["line_count"].append(268427)
    repo_data["redis/redis"]["file_count"].append(1492)

    repo_data["systemd/systemd"]["line_count"].append(1167943)
    repo_data["systemd/systemd"]["file_count"].append(3942)

    repo_data["tokio-rs/tokio"]["line_count"].append(91799)
    repo_data["tokio-rs/tokio"]["file_count"].append(765)

    repo_data["uutils/coreutils"]["line_count"].append(187649)
    repo_data["uutils/coreutils"]["file_count"].append(2061)

    repo_data["vuejs/core"]["line_count"].append(5594701)
    repo_data["vuejs/core"]["file_count"].append(13461)

    with open("dataset/all/instances.jsonl", "r") as f:
        for line in f:
            data = json.loads(line)
            repo = data["repo"]
            patch = data["patch"]

            lines_updated = count_lines_updated(patch)
            files_updated = count_files_updated(patch)
            f2p_tests = len(data["FAIL_TO_PASS"])
            p2p_tests = len(data["PASS_TO_PASS"])

            repo_data[repo]["issue_text"].append(len(data["problem_statement"]))
            repo_data[repo]["lines_updated"].append(lines_updated)
            repo_data[repo]["files_updated"].append(files_updated)
            repo_data[repo]["f2p_tests"].append(f2p_tests)
            repo_data[repo]["p2p_tests"].append(p2p_tests)

    for repo, stats in repo_data.items():
        median_issue_text = statistics.median(stats["issue_text"])
        median_lines = statistics.median(stats["lines_updated"])
        median_files = statistics.median(stats["files_updated"])
        codebase_line_count = statistics.median(stats.get("line_count", [0]))
        codebase_file_count = statistics.median(stats.get("file_count", [0]))
        median_f2p = statistics.median(stats["f2p_tests"])
        median_p2p = statistics.median(stats["p2p_tests"])

        print(
            f"|{repo:<{REPO_LENGTH}}|{round(median_issue_text):<{ISSUE_TEXT_LENGTH}}|{codebase_line_count:<{CODEBASE_LINES_LENGTH}}|{codebase_file_count:<{CODEBASE_FILES_LENGTH}}|{round(median_lines):<{LINES_UPDATED_LENGTH}}|{round(median_files):<{FILES_UPDATED_LENGTH}}|{round(median_f2p):<{F2P_TESTS_LENGTH}}|{round(median_p2p):<{P2P_TESTS_LENGTH}}|"
        )


if __name__ == "__main__":
    main()
