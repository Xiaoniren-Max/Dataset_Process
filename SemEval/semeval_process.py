import json
import re

fo = open("/Users/vog/DataSets/SemEval/Data/TEST_FILE_FULL_output.json", 'w', encoding='utf-8')

test_dict = {'tokens': 'none', 'entities': [], 'relations': [], 'orig_id': -1}


def match_tag(tokens, tag):
    for item in tokens:
        if tag in item:
            return tokens.index(item)


with open("/Users/vog/DataSets/SemEval/Data/TEST_FILE_FULL.TXT") as file:
    lines = file.readlines()
    for l in lines:

        # process the 1st line:
        #     get tokens
        #     get entities
        if "1" <= l[0] <= "9":

            # get tokens (include <e1>)
            strs = l.split("\t")
            sentText = strs[1][1:-2]
            temp_tokens = re.findall(r"[\w]+|[.,!?:;\"'()]|<e1>.*</e1>|<e2>.*</e2>", sentText)
            tokens = list()
            for item in temp_tokens:
                items = item.split(" ")
                tokens += items
            test_dict['tokens'] = tokens

            test_dict['orig_id'] = int(strs[0])

            # get entity1
            entity_dict = {'type': 'none', 'start': match_tag(tokens, "<e1>"), 'end': -1}
            if match_tag(tokens, "<e1>") == match_tag(tokens, "</e1>"):
                entity_dict['end'] = entity_dict['start'] + 1
            else:
                entity_dict['end'] = entity_dict['start'] + 1 + match_tag(tokens, "</e1>") - match_tag(tokens, "<e1>")
            test_dict['entities'].append(entity_dict)

            # get entity2
            entity_dict = {'type': 'none', 'start': match_tag(tokens, "<e2>"), 'end': -1}
            if match_tag(tokens, "<e2>") == match_tag(tokens, "</e2>"):
                entity_dict['end'] = entity_dict['start'] + 1
            else:
                entity_dict['end'] = entity_dict['start'] + 1 + match_tag(tokens, "</e2>") - match_tag(tokens, "<e2>")
            test_dict['entities'].append(entity_dict)

        # get relations from the 2nd line
        if l == 'Other\n':
            relation_dict = {'type': 'Other'}
            test_dict['relations'].append(relation_dict)
        elif l[0] != "\n" and l[7] != ":" and "A" <= l[0] <= "Z":
            l = l.strip("\n")
            strs = l.split("(")
            relation_dict = {'type': strs[0], 'head': -1, 'tail': -1}
            if strs[1][1] == "1":
                relation_dict['head'] = 0
                relation_dict['tail'] = 1
            elif strs[1][1] == "2":
                relation_dict['head'] = 1
                relation_dict['tail'] = 0
            test_dict['relations'].append(relation_dict)

        if l == 'Other\n':
            pass
        elif l[0] == "\n" or l[7] == ":":
            test_dict['entities'].clear()
            test_dict['relations'].clear()

        json_obj = json.dumps(test_dict)
        if test_dict['relations']:
            fo.writelines(json_obj + '\n')