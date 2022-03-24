import json

fi = open("/your_file.json", encoding='utf-8')
fo = open("/your_file.json", 'w', encoding='utf-8')

test_dict = {'tokens': 'none', 'entities': [], 'relations': [], 'orig_id': -1}
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
    test_dict['tokens'] = words

    # get entities
    r = dic['relationMentions']
    for item in r:
        entity_dict_1 = {'text': item['em1Text'], 'start': -1, 'end': -1}
        entity_dict_2 = {'text': item['em2Text'], 'start': -1, 'end': -1}
        m1 = item['em1Text'].split(" ")
        m2 = item['em2Text'].split(" ")
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

    # sort entities
    temp_dict['entities'] = sorted(temp_dict['entities'], key=lambda i: i['start'])

    # get relations
    r = dic['relationMentions']  # list
    for item in r:
        relation_dict = {'type': item['label'], 'head': -1, 'tail': -1}
        for entity_item in temp_dict['entities']:
            if entity_item['text'] == item['em1Text']:
                relation_dict['head'] = temp_dict['entities'].index(entity_item)
            if entity_item['text'] == item['em2Text']:
                relation_dict['tail'] = temp_dict['entities'].index(entity_item)
        if relation_dict not in test_dict['relations']:
            test_dict['relations'].append(relation_dict)

    # set entities
    for item in temp_dict['entities']:
        entity_final = {'type': 'none', 'start': item['start'], 'end': item['end']}
        test_dict['entities'].append(entity_final)

    # set id
    test_dict['orig_id'] = temp_id
    temp_id += 1

    json_obj = json.dumps(test_dict)
    fo.writelines(json_obj+'\n')

    temp_dict['entities'].clear()
    test_dict['entities'].clear()
    test_dict['relations'].clear()

fi.close()
fo.close()