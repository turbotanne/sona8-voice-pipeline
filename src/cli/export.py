import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dest', required=True)
    args = parser.parse_args()
    print(f"Export to {args.dest}")

if __name__ == '__main__':
    main()