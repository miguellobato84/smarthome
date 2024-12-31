# iningUSB Mount Automation Guide

This README provides instructions for automating USB drive mounting on a headless Linux system. The solution is based on a modified version of an excellent guide by Andrea Fortuna, as outlined in @FelixJN's comment on [this Unix Stack Exchange thread](https://unix.stackexchange.com/questions/681379/usb-flash-drives-automatically-mounted-headless-computer).

## Overview

This script and associated configuration files automate the process of mounting and unmounting USB drives to the `/media/` directory using udev rules and systemd services.

### Prerequisites

- Root access to the system
- Basic knowledge of shell scripting and Linux system administration

## Setup Steps

### 1. Create the USB Mount Script

- Create a file at `/root/usb-mount.sh`.
- Copy the provided script content into this file.
- Grant execute permissions using:
  ```bash
  chmod +x /root/usb-mount.sh
  ```

### 2. Create the Systemd Service File

- Create a file at `/etc/systemd/system/usb-mount@.service`.
- Add the provided service configuration to this file.

### 3. Create Udev Rules

- Create a file at `/etc/udev/rules.d/99-local.rules`.
- Insert the provided udev rules into this file.

### 4. Apply Changes

- Reload udev rules:
  ```bash
  udevadm control --reload-rules
  ```
- Reload systemd daemon:
  ```bash
  systemctl daemon-reload
  ```

### 5. Test the Setup

- Insert a USB flash drive.
- Verify that the drive is mounted automatically to `/media/`.
- If successful, the drive should appear in the `/media/` directory.

### 6. Custom Script Block for Rsync and Disk Management

This custom block added to the `usb-mount.sh` script automates the synchronization and management of specific directories to the mounted USB drive. Once the drive is successfully mounted, it checks if the mount path is valid. If it is, the script performs the following steps:

1. **Rsync Backup**: The script uses `rsync` to back up the `tvshows` and `movies` directories from the `/home/miguel/Videos/` path to corresponding directories on the mounted USB drive. It ensures that only new or modified files are copied, ignoring existing ones, and removes files that are no longer present in the source directories.
  
2. **Disk Space Report**: It fetches and logs the total and free disk space of the mounted drive to monitor storage usage.

3. **Sync and Unmount**: After completing the rsync operations, the script flushes the file system buffers using `/bin/sync` to ensure data integrity, then unmounts the USB drive and logs the process.

This block enhances the automation by adding file synchronization and disk management, making it more efficient for backing up media files to external drives.