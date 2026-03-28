"""
Day 5.5 — Disk Management, Partitioning, LVM & Mounting Practice
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import SessionLocal
import models

db = SessionLocal()

module = models.Module(
    title="Day 5.5 - Disk Partitioning, Filesystem & Mounting Practice",
    description="Hands-on practice with disk partitioning, creating filesystems, temporary/permanent mounting, LVM, swap, and disk quota. Uses the 10GB volume (/dev/sdb) attached to your server.",
    sort_order=11,
    unlock_percent=0,
    is_published=False,
    time_limit=120,
)
db.add(module)
db.commit()
db.refresh(module)

questions = [
    # ── Partitioning & Filesystem ──────────────────────────────────────

    {
        "type": "practical",
        "text": "TASK 1 - Check Your Disks\n\nList all block devices on your server using lsblk.\nYou should see /dev/sdb (10GB) — this is your practice disk.\n\nSave the output of lsblk to /home/trainee/disk_info.txt",
        "verify_command": "test -f /home/trainee/disk_info.txt && grep -q 'sdb' /home/trainee/disk_info.txt && echo 'disk_checked'",
        "verify_expected": "disk_checked",
        "verify_type": "contains",
        "points": 1.0,
        "order": 1,
    },
    {
        "type": "practical",
        "text": "TASK 2 - Create Two Partitions\n\nUsing fdisk, create two partitions on /dev/sdb:\n- /dev/sdb1 — 5GB\n- /dev/sdb2 — 5GB (remaining space)\n\nBoth should be Linux type (83).\n\nSteps:\n1. sudo fdisk /dev/sdb\n2. n (new) → p (primary) → 1 → Enter → +5G\n3. n (new) → p (primary) → 2 → Enter → Enter (use remaining)\n4. w (write and quit)",
        "verify_command": "lsblk /dev/sdb 2>/dev/null | grep -c 'sdb[12]'",
        "verify_expected": "2",
        "verify_type": "contains",
        "points": 3.0,
        "order": 2,
    },
    {
        "type": "practical",
        "text": "TASK 3 - Create ext4 Filesystem\n\nCreate an ext4 filesystem on /dev/sdb1.\n\nUse: sudo mkfs.ext4 /dev/sdb1",
        "verify_command": "blkid /dev/sdb1 2>/dev/null | grep -q 'ext4' && echo 'ext4_ok'",
        "verify_expected": "ext4_ok",
        "verify_type": "contains",
        "points": 2.0,
        "order": 3,
    },
    {
        "type": "practical",
        "text": "TASK 4 - Create XFS Filesystem\n\nCreate an XFS filesystem on /dev/sdb2.\n\nIf xfsprogs is not installed, install it first:\nsudo apt install xfsprogs -y\n\nThen: sudo mkfs.xfs /dev/sdb2",
        "verify_command": "blkid /dev/sdb2 2>/dev/null | grep -q 'xfs' && echo 'xfs_ok'",
        "verify_expected": "xfs_ok",
        "verify_type": "contains",
        "points": 2.0,
        "order": 4,
    },
    {
        "type": "practical",
        "text": "TASK 5 - Temporary Mount (ext4)\n\nCreate a mount point /mnt/data1 and temporarily mount /dev/sdb1 on it.\n\nSteps:\n1. sudo mkdir -p /mnt/data1\n2. sudo mount /dev/sdb1 /mnt/data1\n3. Verify with: df -h /mnt/data1",
        "verify_command": "mountpoint -q /mnt/data1 && df -T /mnt/data1 | grep -q 'ext4' && echo 'mounted_ext4'",
        "verify_expected": "mounted_ext4",
        "verify_type": "contains",
        "points": 2.0,
        "order": 5,
    },
    {
        "type": "practical",
        "text": "TASK 6 - Temporary Mount (XFS)\n\nCreate a mount point /mnt/data2 and temporarily mount /dev/sdb2 on it.\n\nSteps:\n1. sudo mkdir -p /mnt/data2\n2. sudo mount /dev/sdb2 /mnt/data2\n3. Verify with: df -h /mnt/data2",
        "verify_command": "mountpoint -q /mnt/data2 && df -T /mnt/data2 | grep -q 'xfs' && echo 'mounted_xfs'",
        "verify_expected": "mounted_xfs",
        "verify_type": "contains",
        "points": 2.0,
        "order": 6,
    },
    {
        "type": "practical",
        "text": "TASK 7 - Write Data to Mounted Filesystems\n\nCreate a test file on each mounted partition:\n- /mnt/data1/test_ext4.txt containing 'ext4 filesystem working'\n- /mnt/data2/test_xfs.txt containing 'xfs filesystem working'\n\nThis proves the filesystems are usable.",
        "verify_command": "grep -q 'ext4 filesystem working' /mnt/data1/test_ext4.txt 2>/dev/null && grep -q 'xfs filesystem working' /mnt/data2/test_xfs.txt 2>/dev/null && echo 'data_written'",
        "verify_expected": "data_written",
        "verify_type": "contains",
        "points": 2.0,
        "order": 7,
    },
    {
        "type": "practical",
        "text": "TASK 8 - Find UUIDs\n\nFind the UUID of both partitions using blkid and save the output to /home/trainee/uuid_list.txt\n\nYou will need these UUIDs for permanent mounting.",
        "verify_command": "test -f /home/trainee/uuid_list.txt && grep -q 'sdb1' /home/trainee/uuid_list.txt && grep -q 'sdb2' /home/trainee/uuid_list.txt && echo 'uuid_saved'",
        "verify_expected": "uuid_saved",
        "verify_type": "contains",
        "points": 2.0,
        "order": 8,
    },
    {
        "type": "practical",
        "text": "TASK 9 - Permanent Mount via /etc/fstab\n\nAdd both partitions to /etc/fstab for permanent mounting (survives reboot).\n\nAdd these lines to /etc/fstab (use actual UUIDs from blkid):\nUUID=<sdb1-uuid>  /mnt/data1  ext4  defaults  0  2\nUUID=<sdb2-uuid>  /mnt/data2  xfs   defaults  0  0\n\nAfter editing, run: sudo mount -a\nIf no errors, your fstab is correct.",
        "verify_command": "grep -q '/mnt/data1' /etc/fstab && grep -q '/mnt/data2' /etc/fstab && mount -a 2>&1 | wc -l | grep -q '0' && echo 'fstab_ok'",
        "verify_expected": "fstab_ok",
        "verify_type": "contains",
        "points": 3.0,
        "order": 9,
    },
    {
        "type": "practical",
        "text": "TASK 10 - Unmount and Remount\n\nUnmount both partitions:\nsudo umount /mnt/data1\nsudo umount /mnt/data2\n\nThen remount using fstab:\nsudo mount -a\n\nVerify both are mounted again and your test files still exist.",
        "verify_command": "mountpoint -q /mnt/data1 && mountpoint -q /mnt/data2 && test -f /mnt/data1/test_ext4.txt && test -f /mnt/data2/test_xfs.txt && echo 'remount_ok'",
        "verify_expected": "remount_ok",
        "verify_type": "contains",
        "points": 2.0,
        "order": 10,
    },

    # ── LVM ────────────────────────────────────────────────────────────

    {
        "type": "practical",
        "text": "TASK 11 - Create a Swap File\n\nCreate a 512MB swap file and enable it.\n\nSteps:\n1. sudo fallocate -l 512M /swapfile\n2. sudo chmod 600 /swapfile\n3. sudo mkswap /swapfile\n4. sudo swapon /swapfile\n5. Verify with: swapon --show",
        "verify_command": "swapon --show 2>/dev/null | grep -q '/swapfile' && echo 'swap_active'",
        "verify_expected": "swap_active",
        "verify_type": "contains",
        "points": 2.0,
        "order": 11,
    },
    {
        "type": "practical",
        "text": "TASK 12 - Make Swap Permanent\n\nAdd the swap file to /etc/fstab so it activates on every boot.\n\nAdd this line to /etc/fstab:\n/swapfile  none  swap  sw  0  0\n\nVerify with: grep swap /etc/fstab",
        "verify_command": "grep -q '/swapfile' /etc/fstab && grep -q 'swap' /etc/fstab && echo 'swap_permanent'",
        "verify_expected": "swap_permanent",
        "verify_type": "contains",
        "points": 2.0,
        "order": 12,
    },
    {
        "type": "practical",
        "text": "TASK 13 - Check Disk Usage\n\nUse the du command to find the top 5 largest directories under / and save the output to /home/trainee/largest_dirs.txt\n\nUse: sudo du -h --max-depth=1 / 2>/dev/null | sort -rh | head -5",
        "verify_command": "test -f /home/trainee/largest_dirs.txt && test -s /home/trainee/largest_dirs.txt && echo 'du_saved'",
        "verify_expected": "du_saved",
        "verify_type": "contains",
        "points": 2.0,
        "order": 13,
    },
    {
        "type": "practical",
        "text": "TASK 14 - Check Filesystem Health\n\nUnmount /mnt/data1 and run a filesystem check on /dev/sdb1.\n\nSteps:\n1. sudo umount /mnt/data1\n2. sudo fsck /dev/sdb1\n3. Remount: sudo mount -a\n\nSave the fsck output to /home/trainee/fsck_output.txt",
        "verify_command": "test -f /home/trainee/fsck_output.txt && test -s /home/trainee/fsck_output.txt && mountpoint -q /mnt/data1 && echo 'fsck_done'",
        "verify_expected": "fsck_done",
        "verify_type": "contains",
        "points": 2.0,
        "order": 14,
    },
    {
        "type": "practical",
        "text": "TASK 15 - Check Inode Usage\n\nCheck inode usage on all mounted filesystems and save to /home/trainee/inode_usage.txt\n\nUse: df -i",
        "verify_command": "test -f /home/trainee/inode_usage.txt && grep -q 'IFree' /home/trainee/inode_usage.txt && echo 'inode_saved'",
        "verify_expected": "inode_saved",
        "verify_type": "contains",
        "points": 1.0,
        "order": 15,
    },

    # ── Theory ─────────────────────────────────────────────────────────

    {
        "type": "short_answer",
        "text": "What is the difference between MBR and GPT partition tables? When would you use each?",
        "correct_answer": "MBR (Master Boot Record): Supports up to 4 primary partitions (or 3 primary + 1 extended with logical partitions), max disk size 2TB, stores partition table at the start of the disk, single point of failure. GPT (GUID Partition Table): Supports up to 128 partitions, no 2TB limit (supports up to 9.4 ZB), stores backup partition table at end of disk, uses CRC32 checksums for integrity. Use MBR for legacy BIOS systems or disks under 2TB. Use GPT for UEFI systems or disks over 2TB.",
        "points": 2.0,
        "order": 16,
    },
    {
        "type": "short_answer",
        "text": "What is the difference between ext4 and XFS filesystems? When would you choose one over the other?",
        "correct_answer": "ext4: Default on most Linux distros, supports up to 1EB volume and 16TB file size, supports shrinking and growing, has journal for crash recovery, good for general use and smaller filesystems. XFS: High-performance journaling filesystem, supports up to 8EB, excellent for large files and parallel I/O, cannot be shrunk (only grown), good for large-scale storage and databases. Choose ext4 for general-purpose servers and when you might need to shrink the filesystem. Choose XFS for high-performance workloads with large files.",
        "points": 2.0,
        "order": 17,
    },
    {
        "type": "short_answer",
        "text": "What is /etc/fstab? Explain each field in an fstab entry. What happens if there is a wrong entry in fstab?",
        "correct_answer": "fstab (filesystem table) is a config file that defines how disk partitions are mounted at boot. Fields: 1) Device (UUID or /dev/sdX) 2) Mount point (directory) 3) Filesystem type (ext4, xfs, swap) 4) Mount options (defaults, ro, noexec, etc.) 5) Dump (0 or 1, for backup utility) 6) Pass (fsck order: 0=skip, 1=root first, 2=others). If there's a wrong entry, the system may fail to boot or drop to emergency mode. Always test with 'mount -a' before rebooting.",
        "points": 3.0,
        "order": 18,
    },
    {
        "type": "short_answer",
        "text": "What is the difference between temporary and permanent mounting? Why is UUID preferred over device names like /dev/sdb1?",
        "correct_answer": "Temporary mounting: Using the mount command directly - the mount is lost after reboot. Permanent mounting: Adding entry to /etc/fstab - the mount persists across reboots. UUID is preferred because device names (/dev/sdb1) can change if disks are added/removed or detected in different order. UUID is a unique identifier tied to the filesystem itself and never changes, making it reliable for fstab entries.",
        "points": 2.0,
        "order": 19,
    },
    {
        "type": "short_answer",
        "text": "What is LVM (Logical Volume Management)? Explain Physical Volume (PV), Volume Group (VG), and Logical Volume (LV). What are the advantages of using LVM?",
        "correct_answer": "LVM is a storage management framework that adds abstraction between physical disks and filesystems. PV (Physical Volume): The actual partition or disk initialized for LVM (pvcreate). VG (Volume Group): A pool of storage combining one or more PVs (vgcreate). LV (Logical Volume): A virtual partition carved from a VG, on which you create a filesystem (lvcreate). Advantages: Resize volumes without unmounting, span across multiple disks, create snapshots for backups, easy to add more storage by extending the VG, thin provisioning.",
        "points": 3.0,
        "order": 20,
    },

    # ── MCQ ─────────────────────────────────────────────────────────────

    {
        "type": "mcq",
        "text": "Which command is used to create an ext4 filesystem on a partition?",
        "options": ["fdisk /dev/sdb1", "mkfs.ext4 /dev/sdb1", "format ext4 /dev/sdb1", "fsck.ext4 /dev/sdb1"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 21,
    },
    {
        "type": "mcq",
        "text": "What does the 'mount -a' command do?",
        "options": [
            "Unmounts all filesystems",
            "Mounts all filesystems listed in /etc/fstab that are not already mounted",
            "Shows all currently mounted filesystems",
            "Mounts all available USB devices"
        ],
        "correct_answer": "1",
        "points": 1.0,
        "order": 22,
    },
    {
        "type": "mcq",
        "text": "Which command shows the UUID of all block devices?",
        "options": ["lsblk --uuid", "blkid", "uuid-list", "fdisk -l --uuid"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 23,
    },
    {
        "type": "mcq",
        "text": "What is the correct permission for a swap file?",
        "options": ["644", "755", "600", "777"],
        "correct_answer": "2",
        "points": 1.0,
        "order": 24,
    },
    {
        "type": "mcq",
        "text": "Which filesystem type CANNOT be shrunk, only grown?",
        "options": ["ext4", "ext3", "XFS", "btrfs"],
        "correct_answer": "2",
        "points": 1.0,
        "order": 25,
    },
]

for q_data in questions:
    q = models.Question(module_id=module.id, **q_data)
    db.add(q)

db.commit()
print(f"Created module '{module.title}' (ID: {module.id}) with {len(questions)} questions")
print(f"  - 15 Practical tasks")
print(f"  - 5 Theory questions")
print(f"  - 5 MCQ questions")
print(f"Module is DRAFT - publish from admin panel when ready")
db.close()
