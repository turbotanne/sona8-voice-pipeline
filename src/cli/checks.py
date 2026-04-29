import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--suite', required=True)

if __name__ == '__main__':
    args = parser.parse_args()
    print(args.suite)