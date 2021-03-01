import os
import platform
import shutil


class VirtualPCInterface:
    """
        Defines all the methods that must be implemented to control the PC.
        It includes actions such as "volume up", "shutdown" that are not the same in all operating systems.
    """

    def volume_up(self):
        """Increase the volume in N. Where N is constant"""
        raise NotImplementedError("Volume Up not implemented")

    def volume_down(self):
        """Decrease the volume in N. Where N is constant"""
        raise NotImplementedError("Volume down not implemented")

    def volume_mute(self):
        """Silence the system"""
        raise NotImplementedError("Mute not implemented")

    def multimedia_play_pause(self):
        """Play or pause current playback"""
        raise NotImplementedError("Play/Pause not implemented")

    def multimedia_next(self):
        """Switch to the next track in the current playback"""
        raise NotImplementedError("Next not implemented")

    def multimedia_prev(self):
        """Switch to the previous track in the current playback"""
        raise NotImplementedError("Previous not implemented")

    def lock(self):
        """Locks the PC to prevent current user from using it"""
        raise NotImplementedError("Lock not implemented")

    def unlock(self):
        """Unlocks the PC, see VirtualPCInterface.pc_lock()"""
        raise NotImplementedError("Unlock not implemented")

    def shutdown(self):
        """Shutdown the PC"""
        raise NotImplementedError("Shutdown not implemented")

    def sleep(self):
        """Sleep the PC"""
        raise NotImplementedError("Sleep not implemented")

    def check_dependencies(self) -> bool:
        """
        check if the system has all dependencies installed. As amixer, systemctl, among others
        :return true if everything is fine, otherwise false
        :rtype bool
        """
        raise NotImplementedError("Sleep not implemented")


class LinuxVirtualPCImplement(VirtualPCInterface):
    def volume_up(self):
        os.system("amixer set 'Master' 10%+")

    def volume_down(self):
        os.system("amixer set 'Master' 10%-")

    def volume_mute(self):
        os.system("amixer set 'Master' 0%")

    def multimedia_play_pause(self):
        os.system("xdotool key XF86AudioPlay")

    def multimedia_next(self):
        os.system("xdotool key XF86AudioNext")

    def multimedia_prev(self):
        os.system("xdotool key XF86AudioPrev")

    def shutdown(self):
        os.system("systemctl poweroff")

    def sleep(self):
        os.system("systemctl suspend")

    def check_dependencies(self) -> bool:
        return shutil.which("amixer") is not None and\
               shutil.which("xdotool") is not None and\
               shutil.which("systemctl") is not None


class WindowsVirtualPCImplement(VirtualPCInterface):
    pass


def get_virtual_pc_instance():
    os = platform.system()
    if os == 'Linux':
        return LinuxVirtualPCImplement()
    elif os == 'Windows':
        return WindowsVirtualPCImplement()
    else:
        return None
