import paramiko
import getpass
import os
import stat


class SshConnection:
    def __init__(self, server, user, verbose=False):
        # download from remote
        self.user = user
        self.server = server
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        passwd = getpass.getpass()
        self.connection.connect(server, username=user, password=passwd)
        self.sftp = self.connection.open_sftp()
        self.verbose = verbose
        if self.verbose:
            print("Connection to remote : {}".format(self.server))
            print("With user {}".format(self.user))

    def __del__(self):
        if self.verbose:
            print("closing remote connection : {}".format(self.server))
        self.sftp.close()
        self.connection.close()

    def command(self, command):
        if self.verbose:
            print("Executing command on host : {}".format(command))
        stdin, stdout, stderr = self.connection.exec_command(command)
        lines = []
        for line in stdout.readlines():
            lines.append(line[:-1])
        return lines

    def download_dir(self, remote_path, host_path):
        if self.verbose:
            print("Download directory: {}".format(remote_path))
        if os.path.splitext(host_path)[1] != '':
            self.sftp.get(remote_path, host_path)
            return
        os.path.exists(host_path) or os.makedirs(host_path)
        dir_items = self.sftp.listdir_attr(remote_path)
        for item in dir_items:
            r_path = os.path.join(remote_path, item.filename)
            l_path = os.path.join(host_path, item.filename)
            if stat.S_ISDIR(item.st_mode):
                self.download_dir(r_path, l_path)
            else:
                self.download_file(r_path, l_path)

    def download_file(self, remote_file, host_path):
        if self.verbose:
            print("Download file : {}".format(remote_file))
        self.sftp.get(remote_file, host_path)

