
import json

# from macros import CALL_SITES_JSON
from macros import KNOWLEDGE_CLIENTS_JSON_FILE


# def findCallSiteByCid(cid):
#     with open(CALL_SITES_JSON, 'r') as fr:
#         callsites = json.load(fr)
#         for c in callsites:
#             if c['id'] == cid:
#                 return c
#     return None


# def findKnowledgeByKid(kid):
#     with open(KNOWLEDGE_JSON, 'r') as fr:
#         knowledge = json.load(fr)
#         for k in knowledge:
#             if k['id'] == kid:
#                 return k
#     return None


def findKnowledgeClientByKid(kid):
    with open(KNOWLEDGE_CLIENTS_JSON_FILE, 'r') as fr:
        knowledge = json.load(fr)
        for k in knowledge:
            if k['id'] == kid:
                return k
    return None


# def findKnowledgeByAPI(api):
#     with open(KNOWLEDGE_JSON, 'r') as fr:
#         knowledge = json.load(fr)
#     for k in knowledge:
#         if k['API'] == api:
#             return k
#     return None
