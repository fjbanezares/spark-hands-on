#!/usr/bin/env python

from pyspark import SparkContext

# we will just execute all in the Master Node without distributing the load
sc = SparkContext("local")

file = sc.textFile("gs://ufv_pyspark_wc_demo-developer-javi/animal-funny-names.txt")

# creation of key value pairs being the value a list
dataLines = file.map(lambda s: s.split(",")).map(lambda x: (x[0], [x[1]]))
print(dataLines.take(100))

# For the reduction we concatenate lists
databyKey = dataLines.reduceByKey(lambda a,b: a + b)
print(databyKey.take(100))

# now we return the key and the number of elements per key
countByKey = databyKey.map(lambda k_v: (k_v[0], len(k_v[1])))
print(countByKey.take(100))
