import argparse

from src.pipeline import VoicePipeline

parser = argparse.ArgumentParser()
parser.add_argument('--file', required=True)

if __name__ == '__main__':
    args = parser.parse_args()
    pipeline = VoicePipeline()
    print(pipeline)