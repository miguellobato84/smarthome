#!/bin/bash
ACTION=$1
DEVBASE=$2
DEVICE="/dev/${DEVBASE}"
LOG_FILE="/home/miguel/Videos/rsync.log"
MOUNT_PATH="/media/PROYECTOR"

echo "$(date): Script invoked with ACTION=${ACTION}, DEVBASE=${DEVBASE}" > ${LOG_FILE}

MOUNT_POINT=$(/bin/mount | /bin/grep ${DEVICE} | /usr/bin/awk '{ print $3 }')  # Check if this drive is already mounted
echo "$(date): Found mount point: ${MOUNT_POINT}" >> ${LOG_FILE}

case "${ACTION}" in
    add)
        if [[ -n ${MOUNT_POINT} ]]; then
            echo "$(date): Device ${DEVICE} already mounted at ${MOUNT_POINT}, exiting." >> ${LOG_FILE}
            exit 1
        fi
        echo "$(date): Gathering device info for ${DEVICE}." >> ${LOG_FILE}
        eval $(/sbin/blkid -o udev ${DEVICE})  # Get info for this drive

        # Determine unique mount point based on label, UUID, or device name
        if [[ -n ${ID_FS_LABEL} ]]; then
            MOUNT_DIR="/media/${ID_FS_LABEL}"
        elif [[ -n ${ID_FS_UUID} ]]; then
            MOUNT_DIR="/media/${ID_FS_UUID}"
        else
            MOUNT_DIR="/media/${DEVBASE}"
        fi

        echo "$(date): Mount point determined as ${MOUNT_DIR}" >> ${LOG_FILE}

        # Create the mount directory if it doesn't exist
        if [[ ! -d ${MOUNT_DIR} ]]; then
            mkdir -p ${MOUNT_DIR}
            echo "$(date): Created directory ${MOUNT_DIR}" >> ${LOG_FILE}
        fi

        OPTS="rw,relatime"
        if [[ ${ID_FS_TYPE} == "vfat" ]]; then
            OPTS+=",users,gid=100,umask=000,shortname=mixed,utf8=1,flush"
            echo "$(date): Detected vfat file system. Using options: ${OPTS}" >> ${LOG_FILE}
        fi

        MOUNT_CMD="/bin/mount -o ${OPTS} ${DEVICE} ${MOUNT_DIR}"
        echo "$(date): Executing mount command: ${MOUNT_CMD}" >> ${LOG_FILE}

        if ! eval ${MOUNT_CMD}; then
            echo "$(date): Failed to mount ${DEVICE} to ${MOUNT_DIR}." >> ${LOG_FILE}
            exit 1
        fi

        echo "$(date): Successfully mounted ${DEVICE} to ${MOUNT_DIR}." >> ${LOG_FILE}
        ;;
    remove)
        if [[ -n ${MOUNT_POINT} ]]; then
            echo "$(date): Unmounting device ${DEVICE} from ${MOUNT_POINT}." >> ${LOG_FILE}
            /bin/umount -l ${DEVICE}
            echo "$(date): Successfully unmounted ${DEVICE}." >> ${LOG_FILE}

            # Optionally remove the mount directory
            if [[ -d ${MOUNT_POINT} ]]; then
                rmdir ${MOUNT_POINT}
                echo "$(date): Removed directory ${MOUNT_POINT}" >> ${LOG_FILE}
            fi
        else
            echo "$(date): No mount point found for device ${DEVICE}, nothing to do." >> ${LOG_FILE}
        fi
        ;;
    *)
        echo "$(date): Unknown action: ${ACTION}. Exiting." >> ${LOG_FILE}
        exit 1
        ;;
esac

# Check if the MOUNT_PATH is mounted
if /bin/mount | /bin/grep -q "${MOUNT_PATH}"; then
    echo "$(date): ${MOUNT_PATH} is mounted. Starting rsync." >> ${LOG_FILE}
    echo "$(date): Starting rsync" >> ${LOG_FILE}
    rsync --verbose --recursive --stats --human-readable --ignore-existing --delete \
        /home/miguel/Videos/tvshows/ ${MOUNT_PATH}/tvshows/ >> ${LOG_FILE}
    rsync --verbose --recursive --stats --human-readable --ignore-existing \
        /home/miguel/Videos/movies/ ${MOUNT_PATH}/movies/ >> ${LOG_FILE}
    echo "$(date): Rsync completed." >> ${LOG_FILE}

    # Get disk usage details
    DISK_USAGE=$(df -BG ${MOUNT_PATH} | /usr/bin/tail -n 1 | /usr/bin/awk '{print $2, $4}')
    TOTAL_SPACE=$(echo ${DISK_USAGE} | /usr/bin/awk '{print $1}')
    FREE_SPACE=$(echo ${DISK_USAGE} | /usr/bin/awk '{print $2}')
    echo "$(date): ${MOUNT_PATH} total space: ${TOTAL_SPACE}, free space: ${FREE_SPACE}" >> ${LOG_FILE}

    # Flush and unmount the MOUNT_PATH
    echo "$(date): Flushing file system buffers for ${MOUNT_PATH}." >> ${LOG_FILE}
    /bin/sync
    echo "$(date): Unmounting ${MOUNT_PATH}." >> ${LOG_FILE}
    /bin/umount ${MOUNT_PATH}
    echo "$(date): Successfully unmounted ${MOUNT_PATH}." >> ${LOG_FILE}
fi
