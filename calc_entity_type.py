import json

fi_1 = open("/Users/vog/DataSets/SemEval/Data/TEST_FILE_FULL_output.json", encoding='utf-8')
fi_2 = open("/Users/vog/DataSets/SemEval/Data/TRAIN_FILE_output.json", encoding='utf-8')
# fi_3 = open("/Users/vog/DataSets/SemEval/Data/TEST_FILE_FULL_output.json", encoding='utf-8')
fo = open("/Users/vog/DataSets/SemEval/Data/entity_types.json", 'w', encoding='utf-8')

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