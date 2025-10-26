import os
import threading
import datetime

root = '/home/hit-meiyu/code/device_1'
passwd = 'MY870322'
net_device = 'enp8s0'

def env_init():
	rs = []
	rs.append(os.system('cd ' + root))
	command2 = 'chmod 777 /dev/ttyUSB1'
	command3 = 'chmod 777 /dev/ttyUSB0'
	command4 = 'systemctl enable chrony'
	command5 = 'systemctl start chrony'
	rs.append(os.system('echo %s | sudo -S %s' % (passwd, command2)))
	rs.append(os.system('echo %s | sudo -S %s' % (passwd, command3)))
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
	os.mkdir(os.path.join(root, 'data', time, 'cam3'))
	os.mkdir(os.path.join(root, 'data', time, 'cam4'))
	os.mkdir(os.path.join(root, 'data', time, 'cam5'))
	os.mkdir(os.path.join(root, 'data', time, 'gps'))
	os.mkdir(os.path.join(root, 'data', time, 'imu'))
	commands = []
	commands.append('roslaunch usb_cam usb_cam-test.launch')
	commands.append('sleep 5 && roslaunch nmea_navsat_driver nmea_serial_driver.launch')
	commands.append('sleep 10 && roslaunch wit_ros_imu rviz_and_imu.launch')
	commands.append('sleep 15 && python2 topics.py ' + time)
	commands.append('python sync.py')
	threads = []
	for cmd in commands:
		th = threading.Thread(target=run_command, args=(cmd,))
		th.start()
		threads.append(th)	
finally:
	print('closing main2.py...')
	print('done.')
