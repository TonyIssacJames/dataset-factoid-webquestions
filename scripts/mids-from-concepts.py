#!/usr/bin/python -u
#
# Creates datase of freebase keys generated from question concepts
#
# Usage: freebaseKey-from-concepts.py dump.json
#
# File dump.json needs to contain array of objetcs for each question. Each object needs to have following fields:
# qId and Concepts. This file can be generated by YodaQa command ./gradlew questionDump.

from SPARQLWrapper import SPARQLWrapper, JSON
import json, sys

def queryFreebasekey(page_id):
    url = 'http://freebase.ailao.eu:3030/freebase/query'
    sparql = SPARQLWrapper(url)
    sparql.setReturnFormat(JSON)
    sparql_query = '''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT * WHERE { 
?topic <http://rdf.freebase.com/key/wikipedia.en_id> "''' + page_id + '''" .
} '''
    sparql.setQuery(sparql_query)
    res = sparql.query().convert()
    s = set()
    retVal = []
    for r in res['results']['bindings']:
        if (r['topic']['value'] not in s):
            retVal.append(r['topic']['value'][27:])
        s.add(r['topic']['value'])
    return retVal

print("[")
with open(sys.argv[1]) as f:
    dump = json.load(f)
    for i, line in enumerate(dump):
        res_line = {}
        res_line['qId'] = line['qId']
        res_line['mid'] = []
        for c in line['Concept']:            
            pair = {}
            pair['concept'] = c['fullLabel']
            pair['key'] = queryFreebasekey(c['pageID'])
            res_line['mid'].append(pair)
        # print (json.dumps(res_line))
        if (i+1 != len(dump)):
            print(json.dumps(res_line) + ",")
        else:
            print (json.dumps(res_line))
print("]")