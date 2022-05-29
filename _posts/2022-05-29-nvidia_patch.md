---
title: Nvidia Patch
date: '2022-05-29 00:25:06'
categories: [theserver]
tags: [docker, gpu]
image:
    path: https://www.xda-developers.com/files/2020/05/NVIDIA-GeForce-NOW-1024x683.jpg
    width: 800
    height: 500
---

> Instructions on how to bypass the transcoding limit on Nvidia graphics cards using nvidia-patch
{: .prompt-info}

![](https://www.xda-developers.com/files/2020/05/NVIDIA-GeForce-NOW-1024x683.jpg)

# Install Latest NVIDIA Driver

Download and install the latest nvidia driver from the table on that one github page

```bash
sudo apt update
sudo apt install --no-install-recommends nvidia-cuda-toolkit nvidia-headless-XXX nvidia-utils-XXX libnvidia-encode-XXX
sudo reboot
# Test
nvidia-smi
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