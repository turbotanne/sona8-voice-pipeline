import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    args = parser.parse_args()
    print(f"Summarize {args.file}")

if __name__ == '__main__':
    main()