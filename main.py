from Services import InfoGenerator

if __name__ == '__main__':
    sys_info = InfoGenerator().generate_collector()
    print(f"{sys_info.os_name} {sys_info.os_display_ver} {sys_info.os_build_ver}")
    print(sys_info.os_installed_apps)
