import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    args = parser.parse_args()
    print(f"Ingest {args.source}")

if __name__ == '__main__':
    main()