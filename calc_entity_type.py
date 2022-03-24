import json

fi_1 = open("/your_file_1.jsonn", encoding='utf-8')
fi_2 = open("/your_file_2.json", encoding='utf-8')
# fi_3 = open("/your_file_3.json", encoding='utf-8')
fo = open("/your_file.json", 'w', encoding='utf-8')

type_list = list()

for line in fi_1.readlines():
    dic = json.loads(line)

    r = dic['entities']
    for item in r:
        if item['type'] not in type_list:
            type_list.append(item['type'])
            fo.writelines(item['type']+'\n')

for line in fi_2.readlines():
    dic = json.loads(line)

    r = dic['entities']
    for item in r:
        if item['type'] not in type_list:
            type_list.append(item['type'])
            fo.writelines(item['type']+'\n')

# for line in fi_3.readlines():
#     dic = json.loads(line)
#
#     r = dic['entities']
#     for item in r:
#         if item['type'] not in type_list:
#             type_list.append(item['type'])
#             fo.writelines(item['type']+'\n')