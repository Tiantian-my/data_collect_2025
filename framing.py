'''
采集数据组帧
input:  device_0数据, 地址为./device_0/data
        device_1数据, 地址为./device_1/data
        对齐阈值, 自定义值(s)
output: 对齐数据, 自定义地址
*这段代码还没有完成测试优化
'''
import os
import shutil

in_path_0 = './device_0/data'
in_path_1 = './device_1/data'
out_path = './aligned_data'
threshold = 0.1

valid_stamps_0 = []
valid_path_0 = os.path.join(in_path_0, 'valid')
valid_lidar_path = os.path.join(valid_path_0, 'lidar')
valid_cam0_path = os.path.join(valid_path_0, 'cam0')
valid_cam1_path = os.path.join(valid_path_0, 'cam1')
valid_cam2_path = os.path.join(valid_path_0, 'cam2')
# 创建有效帧保存路径
if not os.path.exists(valid_path_0):
    os.mkdir(valid_path_0)
    os.mkdir(valid_lidar_path)
    os.mkdir(valid_cam0_path)
    os.mkdir(valid_cam1_path)
    os.mkdir(valid_cam2_path)
# 获取device_0有效帧对应的时间戳(cam0/cam1/cam2/lidar同步)
groups_d0 = os.listdir(in_path_0)
for group in groups_d0:
    group_path = os.path.join(in_path_0, group)
    # 取LiDAR的时间戳
    lidar_path = os.path.join(group_path, 'lidar')
    lidar_files = os.listdir(lidar_path)
    if len(lidar_files) == 0:
        continue
    else:
        cam0_path = os.path.join(group_path, 'cam0')
        cam1_path = os.path.join(group_path, 'cam1')
        cam2_path = os.path.join(group_path, 'cam2')
        for lf in lidar_files:
            stamp = lf[:-4]
            valid_stamps_0.append(int(stamp))
            shutil.copy(os.path.join(lidar_path, lf), os.path.join(valid_lidar_path, lf))
            shutil.copy(os.path.join(cam0_path, stamp+'.png'), os.path.join(valid_cam0_path, stamp+'.png'))
            shutil.copy(os.path.join(cam1_path, stamp+'.png'), os.path.join(valid_cam1_path, stamp+'.png'))
            shutil.copy(os.path.join(cam2_path, stamp+'.png'), os.path.join(valid_cam2_path, stamp+'.png'))
valid_stamps_0.sort()

valid_stamps_1 = []
valid_path_1 = os.path.join(in_path_1, 'valid')
valid_imu_path = os.path.join(valid_path_1, 'imu')
valid_cam3_path = os.path.join(valid_path_1, 'cam3')
valid_cam4_path = os.path.join(valid_path_1, 'cam4')
valid_cam5_path = os.path.join(valid_path_1, 'cam5_pool')
valid_gps_path = os.path.join(valid_path_1, 'gps_pool')
# 创建有效帧保存路径
if not os.path.exists(valid_path_1):
    os.mkdir(valid_path_1)
    os.mkdir(valid_imu_path)
    os.mkdir(valid_cam3_path)
    os.mkdir(valid_cam4_path)
# 获取device_1有效帧对应的时间戳(cam3/cam4)
groups_d1 = os.listdir(in_path_1)
for group in groups_d1:
    group_path = os.path.join(in_path_1, group)
    imu_path = os.path.join(group_path, 'imu')
    imu_files = os.listdir(imu_path)
    if len(imu_files) == 0:
        continue
    else:
        cam3_path = os.path.join(group_path, 'cam3')
        cam4_path = os.path.join(group_path, 'cam4')
        cam5_path = os.path.join(group_path, 'cam5')
        gps_path = os.path.join(group_path, 'gps')
        cam5_files = os.listdir(cam5_path)
        gps_files = os.listdir(gps_path)
        for imuf in imu_files:
            stamp = imuf[:-4]
            valid_stamps_1.append(int(stamp))
            shutil.copy(os.path.join(imu_path, stamp+'.txt'), os.path.join(valid_imu_path, stamp+'.txt'))
            shutil.copy(os.path.join(cam3_path, stamp+'.png'), os.path.join(valid_cam3_path, stamp+'.png'))
            shutil.copy(os.path.join(cam4_path, stamp+'.png'), os.path.join(valid_cam4_path, stamp+'.png'))
        for c5f in cam5_files:
            shutil.copy(os.path.join(cam5_path, c5f), os.path.join(valid_cam5_path, c5f))
        for gf in gps_files:
            shutil.copy(os.path.join(gps_path, gf), os.path.join(valid_gps_path, gf))
valid_stamps_1.sort()

# 按照阈值做匹配并复制, 同时删除无法匹配的帧(同步cam0/cam1/cam2/cam3/cam4/lidar/imu)
p0 = p1 = 0
while p0 < len(valid_stamps_0) and p1 < len(valid_stamps_1):
    if valid_stamps_0[p0] - valid_stamps_1[p1] > threshold * 1000:
        p1 += 1
        os.remove(os.path.join(valid_imu_path, valid_stamps_1[p1]+'.txt'))
        os.remove(os.path.join(valid_cam3_path, valid_stamps_1[p1]+'.png'))
        os.remove(os.path.join(valid_cam4_path, valid_stamps_1[p1]+'.png'))
        continue
    elif valid_stamps_1[p1] - valid_stamps_0[p0] > threshold * 1000:
        p0 += 1
        os.remove(os.path.join(valid_lidar_path, valid_stamps_0[p0]+'.bin'))
        os.remove(os.path.join(valid_cam0_path, valid_stamps_0[p0]+'.png'))
        os.remove(os.path.join(valid_cam1_path, valid_stamps_0[p0]+'.png'))
        os.remove(os.path.join(valid_cam2_path, valid_stamps_0[p0]+'.png'))
        continue
    else:
        p0 += 1
        p1 += 1
if p0 >= len(valid_stamps_0):
    for i in range(p1, len(valid_stamps_1)):
        os.remove(os.path.join(valid_imu_path, valid_stamps_1[p1]+'.txt'))
        os.remove(os.path.join(valid_cam3_path, valid_stamps_1[i]+'.png'))
        os.remove(os.path.join(valid_cam4_path, valid_stamps_1[i]+'.png'))
elif p1 >= len(valid_stamps_1):
    for i in range(p0, len(valid_stamps_0)):
        os.remove(os.path.join(valid_lidar_path, valid_stamps_0[i]+'.bin'))
        os.remove(os.path.join(valid_cam0_path, valid_stamps_0[i]+'.png'))
        os.remove(os.path.join(valid_cam1_path, valid_stamps_0[i]+'.png'))
        os.remove(os.path.join(valid_cam2_path, valid_stamps_0[i]+'.png'))

# 继续匹配cam5和GPS(1Hz)
valid_stamps_1 = [int(imuf[:-4]) for imuf in os.listdir(valid_imu_path)]
valid_cam5_stamps = [int(c5f[:-4]) for c5f in os.listdir(valid_cam5_path)]
valid_gps_stamps = [int(gf[:-4]) for gf in os.listdir(valid_gps_path)]
matched_cam5_path = os.path.join(valid_path_1, 'cam5')
matched_gps_path = os.path.join(valid_path_1, 'gps')
p1 = p5 = 0
while p1 < len(valid_stamps_1):
    if p5 < len(valid_cam5_stamps) - 1:
        if valid_cam5_stamps[p5] < valid_stamps_1[p1]:
            if valid_cam5_stamps[p5+1] < valid_stamps_1[p1]:
                p5 += 1
            else:
                if abs(valid_cam5_stamps[p5+1] - valid_stamps_1[p1]) < abs(valid_cam5_stamps[p5] - valid_stamps_1[p1]):
                    shutil.copy(os.path.join(valid_cam5_path,valid_cam5_stamps[p5+1]+'.png'), os.path.join(matched_cam5_path,valid_stamps_1[p1]+'.png'))
                else:
                    shutil.copy(os.path.join(valid_cam5_path,valid_cam5_stamps[p5]+'.png'), os.path.join(matched_cam5_path,valid_stamps_1[p1]+'.png'))
                p1 += 1
        else:
            shutil.copy(os.path.join(valid_cam5_path,valid_cam5_stamps[p5]+'.png'), os.path.join(matched_cam5_path,valid_stamps_1[p1]+'.png'))
            p1 += 1
    else:
        shutil.copy(os.path.join(valid_cam5_path,valid_cam5_stamps[-1]+'.png'), os.path.join(matched_cam5_path,valid_stamps_1[p1]+'.png'))
        p1 += 1
p1 = pg = 0
while p1 < len(valid_stamps_1):
    if pg < len(valid_gps_stamps) - 1:
        if valid_gps_stamps[pg] < valid_stamps_1[p1]:
            if valid_gps_stamps[pg+1] < valid_stamps_1[p1]:
                pg += 1
            else:
                if abs(valid_gps_stamps[pg+1] - valid_stamps_1[p1]) < abs(valid_gps_stamps[pg] - valid_stamps_1[p1]):
                    shutil.copy(os.path.join(valid_gps_path,valid_gps_stamps[pg+1]+'.txt'), os.path.join(matched_gps_path,valid_stamps_1[p1]+'.txt'))
                else:
                    shutil.copy(os.path.join(valid_gps_path,valid_gps_stamps[pg]+'.txt'), os.path.join(matched_gps_path,valid_stamps_1[p1]+'.txt'))
                p1 += 1
        else:
            shutil.copy(os.path.join(valid_gps_path,valid_gps_stamps[pg]+'.txt'), os.path.join(matched_gps_path,valid_stamps_1[p1]+'.txt'))
            p1 += 1
    else:
        shutil.copy(os.path.join(valid_gps_path,valid_gps_stamps[-1]+'.txt'), os.path.join(matched_gps_path,valid_stamps_1[p1]+'.txt'))
        p1 += 1

# 删除多余的目录以节省空间
# shutil.rmtree(valid_cam5_path)
# shutil.rmtree(valid_gps_path)