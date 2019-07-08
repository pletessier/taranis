import argparse
import sys

from config import config
from dotmap import DotMap

from utils.singleton import Singleton


class Configuration(metaclass=Singleton):
    def __init__(self):
        parser = argparse.ArgumentParser(prog='Taranis', description='Taranis server')
        parser.add_argument('--config-file', '-F', dest='config_files', action='append', type=str,
                            help='a list of yaml config files')
        parser.add_argument('--config-path', '-P', dest='config_paths', action='append', type=str,
                            help='a list of directories in which the file paths are keys and file contents are value')
        parser.add_argument('--additional-config', '-C', dest='additional_config', action='append', type=str,
                            help='a list of dotted.key=value configs')
        # args = parser.parse_args()
        args, unknowns = parser.parse_known_args()

        if unknowns:
            parser.print_usage()
            sys.exit(1)

        configurations = list()
        configurations.append(dict(i.split("=") for i in args.additional_config) if args.additional_config else dict())
        configurations.append("env")
        if args.config_paths:
            configurations.extend(args.config_paths)
        if args.config_files:
            configurations.extend(args.config_files)

        confSet = config(*configurations, prefix="TARANIS", remove_level=0)

        tempdict = dict()

        for key, value in confSet.as_dict().items():
            tree = key.split('.')
            root = tempdict
            for i, b in enumerate(tree):
                if b not in root:
                    if (i + 1) == len(tree):
                        root[b] = value
                    else:
                        root[b] = dict()
                root = root[b]
        self.dict = DotMap(tempdict)


configuration = Configuration().dict
print("Config is : \n{}".format(configuration))
