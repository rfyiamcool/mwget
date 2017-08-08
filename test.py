#coding:utf-8
import sys

from mwget.multiwget import FileMwget

#163镜像的速度比较给力
file_url = "http://mirrors.163.com/centos/7/isos/x86_64/CentOS-7-x86_64-NetInstall-1611.iso"


def test():
    if sys.argv[1:]:
        mfile = sys.argv[1]
    else:
        print 'give me url'
        sys.exit()

    down = FileMwget(mfile, process_num=10, debug=True)
    down.run()
    print down.get_report()


if __name__ == "__main__":
    test()
