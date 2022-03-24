import filecmp


def compareFile(filea, fileb):
    if not filecmp.cmp(filea, fileb):  # 若文件有不同，则依次比较每一行内容
        readfilea = open(filea, 'r')
        readfileb = open(fileb, 'r')
        while True:
            linefilea = readfilea.readline().strip()  # 一行一行的读取并比较
            linefileb = readfileb.readline().strip()
            if linefilea and linefileb:
                if linefilea != linefileb:
                    print('有不同! 前者内容为：', linefilea, '后者内容为：', linefileb)
            else:
                break
        readfilea.close()
        readfileb.close()
    else:
        print('服务返回字段都相同')


compareFile(r'/Users/vog/Desktop/Temp/data/NYTJ/raw_test.json', r'/Users/vog/Desktop/Temp/data/NYTN/nyt_test.json')
