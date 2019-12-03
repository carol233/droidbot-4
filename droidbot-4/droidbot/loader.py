#######
#author : tmliu
#date: 2018.05.30
#######

import os
from droidbot import DroidBot


def diff(a, b):
    return list(set(b).difference(set(a)))


def clear_cache(device_serial):
    standard = ['Alarms', 'Android', 'DCIM', 'Download', 'Movies', 'Music', 'Notifications', 'Pictures', 'Podcasts',
                'Ringtones', '_AdContent', 'storage']
    str = os.popen("adb -s "+ device_serial + " shell cd /sdcard;ls").read()
    dirlist = str.split('\r\n')
    diffs = diff(standard, dirlist)
    for dir in diffs:
        if dir:
            # print dir
            os.system("adb -s " + device_serial + " shell rm -rf /sdcard/" + dir)


def getFileList(rootDir, pickstr):
    """
    :param rootDir:  root directory of dataset
    :return: A filepath list of sample
    """
    filePath = []
    for parent, dirnames, filenames in os.walk(rootDir):
        for filename in filenames:
            if pickstr in filename:
                file = os.path.join(parent, filename)
                filePath.append(file)

    return filePath

def main():
    """
    the main function
    it starts a droidbot according to the arguments given in cmd line
    """
    bppath = root_path + 'breakpoint.txt'
    if not os.path.exists(bppath):
        os.system("adb -s " +device_serial + " shell mkdir /sdcard/_AdContent")
        with open(bppath,"a+") as f:
            print("break point is set")
    with open(bppath, "r+") as f:
        apk_done = f.read()

    apknames = getFileList(app_path, ".apk")
    for apk in apknames:
        apkname = os.path.split(apk)[-1][:-4]
        if apkname not in apk_done:
            with open(ip_pkg, "r+") as fpkg:
                lines = fpkg.readlines()
            with open(ip_pkg, "w+") as fpkg:
                for line in lines:
                    if device_ip not in line:
                        fpkg.write(line.strip('\n')+'\n')
                fpkg.write(device_ip + ":" + apkname+'\n')
            try:
                print(apkname)
                droidbot = DroidBot(app_path=apk,
                                    device_serial=device_serial,
                                    is_emulator=False,
                                    output_dir=os.path.join(output_dir, apkname),
                                    env_policy=None,
                                    policy_name="dfs_greedy",
                                    random_input=False,
                                    script_path=None,
                                    event_count=8,
                                    event_interval=6,
                                    timeout=None,
                                    keep_app=False,
                                    keep_env=True,
                                    cv_mode=False,
                                    debug_mode=False,
                                    profiling_method=None,
                                    grant_perm=False)
                clear_cache(device_serial)
                droidbot.start()
                with open(bppath, "a+") as f:
                    f.write(apkname+'\n')
            except:
                # droidbot.stop()
                with open(bppath, "a+") as f:
                    f.write(apkname+'\n')
                print(apkname + " can not use! Continue!")
                import traceback
                traceback.print_exc()
    return


if __name__ == "__main__":
    cfg = os.path.abspath(os.path.dirname(os.getcwd())) + '/cfg.txt'
    if os.path.exists(cfg):
        with open(cfg, "r+") as f:
            lines = f.readlines()
            for line in lines:
                if 'root_path' in line:
                    root_path = line.strip('\n').split('=')[-1]
                    continue
                if 'app_path' in line:
                    app_path = line.strip('\n').split('=')[-1]
                    continue
                if 'device_serial' in line:
                    device_serial = line.strip('\n').split('=')[-1]
                    continue
                if 'device_ip' in line:
                    device_ip = line.strip('\n').split('=')[-1]
                    continue
                if 'output_dir' in line:
                    output_dir = line.strip('\n').split('=')[-1]
                    continue
                if 'ip_pkg' in line:
                    ip_pkg = line.strip('\n').split('=')[-1]
                    continue
        # os.system("adb connect "+device_serial)
        # os.system('adb -s '+device_serial + " root")
        main()