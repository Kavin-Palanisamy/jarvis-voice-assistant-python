"""
system_control.py
Manages Windows OS interactions: volume, brightness, power, and app launching.
"""

import os
import wmi
import psutil
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import subprocess
from logger import get_logger

logger = get_logger()

class SystemControl:
    def __init__(self):
        self.wmi_client = wmi.WMI()
        logger.info("System control initialized.")

    def launch_app(self, app_name: str) -> bool:
        """Very basic application launcher via Windows start shell command."""
        logger.info(f"Attempting to launch application: {app_name}")
        try:
            # os.system blocks rarely in this context since start spawns immediately
            os.system(f'start {app_name}')
            return True
        except Exception as e:
            logger.error(f"Failed to launch app '{app_name}': {e}")
            return False

    def set_volume(self, level: int):
        """Sets Windows master volume (0-100)."""
        logger.info(f"Setting volume to {level}%")
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            scalar_vol = max(0.0, min(1.0, level / 100.0))
            volume.SetMasterVolumeLevelScalar(scalar_vol, None)
        except Exception as e:
            logger.error(f"Failed to set volume: {e}")

    def set_brightness(self, level: int):
        """Sets screen brightness (0-100)."""
        logger.info(f"Setting brightness to {level}%")
        try:
            sbc.set_brightness(level)
        except Exception as e:
            logger.error(f"Failed to set brightness: {e}")

    def get_system_stats(self) -> dict:
        """Returns CPU, RAM, and Disk utilization."""
        stats = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "ram_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        }
        return stats

if __name__ == "__main__":
    sys_ctrl = SystemControl()
    print("System Stats:", sys_ctrl.get_system_stats())
