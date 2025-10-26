import time
import os

passwd = 'MY870322'

def sync():
    while True:
        try:
            os.system('echo %s | sudo -S %s' % (passwd, 'systemctl restart chrony'))
            time.sleep(1)
        except KeyboardInterrupt:
            print('sync return')
            return