from Services import InfoGenerator

if __name__ == '__main__':
    sys_info = InfoGenerator().generate_collector()
    print(sys_info.os_name)
    print(sys_info.os_installed_apps)
