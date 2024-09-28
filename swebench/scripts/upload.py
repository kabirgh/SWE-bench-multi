import argparse
from datasets import load_dataset, Value


def upload_jsonl_to_huggingface(instances_path, dataset_name, private=False):
    # Load the dataset from the JSONL file
    dataset = load_dataset("json", data_files={"test": instances_path})
    print("Test dataset loaded, features: ", dataset["test"].features)  # type: ignore

    # Cast to string to match swe-bench schema
    dataset = dataset.cast_column("created_at", feature=Value("string"))

    # Push the dataset to the Hugging Face Hub
    dataset.push_to_hub(dataset_name, private=private)  # type: ignore
    print(f"Dataset {dataset_name} uploaded to Hugging Face")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload a file or folder containing task instances to Hugging Face as a dataset"
    )
    parser.add_argument(
        "instances_path", type=str, help="Path to the instances_path JSONL file"
    )
    parser.add_argument(
        "dataset_name", type=str, help="Name of the dataset on Hugging Face"
    )
    parser.add_argument(
        "--private", action="store_true", help="Make the dataset private"
    )

    args = parser.parse_args()

    upload_jsonl_to_huggingface(args.instances_path, args.dataset_name, args.private)
