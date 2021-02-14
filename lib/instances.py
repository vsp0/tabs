from . import bservers
import paramiko
import zipfile
import random
import string
import os

instances = []


class Instance:
    def __init__(self, source, delay):
        self.source = source
        self.delay = delay

        self.id = self.__new_id()

        instances.append(self)
    
    def backup(self):
        for bserver in bservers.bservers:
            if bserver.can_connect():
                tp = paramiko.Transport((bserver.ip, 22))
                tp.connect(username=bserver.user, password=bserver.passwd)

                target = f'/home/{bserver.user}/TABS/Instances/{self.id}'

                with SFTPClient.from_transport(tp) as sftp:
                    sftp.mkdir(target, ignore_existing=True)
                    sftp.put_dir(self.source, target)
                
                   
    def __new_id(self):
        return  'b-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))


class SFTPClient(paramiko.SFTPClient):
    def put_dir(self, source, target):
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                self.put(os.path.join(source, item), '%s/%s' % (target, item))

            else:
                self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                self.put_dir(os.path.join(source, item), '%s/%s' % (target, item))

    def mkdir(self, path, mode=511, ignore_existing=False):
        try:
            super(SFTPClient, self).mkdir(path, mode)

        except IOError:
            if ignore_existing:
                pass

            else:
                raise
