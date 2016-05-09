# -*- coding: utf-8 -*-

import os, time, subprocess, platform

if platform.system() == 'Windows':
    seek = 'findstr'
else:
    seek = 'grep'

def getWindowName(seek):
    # 获取windowName;
    getWindow = os.popen('adb shell dumpsys window | ' + seek + ' mCurrentFocus').readline().split()[-1]
    windowName = getWindow[:-1]
    print windowName
    return windowName


def getSurfaceFlinger(runCount):
    windowName = getWindowName(seek)
    retries = 0
    FPS_List = []
    for i in range(int(runCount)):
        os.system('adb shell dumpsys SurfaceFlinger --latency-clear')
        time.sleep(0.3)
        # surfaceFlinger命令,获取运行结果;
        surfaceFlinger_timeList = []
        surfaceFlinger_all = os.popen('adb shell dumpsys SurfaceFlinger --latency ' + windowName).readlines()
        for surface_line in surfaceFlinger_all[1:-1]:
            # 过滤空值, 获取第二列的值;
            if len(surface_line) > 10:
                surfaceFlinger_timeList.append(surface_line.split()[1])
        #print surfaceFlinger_timeList
        # 判断surfaceFlinger_timeList的列表长度,如果小于4则重新获取（列表长度小于4不足以提供后续计算）,重试10次;
        if len(surfaceFlinger_timeList) < 4:
            retries += 1
            if retries < 20:
                continue
            else:
                print windowName + '不能获取surface flinger latency的数据.'
                break
        # 计算单帧耗时,第二列数据后一数据与前一数据的差;
        framesTimeList = []
        for i in range(len(surfaceFlinger_timeList)):
            if i != len(surfaceFlinger_timeList) - 1:
                timing = int(surfaceFlinger_timeList[i+1]) - int(surfaceFlinger_timeList[i])
                # 纳秒换算毫秒;
                framesTime = round(timing / 1000000.00, 2)
                # 容错,偶尔出现超大值,导致计算结果异常;
                if framesTime < 3000:
                    print framesTime
                    framesTimeList.append(framesTime)
        #print framesTimeList
        FPS = round(1000 / (sum(framesTimeList) / len(framesTimeList)), 2)
        FPS_List.append(FPS)
        avg_1st = round(sum(framesTimeList) / len(framesTimeList), 2)
        max_1st = max(framesTimeList)

        # 通过比例计算FPS
        jank_count = 0
        vsync_overtime = 0
        frame_count = len(framesTimeList)
        for render_time in framesTimeList:
                if render_time > 16.67:
                    jank_count += 1
                    if render_time % 16.67 == 0 :
                        vsync_overtime += int(render_time / 16.67) - 1
                    else:
                        vsync_overtime += int(render_time / 16.67)

        fps = int(frame_count * 60 / (frame_count + vsync_overtime))

        print '平均每帧耗时算法的FPS值: ' + str(FPS), '平均每帧耗时:' + str(avg_1st)
        print '比例计算的FPS值: ' + str(fps)

    if len(FPS_List) > 0:
        avgFPS = str(round(sum(FPS_List) / len(FPS_List), 2))
        #print FPS_List
        print '平均FPS值: ' + avgFPS
        return avgFPS
    else:
        print '设备内无操作脚本或其他未知错误.'
    # # 这是用来计算两次FPS值间落差的方法,暂时不用,封印;
    # print FPS_List.index(min(FPS_List))

def main(runCount=20000):
    # 两个参数,第一个滑动类型,第二个操作次数（默认50次）;
    avgFPS = getSurfaceFlinger(runCount)
    print 'FPS测试完毕.'
    return avgFPS

if __name__ == '__main__':
    main()


