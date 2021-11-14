import argparse


class ArgParser:

    @property
    def parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("map_file", type=str, help='filename to read map')

        return parser

    @property
    def args(self):
        return self.parser.parse_args()
