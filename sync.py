import glob
import logging
import os

import rclone

cfg_path = "./rclone.conf"
from_drives = [
    "dummygd",
]
to_drives = [
    "box",
]

cfg = open(cfg_path).read()
rc = rclone.with_config(cfg)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)s [%(levelname)s]: %(message)s")

flags = ["-vP"]
if os.path.isdir("accounts"):
    sa_files = glob.glob("accounts/*.json")
    assert len(sa_files)
    flags.append("--drive-service-account-file-path")
    flags.append("accounts")

to_drive = to_drives[0]
for from_drive in from_drives:
    print(f"From: {from_drive}:")
    print(f"To: {to_drive}:sync")
    result = rc.sync(
        f"{from_drive}:",
        f"{to_drive}:sync",
        flags,
    )
    if "error" in result["error"].decode("utf-8").lower():
        exit(1)

from_drive = to_drives[0]
for to_drive in to_drives[1:]:
    print(f"From: {from_drive}:sync/")
    print(f"To: {to_drive}:sync/")
    result = rc.sync(
        f"{from_drive}:sync/",
        f"{to_drive}:sync/",
        flags,
    )
    if "error" in result["error"].decode("utf-8").lower():
        exit(1)
