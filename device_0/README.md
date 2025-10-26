chrony installation:
    sudo apt update
    sudo apt install chrony
    sudo systemctl enable chrony
    sudo systemctl start chrony

edit chrony.conf
    sudo gedit /etc/chrony/chrony.conf

    (write...)
    # 使用可靠的 NTP 服务器（中国用户推荐）
    server ntp.aliyun.com iburst
    server ntp1.aliyun.com iburst
    server cn.pool.ntp.org iburst
    server time.apple.com iburst

    # 基本配置
    driftfile /var/lib/chrony/drift
    makestep 1.0 3
    rtcsync
    keyfile /etc/chrony/chrony.keys
    logdir /var/log/chrony
    maxupdateskew 100.0

    # 允许局域网设备访问
    allow 192.168.31.0/24
    # 使用本地时钟作为备用（如果断网）
    local stratum 10
