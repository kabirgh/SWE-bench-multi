# Sort instances to ensure consistent ordering
all_instances.sort(key=lambda x: x["instance_id"])

# Next create dummy_predictions.json file to check if tests fail before patch is applied
empty_patch = """diff --git a/empty.txt b/empty.txt
new file mode 100644
index 0000000..e69de29
--- /dev/null
+++ b/empty.txt
"""
dummy_predictions = []
for instance in all_instances:
    dummy_predictions.append(
        {
            "instance_id": instance["instance_id"],
            "model_name_or_path": "empty",
            "model_patch": empty_patch,
        }
    )

# Write empty predictions
with open(os.path.join(output_dir, "dummy_predictions.json"), "w+") as f:
    json.dump(dummy_predictions, f, indent=2)

print(
    f"Created predictions file to apply dummy patch: {output_dir}/dummy_predictions.json"
)