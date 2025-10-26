import os
import threading
import datetime

root = '/home/hit-meiyu/code/device_0'
passwd = 'MY870322'
net_device = 'enp8s0'

def env_init():
	rs = []
	rs.append(os.system('cd '+root))
	command1 = 'ifconfig ' + net_device + ' 192.168.1.102 netmask 255.255.255.0'
	command4 = 'systemctl enable chrony'
	command5 = 'systemctl start chrony'
	rs.append(os.system('echo %s | sudo -S %s' % (passwd, command1)))
	os.system('echo %s | sudo -S %s' % (passwd, command4))
	os.system('echo %s | sudo -S %s' % (passwd, command5))
	os.system('python -V')
	for r in rs:
		if r!=0:
			print('Initiation error!')
			return False
	print('Environment initiation done!')
	return True

def run_command(command):
	try:
		print('command %s start running %s' % (command, datetime.datetime.now()))
		os.system(command)
		print('command %s finish running %s' % (command, datetime.datetime.now()))
	except:
		print('%s\t run failed' % (command))
try:
	env_init()
	time = datetime.datetime.now()
	time = time.strftime('%Y-%m-%d-%H-%M-%S')
	print('----------------------------time----------------------------')
	print(time)
	os.mkdir(os.path.join(root, 'data', time))
	os.mkdir(os.path.join(root, 'data', time, 'lidar'))
	os.mkdir(os.path.join(root, 'data', time, 'cam0'))
	os.mkdir(os.path.join(root, 'data', time, 'cam1'))
	os.mkdir(os.path.join(root, 'data', time, 'cam2'))

	commands = []
	commands.append('roslaunch rslidar_sdk start.launch')
	commands.append('sleep 5 && roslaunch usb_cam usb_cam-test.launch')
	commands.append('sleep 10 && python2 topics.py ' + time)
	threads = []
	for cmd in commands:
		th = threading.Thread(target=run_command, args=(cmd,))
		th.start()
		threads.append(th)
		
finally:
	print('closing main2.py...')
	print('done.')
