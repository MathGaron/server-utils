from argument_parser import ArgumentParser
import sys
import json
import os

from ssh_connection import SshConnection

if __name__ == '__main__':
    args = ArgumentParser(sys.argv[1:])
    if args.help:
        args.print_help()
        sys.exit(1)

    with open(args.config_file) as data_file:
        data = json.load(data_file)


    server = data["server"]
    user = data["user"]
    remote_path = data["remote_path"]
    host_path = data["host_path"]

    if not os.path.exists(host_path):
        os.mkdir(host_path)

    ssh = SshConnection(server, user, args.verbose)
    ssh.download_dir(remote_path, host_path)