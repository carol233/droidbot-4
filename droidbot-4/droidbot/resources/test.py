import os
def diff(a,b):
    return list(set(b).difference(set(a)))

def clear_cache():
    standard = ['Alarms', 'Android', 'DCIM', 'Download', 'Movies', 'Music', 'Notifications', 'Pictures', 'Podcasts', 'Ringtones', '_AdContent', 'storage']
    os.system("adb -s 192.168.97.101:5555 root")
    os.system("adb -s 192.168.97.101:5555 shell mkdir /sdcard/_AdContent")
    str = os.popen("adb -s 192.168.97.101:5555 shell cd /sdcard;ls").read()
    dirlist = str.split('\r\n')
    diffs = diff(standard, dirlist)
    for dir in diffs:
        if dir:
            # print dir
            os.system("adb -s 192.168.97.101:5555 shell rm -rf /sdcard/" + dir)
clear_cache()