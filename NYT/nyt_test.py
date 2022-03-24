import json
from nltk import word_tokenize

fi = open("/Users/vog/DataSets/TEST/nyt_test.json", encoding='utf-8')
fo = open("/Users/vog/DataSets/TEST/nyt_test_output.json", 'w', encoding='utf-8')

test_dict = {'tokens': 'null', 'entities': [], 'relations': [], 'id': -1}
temp_id = 0
test_list = list()


def matchEntity(tokens, entity):
    entityIdx = list()
    idx = 0
    for item in tokens:
        if item == entity[0]:
            entityIdx.append(idx)
        idx += 1
    # print(entityIdx)
    for i in entityIdx:
        tmpi = i
        flag = True
        for item in entity:
            if item != tokens[tmpi]:
                flag = False
                break
            tmpi += 1
        if flag == False:
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
    e = dic['entityMentions']
    for item in e:
        entity_dict = {'type': item['label'], 'start': -1, 'end': -1}
        m = item['text'].split(" ")
        # print(m)
        entity_dict['start'] = matchEntity(words, m)
        entity_dict['end'] = entity_dict['start'] + 1
        for c in item['text']:
            if c == ' ':
                entity_dict['end'] += 1
        test_dict['entities'].append(entity_dict)

    # get relations
    r = dic['relationMentions']  # list
    for item in r:
        relation_dict = {'type': item['label'], 'head': -1, 'tail': -1}
        # print(item['em2Text'])
        for entity_item in e:
            if "\\" in item['em1Text']:
                idx_u = item['em1Text'].index("\\")
                es1 = item['em1Text'][0:idx_u]
                es2 = item['em1Text'][idx_u+1:]
                # print(es1)
                # print(es2)
                if es1 in entity_item['text'] and es2 in entity_item['text']:
                    # if len(es1) != 0 and len(es2) != 0 and entity_item['text'].index(es1)+len(es1) == entity_item['text'].index(es2)-1:
                        relation_dict['head'] = e.index(entity_item)
                    # elif len(es1) == 0 or len(es2) == 0:
                    #     relation_dict['head'] = e.index(entity_item)
            # print(type(item['em2Text']))
            if "\\" in item['em2Text']:
                idx_u = item['em2Text'].index("\\")
                es1 = item['em2Text'][0:idx_u]
                es2 = item['em2Text'][idx_u+1:]
                # print(es1)
                # print(es1[-1])
                # print(es2)
                if es1 in entity_item['text'] and es2 in entity_item['text']:
                    # print('yes')
                    # if len(es1) != 0 and len(es2) != 0 and entity_item['text'].index(es1)+len(es1) == entity_item['text'].index(es2)-1:
                        relation_dict['tail'] = e.index(entity_item)
                    # elif len(es1) == 0 or len(es2) == 0:
                    #     relation_dict['tail'] = e.index(entity_item)
            if entity_item['text'] == item['em1Text']:
                relation_dict['head'] = e.index(entity_item)
            elif entity_item['text'] == item['em2Text']:
                relation_dict['tail'] = e.index(entity_item)
        test_dict['relations'].append(relation_dict)

    # set id
    test_dict['id'] = temp_id
    temp_id += 1

    test_list.append(test_dict)

    test_dict['entities'].clear()
    test_dict['relations'].clear()

json_obj = json.dumps(test_list)
fo.writelines(json_obj)

fi.close()
fo.close()