import os
import xlwings as xw


def get_path():
    """
    获取data目录下的kernel log 的路径
    """
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
    将kernel log 复制到log/log文件中
    """
    log_path = "temp/log"
    if os.path.exists(log_path):
        os.remove(log_path)
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
    convert_log_path = "temp/log.localtime"
    convert_battery_log_path = "temp/convert_kernel_log.txt"
    if os.path.exists(convert_log_path):
        os.remove(convert_log_path)
    if os.path.exists(convert_battery_log_path):
        os.remove(convert_battery_log_path)
    os.system("call run_convert.bat")
    file = open(convert_log_path, "r+", encoding="utf-8")
    convert_battery_log = open(convert_battery_log_path, "a+", encoding="utf-8")
    for line in file:
        if "healthd: battery l" in line:
            convert_battery_log.writelines(line)
    convert_battery_log.close()
    file.close()


def kernel_battery_data_extract(convert_kernel_log_path: str):
    if os.path.exists(convert_kernel_log_path):
        kernel_log = open(convert_kernel_log_path, "r+", encoding="utf-8")

        date_kernel = open("temp/date_kernel.txt", "w+", encoding="utf-8")
        date_kernel.writelines("day hour_minute battery_level\n")
        flag = ""
        for k in kernel_log:
            res = k[k.rfind("<"):k.rfind("]") + 1]
            k = k.replace(res, "")
            line = k.split(" ")
            day = line[0]
            hour_minute = line[1][:5]
            battery_level = line[4][2:4]
            if flag != hour_minute:
                flag = hour_minute
                line_c = f"{day} {hour_minute} {battery_level}\n"
                print(line_c)
                date_kernel.writelines(line_c)
        date_kernel.close()
        kernel_log.close()
    else:
        print(f"{convert_kernel_log_path}文件不存在，请确认")


def excel_date():
    pass


if __name__ == '__main__':
    # kernels = get_path()
    # get_battery_log(kernels)
    # format_time_log()
    # kernel_battery_data_extract("temp/convert_kernel_log.txt")
    excel_date()