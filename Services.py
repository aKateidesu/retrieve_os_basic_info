import platform
import winreg

class OsType:
    Unknown = 0
    Linux = 1
    MacOS = 2
    Windows = 3


def analyze_platform() -> int:
    """
    判断是什么系统(Linux, MacOS, Windows)
    :return: OsType
    """
    if platform.system() == 'Linux':
        return OsType.Linux
    elif platform.system() == 'Darwin':  # TODO
        return OsType.MacOS
    elif platform.system() == 'Windows':
        return OsType.Windows
    else:
        return OsType.Unknown


class InfoCollector:
    Current_platform = OsType.Unknown

    def __init__(self):
        self.os_name, self.display_ver, self.os_build_ver = self.retrieve_os_info()
        self.os_installed_apps = self.retrieve_installed_apps()

    def retrieve_os_info(self) -> tuple:
        return "", "", ""

    def retrieve_installed_apps(self) -> list:
        return []


class WindowsInfoCollector(InfoCollector):

    OS_VER_KEY = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
    OS_INSTALLED_APPS_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    def __init__(self):
        # TODO
        self.CurrentPlatform = OsType.Windows
        super().__init__()

    def retrieve_os_info(self) -> tuple:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.OS_VER_KEY, winreg.KEY_READ) as key:
                product_name, _ = winreg.QueryValueEx(key, "ProductName")
                current_build_number, _ = winreg.QueryValueEx(key, "CurrentBuildNumber")
                if "Windows 10" in product_name:
                    if int(current_build_number) >= 22000:
                        # build版本号大于等于22000时为windows11
                        product_name.replace("Windows 10", "Windows 11")
                display_version, _ = winreg.QueryValueEx(key, "DisplayVersion")
            return product_name, display_version, current_build_number
        except:
            print("打开注册表失败,无法获取Windows版本信息")
            exit(1)

    def retrieve_installed_apps(self) -> list:
        """
        返回已安装的应用列表(约等于控制面板已安装程序排除系统组件后的结果)
        :return:
        """
        reg_key_list = [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]
        software_list = []
        try:
            for reg_key in reg_key_list:
                with winreg.OpenKey(reg_key, self.OS_INSTALLED_APPS_KEY, winreg.KEY_READ) as key:
                    index = 0
                    while True:
                            try:
                                sub_key_name = winreg.EnumKey(key, index)
                            except OSError:
                                break
                            with winreg.OpenKey(key, sub_key_name) as subkey:
                                # 判断是否为系统组件
                                try:
                                    system_component, _ = winreg.QueryValueEx(subkey, "SystemComponent")
                                except FileNotFoundError:
                                    system_component = "0"
                                if int(system_component) == 1:
                                    # 不记录组件
                                    index += 1
                                    continue
                                # 名称
                                try:
                                    display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                                except FileNotFoundError:
                                    # 没有名称的软件直接跳过
                                    # display_name = sub_key_name  # 将子健名称作为软件名
                                    index += 1
                                    continue

                                # 版本号
                                try:
                                    display_version, _ = winreg.QueryValueEx(subkey, "DisplayVersion")
                                except FileNotFoundError:
                                    display_version = ""

                                # 发行者/公司
                                try:
                                    publisher, _ = winreg.QueryValueEx(subkey, "Publisher")
                                except FileNotFoundError:
                                    publisher = ""
                                software_list.append((display_name, display_version, publisher))

                            index += 1

        except FileNotFoundError:
            print("打开注册表失败,无法获取对应软件信息")
            exit(1)

        return software_list


class LinuxInfoCollector(InfoCollector):
    # TODO

    def __init__(self):
        self.CurrentPlatform = OsType.Linux
        super().__init__()


class MacOSInfoCollector(InfoCollector):
    # TODO

    def __init__(self):
        self.CurrentPlatform = OsType.MacOS
        super().__init__()


class InfoGenerator:
    def __init__(self):
        self.current_platform = analyze_platform()

    def generate_collector(self) -> InfoCollector:
        if self.current_platform == OsType.Windows:
            # Windows
            return WindowsInfoCollector()
        elif self.current_platform == OsType.Linux:
            # Linux
            return LinuxInfoCollector()
        elif self.current_platform == OsType.MacOS:
            # MacOS
            return MacOSInfoCollector()
        else:
            # Unknown
            return InfoCollector()
