import os
import argparse
import sys
import hashlib

def parse_args():
    parser = argparse.ArgumentParser(description="Hash Utility")
    parser.add_argument('--algo', choices=['md5', 'sha256', 'sha384'], required=True, help="Hash algorithm")
    parser.add_argument('--input', help="Input file to hash")
    return parser.parse_args()

def main():
    args = parse_args()
    if not args.input or not os.path.isfile(args.input):
        print("Invalid input file.")
        sys.exit(1)

    with open(args.input, 'rb') as f:
        data = f.read()

    if args.algo == 'md5':
        hash_value = hashlib.md5(data).hexdigest()
    elif args.algo == 'sha256':
        hash_value = hashlib.sha256(data).hexdigest()
    elif args.algo == 'sha384':
        hash_value = hashlib.sha384(data).hexdigest()

    print(f"{args.algo} hash of {args.input}: {hash_value}")

if __name__ == "__main__":
    main()