#!/usr/bin/python
# Using REST-API of http://search.maven.org to find results by sha1sum of a given jar.

import sys
import json
import urllib2
import hashlib

def hashfile(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()

def request( hash ):
    url = 'http://search.maven.org/solrsearch/select?q=1:"'+hash+'"&wt=json&rows=20'
    response = urllib2.urlopen(url).read()
    return json.loads(response);


# Example: http://search.maven.org/remotecontent?filepath=commons-io/commons-io/2.4/commons-io-2.4.pom
def getAllPaths( doc ):
    prefix='http://search.maven.org/remotecontent?filepath=';
    group=doc["g"]
    groupPath=group.replace(".","/")
    name=doc["a"]
    version=doc["v"]
    fullPrefix = prefix + groupPath + "/" +  name + "/" + version + "/" + name + "-" + version
    result=[]
    for ec in doc["ec"]:
        result.append( fullPrefix + ec )
    return result 


filename = sys.argv[1]
sha1=hashfile( sys.argv[1] )
print sha1 + ' ' + filename
obj = request( sha1 )
print obj["response"]["numFound"]
for path in getAllPaths( obj["response"]["docs"][0] ):
    print "\t" +  path;
#print json.dumps(obj, indent=4)
