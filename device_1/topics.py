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

root = '/home/hit-meiyu/code/device_1'
count = 0

if len(sys.argv)==1:
    print('Error: parameter lost! ')
    sys.exit()
elif len(sys.argv)>2:
    print('Error: too many parameters! ')
    sys.exit()
time = sys.argv[1]

def multi_callback(Subcriber_cam3, Subcriber_cam4, Subcriber_imu):
    bridge = cv_bridge.CvBridge()
    cam3_data = bridge.imgmsg_to_cv2(Subcriber_cam3, 'bgr8')
    cam4_data = bridge.imgmsg_to_cv2(Subcriber_cam4, 'bgr8')
    stamp = Subcriber_imu.header.stamp.secs*1000 + Subcriber_imu.header.stamp.nsecs//1000000
    path = os.path.join(root, 'data', time)
    save_cams(cam3_data, cam4_data, path, stamp)
    save_imu(Subcriber_imu, path, stamp)
    global count
    print("[cams] Frame %d saved!" % count)
    count += 1
    cv2.waitKey(1)

def cam5_callback(Subcriber_cam):
    bridge = cv_bridge.CvBridge()
    cam_data = bridge.imgmsg_to_cv2(Subcriber_cam, 'bgr8')
    stamp = Subcriber_cam.header.stamp.secs*1000 + Subcriber_cam.header.stamp.nsecs//1000000
    path = os.path.join(root, 'data', time, 'cam5')
    save_cam(cam_data, path, stamp)
    cv2.waitKey(1)

def gps_callback(Subcriber_gps):
    stamp = Subcriber_gps.header.stamp.secs*1000 + Subcriber_gps.header.stamp.nsecs//1000000
    path = os.path.join(root, 'data', time)
    save_gps(Subcriber_gps, path, stamp)
    cv2.waitKey(1)

def save_cams(cam3_data, cam4_data, path, stamp):
    path3 = os.path.join(path, 'cam3', str(stamp) + '.png')
    path4 = os.path.join(path, 'cam4', str(stamp) + '.png')
    cv2.imwrite(path3, cam3_data)
    cv2.imwrite(path4, cam4_data)

def save_gps(gps_data, path, stamp):
    path_gps = os.path.join(path, 'gps', str(stamp) + '.txt')
    with open(path_gps, 'w+') as file:
        latitude = str(gps_data.latitude)
        file.write(latitude + '\n')
        longitude = str(gps_data.longitude)
        file.write(longitude + '\n')
        altitude = str(gps_data.altitude)
        file.write(altitude + '\n')
        pos_cov = str(gps_data.position_covariance)
        file.write(pos_cov + '\n')
        pos_cov_type = str(gps_data.position_covariance_type)
        file.write(pos_cov_type + '\n')

def save_imu(imu_data, path, stamp):
    path_imu = os.path.join(path, 'imu', str(stamp) + '.txt')
    with open(path_imu, 'w+') as file:
        orientation = str([imu_data.orientation.x, imu_data.orientation.y, imu_data.orientation.z, imu_data.orientation.w])
        file.write(orientation + '\n')
        ort_cov = str(imu_data.orientation_covariance)
        file.write(ort_cov + '\n')
        ang_vel = str([imu_data.angular_velocity.x, imu_data.angular_velocity.y, imu_data.angular_velocity.z])
        file.write(ang_vel + '\n')
        ang_cov = str(imu_data.angular_velocity_covariance)
        file.write(ang_cov + '\n')
        linear_accel = str([imu_data.linear_acceleration.x, imu_data.linear_acceleration.y, imu_data.linear_acceleration.z])
        file.write(linear_accel + '\n')
        linear_cov = str(imu_data.linear_acceleration_covariance)
        file.write(linear_cov + '\n')

def save_cam(cam_data, path, stamp):
    path = os.path.join(path, str(stamp) + '.png')
    cv2.imwrite(path, cam_data)

if __name__ == '__main__':
    rospy.init_node('two_TOPIC', anonymous=True)#初始化节点
    print('initiation done!')
    
    rospy.Subscriber('/usb_cam5/image_raw', Image, cam5_callback)
    subcriber_cam3 = message_filters.Subscriber('/usb_cam3/image_raw', Image)
    subcriber_cam4 = message_filters.Subscriber('/usb_cam4/image_raw', Image)
    print('usb_cam opened!')

    subcriber_imu = message_filters.Subscriber('/imu/data', Imu)
    print('imu opened!')
    
    sync = message_filters.ApproximateTimeSynchronizer([subcriber_cam3, subcriber_cam4, subcriber_imu], 10, 0.08)#同步时间戳，具体参数含义需要查看官方文档。
    print('synchronization done!')
    sync.registerCallback(multi_callback)#执行反馈函数

    rospy.Subscriber('/fix', NavSatFix, gps_callback)
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("over!")
        cv2.destroyAllWindows()

