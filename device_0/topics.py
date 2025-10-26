#!/usr/bin/env python2
# coding=UTF-8
'''
此程序为测试测试程序， 用以测试message_filters同时
订阅两个topic，可以同时进行数据处理。
'''
import rospy, math, random, cv_bridge, cv2, os, sys
import numpy as np
import message_filters
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image, CameraInfo, NavSatFix, PointCloud2, TimeReference, Imu
from sensor_msgs import point_cloud2

root = '/home/hit-meiyu/code/device_0'
count = 0
cam0_count = 0
cam1_count = 0
cam2_count = 0
lidar_count = 0

if len(sys.argv)==1:
    print('Error: parameter lost! ')
    sys.exit()
elif len(sys.argv)>2:
    print('Error: too many parameters! ')
    sys.exit()
time = sys.argv[1]

def multi_callback(Subcriber_cam0, Subcriber_cam1, Subcriber_cam2, Subcriber_lidar):
    bridge = cv_bridge.CvBridge()
    cam0_data = bridge.imgmsg_to_cv2(Subcriber_cam0, 'bgr8')#常规操作
    cam1_data = bridge.imgmsg_to_cv2(Subcriber_cam1, 'bgr8')
    cam2_data = bridge.imgmsg_to_cv2(Subcriber_cam2, 'bgr8')

    global count
    print("[cams] Frame %d saved!" % count)
    count += 1

    stamp = Subcriber_lidar.header.stamp.secs*1000 + Subcriber_lidar.header.stamp.nsecs//1000000
    path = os.path.join(root, 'data', time)

    save_cams(cam0_data, cam1_data, cam2_data, path, stamp)
    save_lidar(Subcriber_lidar, path, stamp)
    cv2.waitKey(1)

def lidar_callback(Subcriber_lidar):
    path = os.path.join(root, 'data', time)
    stamp = Subcriber_lidar.header.stamp.secs*1000 + Subcriber_lidar.header.stamp.nsecs//1000000
    save_lidar(Subcriber_lidar, path, stamp)
    global lidar_count
    lidar_count += 1
    cv2.waitKey(1)

def cam0_callback(Subcriber_cam):
    bridge = cv_bridge.CvBridge()
    cam_data = bridge.imgmsg_to_cv2(Subcriber_cam, 'bgr8')
    stamp = Subcriber_cam.header.stamp.secs*1000 + Subcriber_cam.header.stamp.nsecs//1000000
    path = os.path.join(root, 'data', time, 'cam0')
    save_cam(cam_data, path, stamp)
    global cam0_count
    print("[cam_0] Frame %d saved!" % cam0_count)
    cam0_count += 1
    cv2.waitKey(1)

def cam1_callback(Subcriber_cam):
    bridge = cv_bridge.CvBridge()
    cam_data = bridge.imgmsg_to_cv2(Subcriber_cam, 'bgr8')
    stamp = Subcriber_cam.header.stamp.secs*1000 + Subcriber_cam.header.stamp.nsecs//1000000
    path = os.path.join(root, 'data', time, 'cam1')
    save_cam(cam_data, path, stamp)
    global cam1_count
    print("[cam_1] Frame %d saved!" % cam1_count)
    cam1_count += 1
    cv2.waitKey(1)

def cam2_callback(Subcriber_cam):
    bridge = cv_bridge.CvBridge()
    cam_data = bridge.imgmsg_to_cv2(Subcriber_cam, 'bgr8')
    stamp = Subcriber_cam.header.stamp.secs*1000 + Subcriber_cam.header.stamp.nsecs//1000000
    path = os.path.join(root, 'data', time, 'cam2')
    save_cam(cam_data, path, stamp)
    global cam2_count
    print("[cam_2] Frame %d saved!" % cam2_count)
    cam2_count += 1
    cv2.waitKey(1)

def save_lidar(lidar_data, path, stamp):
    points_pc2 = point_cloud2.read_points(lidar_data, skip_nans=True)
    points_np = np.asarray(list(points_pc2), dtype=np.float32)
    path_lidar = os.path.join(path, 'lidar', str(stamp) + '.bin')
    points_np.tofile(path_lidar)

def save_cams(cam0_data, cam1_data, cam2_data, path, stamp):
    path0 = os.path.join(path, 'cam0', str(stamp) + '.png')
    path1 = os.path.join(path, 'cam1', str(stamp) + '.png')
    path2 = os.path.join(path, 'cam2', str(stamp) + '.png')
    cv2.imwrite(path0, cam0_data)
    cv2.imwrite(path1, cam1_data)
    cv2.imwrite(path2, cam2_data)

def save_cam(cam_data, path, stamp):
    path = os.path.join(path, str(stamp) + '.png')
    cv2.imwrite(path, cam_data)

if __name__ == '__main__':
    rospy.init_node('two_TOPIC', anonymous=True)#初始化节点

    print('initiation done!')
    
    subcriber_cam0 = message_filters.Subscriber('/usb_cam0/image_raw', Image)#订阅第一个话题，rgb图像
    subcriber_cam1 = message_filters.Subscriber('/usb_cam1/image_raw', Image)#订阅第二个话题，rgb图像
    subcriber_cam2 = message_filters.Subscriber('/usb_cam2/image_raw', Image)
    print('usb_cam opened!')

    subcriber_lidar = message_filters.Subscriber('/rslidar_points', PointCloud2)
    print('lidar opened!')

    sync = message_filters.ApproximateTimeSynchronizer([subcriber_cam0, subcriber_cam1, subcriber_cam2, subcriber_lidar], 10, 0.08)#同步时间戳，具体参数含义需要查看官方文档。
    print('synchronization done!')
    sync.registerCallback(multi_callback)#执行反馈函数
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("over!")
        cv2.destroyAllWindows()

