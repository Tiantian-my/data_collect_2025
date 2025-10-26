chrony installation:
    sudo apt update
    sudo apt install chrony
    sudo systemctl enable chrony
    sudo systemctl start chrony

edit chrony.conf
    sudo gedit /etc/chrony/chrony.conf

    (write...)
    # 使用可靠的 NTP 服务器（中国用户推荐）
    server <host-ip> iburst

    # 基本配置
    driftfile /var/lib/chrony/drift
    makestep 0.005 3
    rtcsync
    keyfile /etc/chrony/chrony.keys
    logdir /var/log/chrony
    maxupdateskew 100.0
