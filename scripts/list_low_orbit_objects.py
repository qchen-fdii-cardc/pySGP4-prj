import sys

# Path to the 3LE file (default or from command line)
THREE_LE_FILE = sys.argv[1] if len(sys.argv) > 1 else "low-orbit-30-3le.txt"


# Define a function to parse 3LE files
def parse_3le(file_path):
    objects = []
    with open(file_path, "r") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 3):
            if i + 2 < len(lines):
                name = lines[i].strip()
                line1 = lines[i + 1].strip()
                line2 = lines[i + 2].strip()
                objects.append((name, line1, line2))
    return objects


# Main script
def main():
    objects = parse_3le(THREE_LE_FILE)
    print(f"Found {len(objects)} low orbit objects:")
    for obj in objects:
        print(obj[0])


if __name__ == "__main__":
    main()
