from . import bservers
import paramiko
import datetime
import random
import string
import os

instances = []


class Instance:
    def __init__(self, source, delay):
        self.source = source
        self.delay = int(delay)
        self.backup_next = None

        self.id = self.__new_id()

        instances.append(self)
    
    def backup(self):
        for bserver in bservers.bservers:
            if bserver.can_connect():
                print(f'Successfully connected to {bserver.ip}...')

                tp = paramiko.Transport((bserver.ip, 22))
                tp.connect(username=bserver.user, password=bserver.passwd)

                target = bservers.get_target(bserver, self)

                with FolderSFTPClient.from_transport(tp) as sftp:
                    sftp.mkdir(target, ignore_existing=True)
                    sftp.put_dir(self.source, target)
            
            else:
                print(f'Failed to connect to {bserver.ip}...')
    
    def is_time_between(self, begin_time):
        one_second = datetime.timedelta(seconds=1)
        end_time = datetime.datetime.now() + one_second
    
        return self.backup_next >= begin_time and self.backup_next <= end_time

    def __new_id(self):
        return  'b-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))


class FolderSFTPClient(paramiko.SFTPClient):
    def put_dir(self, source, target):
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                self.put(os.path.join(source, item), '%s/%s' % (target, item))

            else:
                self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                self.put_dir(os.path.join(source, item), '%s/%s' % (target, item))

    def mkdir(self, path, mode=511, ignore_existing=False):
        try:
            super(FolderSFTPClient, self).mkdir(path, mode)

        except IOError:
            if ignore_existing:
                pass

            else:
                raise
