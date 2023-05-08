import json
from macros import INCOMPATIBILITY_JSON_FILE

def findIncompatibilityById(id):
    with open(INCOMPATIBILITY_JSON_FILE, 'r') as fr:
        knowledge = json.load(fr)
        for k in knowledge:
            if k['id'] == id:
                return k
    return None


# def findKnowledgeByAPI(api):
#     with open(KNOWLEDGE_JSON, 'r') as fr:
#         knowledge = json.load(fr)
#     for k in knowledge:
#         if k['API'] == api:
#             return k
#     return None
