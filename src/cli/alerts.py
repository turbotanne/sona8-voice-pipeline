import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--message', required=True)

if __name__ == '__main__':
    args = parser.parse_args()
    print(args.message)