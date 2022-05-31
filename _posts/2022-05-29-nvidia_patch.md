---
title: Nvidia Patch
date: '2022-05-29 00:25:06'
categories: [theserver]
tags: [docker, gpu]
image:
    src: /assets/img/nvidia-header.jpg
    width: 800
    height: 500
---

> Instructions on how to bypass the transcoding limit on Nvidia graphics cards using nvidia-patch
{: .prompt-info}

# Install Latest NVIDIA Driver

Download and install the latest nvidia driver from the table on that one github page

```bash
VER=XXX
sudo apt update
sudo apt install --no-install-recommends nvidia-cuda-toolkit nvidia-headless-${VER} nvidia-utils-${VER} libnvidia-encode-${VER}
sudo reboot
```

After a reboot, test with `nvidia-smi`
```bash
$ nvidia-smi
Mon May 30 20:52:01 2022
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 510.73.05    Driver Version: 510.73.05    CUDA Version: 11.6     |
|-------------------------------+----------------------+----------------------+
...
...
```

<!-- ## Old Install Instructions
    
    ## Download
    
    ```bash
    cd /opt/nvidia
    curl <link> -o nvidia.run
    ```
    
    ## Install
    
    Make sure you
    
    ```bash
    sudo chmod +x ./nvidia.run
    sudo ./nvidia.run
    ```
     -->

## Whoops I did an oopsie

To start over and uninstall everything nvidia, follow these steps.

<!-- ### Installed With Run File

If you installed the drivers with the .run file from nvidias website, uninstall with this

```bash
sudo ./NVIDIA-Linux-x86_64-510.47.03.run --uninstall
``` -->

### Installed With apt

If installed with apt, this command should uninstall everything nvidia

```bash
sudo apt purge '*nvidia*'
```

# Set Up NVIDIA Docker Runtime

```bash
sudo apt install -y nvidia-docker2
sudo systemctl restart docker
```

If the repo isn't set up, follow the steps here.

[Installation Guide - NVIDIA Cloud Native Technologies documentation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#setting-up-nvidia-container-toolkit)

# Run the NVIDIA Driver Patch

## Clone Repo

```bash
sudo git clone https://github.com/keylase/nvidia-patch nvidia-patch
```

## Patch

```bash
cd ./nvidia-patch
sudo bash ./patch.sh
```