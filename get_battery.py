import os
import shutil

from openpyxl import Workbook


def get_log():
    """
    拷贝手机录制的log(debuglogger)
    :return:
    """
    log_path = "data/debuglogger"
    if os.path.exists(log_path):
        shutil.rmtree(log_path)
    os.system("adb devices")
    os.system(f"adb pull /sdcard/debuglogger {log_path}/")


def get_path():
    """
    获取data目录下的kernel log 文件的路径
    """
    # get_log()
    log_root = r"data/debuglogger/mobilelog"
    lists = []
    temp = os.listdir(log_root)
    for t in temp:
        l_p = log_root + "/" + t
        if os.path.isdir(l_p):
            tp = os.listdir(l_p)
            for i in range(len(tp)):
                tp[i] = l_p + "/" + tp[i]
                lists.append(tp[i])
    lls = []
    for i in lists:
        if i.rfind("kernel") != -1:
            lls.append(i)
    return lls


def get_battery_log(data_list: list):
    """
    将所有的kernel log 合并并复制到temp/log文件中
    """
    log_path = "temp/log"
    exists_delete(log_path)
    num = len(data_list)
    for i in range(num):
        file = open(data_list[i], "r+", encoding="utf-8")
        log = open(log_path, "a+", encoding="utf-8")
        print("数据提取中")
        for line in file:
            log.writelines(line)
        log.close()
        file.close()


def format_time_log():
    """
    1.格式化kernel log 的时间戳
    2.将kernel log中的电量log（日期、时间、电量）保存至temp/data_kernel中

    """
    convert_log_path = "temp/log.localtime"
    date_kernel_log_path = "temp/data_kernel.txt"
    exists_delete(convert_log_path)
    exists_delete(date_kernel_log_path)
    os.system("call run_convert.bat")
    file = open(convert_log_path, "r+", encoding="utf-8")
    date_kernel_log = open(date_kernel_log_path, "a+", encoding="utf-8")
    date_kernel_log.writelines("day hour_minute battery_level\n")
    for line in file:
        if "healthd: battery l" in line:
            line = line.split(" ")[::-1]
            day = line[-1]
            hour_minute = line[-2][:5]
            battery_level = line[7][2:4]
            date_kernel_log.writelines(f"{day} {hour_minute} {battery_level}")
    date_kernel_log.close()
    file.close()


def excel_date():
    """
    将data_kernel.txt文件中的数据保存至表格（battery.xls）中
    """
    exists_delete("battery.xls")
    file_path = "temp/data_kernel.txt"
    if os.path.exists(file_path):
        file = open(file_path, "r+", encoding="utf-8")
        workbook = Workbook()
        worksheet = workbook.active
        i = 0
        for line in file:
            line = line.split(" ")
            day_row = f"A{i + 1}"
            hour_minute_row = f"B{i + 1}"
            battery_level_row = f"C{i + 1}"
            worksheet[day_row] = line[0]
            worksheet[hour_minute_row] = line[1]
            worksheet[battery_level_row] = line[2]
            i += 1
        workbook.save("battery.xls")
        print("已将电量信息汇总并去重到battery.xls表格中啦")
        os.system("battery.xls")


def exists_delete(path: str):
    if os.path.exists(path):
        os.remove(path)


if __name__ == '__main__':
    kernels = get_path()
    get_battery_log(kernels)
    format_time_log()
    excel_date()
