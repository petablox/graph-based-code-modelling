import json
import sys

file_to_force = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]

print("forcing file", file_to_force, "from", input_file, "to", output_file)


c = open(input_file).read().split("\n")

with open(output_file, "a") as f:
    for line in c:
        if not line: continue

        line_obj = json.loads(line)
        if file_to_force in line_obj["Filename"]:
                f.write(line + "\n")
