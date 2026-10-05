import argparse


def run() -> None:
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("config")
        args = parser.parse_args(["config.json"])
        print(args)
    except FileNotFoundError:
        print("Config file not found.")

