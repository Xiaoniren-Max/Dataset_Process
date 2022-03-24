import json
from nltk import word_tokenize

fi = open("/Users/vog/DataSets/TEST/webnlg_test.json", encoding='utf-8')
fo = open("/Users/vog/DataSets/TEST/webnlg_test_output.json", 'w', encoding='utf-8')

test_dict = {'tokens': 'null', 'entities': [], 'relations': [], 'id': -1}
temp_dict = {'entities': []}
temp_id = 0


def match_entity(tokens, entity):
    entity_idx = list()
    idx = 0
    for item in tokens:
        if item == entity[0]:
            entity_idx.append(idx)
        idx += 1
    # print(entity_idx)
    for i in entity_idx:
        tmp_i = i
        flag = True
        for item in entity:
            if item != tokens[tmp_i]:
                flag = False
                break
            tmp_i += 1
        if not flag:
            continue
        else:
            return i


for line in fi.readlines():
    dic = json.loads(line)

    # get tokens
    t = dic['sentText']
    words = t.split(" ")
    # print(words)
    # words = word_tokenize(str(t))
    test_dict['tokens'] = words

    # get entities
    r = dic['relationMentions']
    for item in r:
        entity_dict_1 = {'text': item['em1Text'], 'start': -1, 'end': -1}
        entity_dict_2 = {'text': item['em2Text'], 'start': -1, 'end': -1}
        m1 = item['em1Text'].split(" ")
        m2 = item['em2Text'].split(" ")
        # print(m)
        entity_dict_1['start'] = match_entity(words, m1)
        entity_dict_2['start'] = match_entity(words, m2)
        entity_dict_1['end'] = entity_dict_1['start'] + 1
        entity_dict_2['end'] = entity_dict_2['start'] + 1
        for c in item['em1Text']:
            if c == ' ':
                entity_dict_1['end'] += 1
        for c in item['em2Text']:
            if c == ' ':
                entity_dict_2['end'] += 1
        if entity_dict_1 not in temp_dict['entities']:
            temp_dict['entities'].append(entity_dict_1)
        if entity_dict_2 not in temp_dict['entities']:
            temp_dict['entities'].append(entity_dict_2)

    # get relations
    r = dic['relationMentions']  # list
    for item in r:
        relation_dict = {'type': item['label'], 'head': -1, 'tail': -1}
        for entity_item in test_dict['entities']:
            if entity_item['text'] == item['em1Text']:
                relation_dict['head'] = test_dict['entities'].index(entity_item)
            elif entity_item['text'] == item['em2Text']:
                relation_dict['tail'] = test_dict['entities'].index(entity_item)
        test_dict['relations'].append(relation_dict)

    # set entities
    for item in temp_dict['entities']:
        entity_final = {'type': 'null', 'start': item['start'], 'end': item['end']}
        test_dict['entities'].append(entity_final)

    # sort entities
    test_dict['entities'] = sorted(test_dict['entities'], key = lambda i: i['start'])


    # # get relations
    # r = dic['relationMentions']  # list
    # for item in r:
    #     relation_dict = {'type': item['label'], 'head': -1, 'tail': -1}
    #     # print(item['em2Text'])
    #     for entity_item in e:
    #         if entity_item['text'] == item['em1Text']:
    #             relation_dict['head'] = e.index(entity_item)
    #         elif entity_item['text'] == item['em2Text']:
    #             relation_dict['tail'] = e.index(entity_item)
    #     test_dict['relations'].append(relation_dict)

    # set id
    test_dict['id'] = temp_id
    temp_id += 1

    json_obj = json.dumps(test_dict)
    fo.writelines(json_obj+'\n')

    temp_dict['entities'].clear()
    test_dict['entities'].clear()
    test_dict['relations'].clear()

fi.close()
fo.close()