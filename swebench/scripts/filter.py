import json
import argparse

instance_ids = [
    "apache__druid-13704",
    "apache__lucene-13704",
    "facebook__docusaurus-9183",
    "google__gson-2479",
    "apache__druid-14136",
    "caddyserver__caddy-5404",
    "facebook__docusaurus-9897",
    "hashicorp__terraform-34814",
    "apache__druid-15402",
    "caddyserver__caddy-6115",
    "gohugoio__hugo-12448",
    "jqlang__jq-2235",
    "apache__druid-16875",
    "caddyserver__caddy-6345",
    "google__gson-2024",
    "jqlang__jq-2658",
    "apache__lucene-12626",
    "facebook__docusaurus-10130",
    "google__gson-2061",
    "jqlang__jq-2750",
    "apache__lucene-13301",
    "facebook__docusaurus-10309",
    "google__gson-2134",
    "micropython__micropython-12158",
    "apache__lucene-13494",
    "facebook__docusaurus-8927",
    "google__gson-2158",
]


def filter_jsonl(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            data = json.loads(line)
            if data["instance_id"] not in instance_ids:
                outfile.write(line)


def main():
    parser = argparse.ArgumentParser(
        description="Filter JSONL file based on instance IDs"
    )
    parser.add_argument("input_file", help="Path to input JSONL file")
    parser.add_argument("output_file", help="Path to output JSONL file")

    args = parser.parse_args()

    filter_jsonl(args.input_file, args.output_file)
    print(f"Filtered data written to {args.output_file}")


if __name__ == "__main__":
    main()
