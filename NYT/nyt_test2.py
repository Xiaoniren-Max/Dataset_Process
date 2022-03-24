import json

fi = open("/Users/vog/DataSets/TEST/nyt_test.json", encoding='utf-8')
fo = open("/Users/vog/DataSets/TEST/nyt_test_output.json", 'w', encoding='utf-8')

test_dict = {'tokens': 'none', 'entities': [], 'relations': [], 'orig_id': -1}
temp_id = 0
temp_entities = list()


def match_entity(tokens, entity):
    entity_idx = list()
    idx = 0
    for item in tokens:
        if item == entity[0]:
            entity_idx.append(idx)
        idx += 1
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
    e = dic['entityMentions']
    for item in e:
        entity_dict = {'type': item['label'], 'start': -1, 'end': -1}
        temp_entity = {'text': item['text']}
        m = item['text'].split(" ")
        entity_dict['start'] = match_entity(words, m)
        entity_dict['end'] = entity_dict['start'] + 1
        for c in item['text']:
            if c == ' ':
                entity_dict['end'] += 1
        if entity_dict not in test_dict['entities']:
            test_dict['entities'].append(entity_dict)
        if temp_entity not in temp_entities:
            temp_entities.append(temp_entity)

    # get relations
    r = dic['relationMentions']  # list
    for item in r:
        relation_dict = {'type': item['label'], 'head': -1, 'tail': -1}
        for entity_item in temp_entities:
            if "\\" in item['em1Text']:
                idx_u = item['em1Text'].index("\\")
                es1 = item['em1Text'][0:idx_u]
                es2 = item['em1Text'][idx_u+6:]
                if es1 in entity_item['text'] and es2 in entity_item['text']:
                    relation_dict['head'] = temp_entities.index(entity_item)
            if "\\" in item['em2Text']:
                idx_u = item['em2Text'].index("\\")
                es1 = item['em2Text'][0:idx_u]
                es2 = item['em2Text'][idx_u+6:]
                if es1 in entity_item['text'] and es2 in entity_item['text']:
                    relation_dict['tail'] = temp_entities.index(entity_item)
            if entity_item['text'] == item['em1Text']:
                relation_dict['head'] = temp_entities.index(entity_item)
            elif entity_item['text'] == item['em2Text']:
                relation_dict['tail'] = temp_entities.index(entity_item)
        if relation_dict not in test_dict['relations']:
            test_dict['relations'].append(relation_dict)

    # set id
    test_dict['orig_id'] = temp_id
    temp_id += 1

    json_obj = json.dumps(test_dict)
    fo.writelines(json_obj + '\n')

    test_dict['entities'].clear()
    test_dict['relations'].clear()
    temp_entities.clear()

fi.close()
fo.close()