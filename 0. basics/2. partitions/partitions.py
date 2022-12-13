from pyspark.sql import SparkSession
from pyspark.rdd import portable_hash


# https://stackoverflow.com/questions/31424396/how-does-hashpartitioner-work
#  RDD.glom() → pyspark.rdd.RDD[List[T]][source]
# Return an RDD created by coalescing all elements within each partition into a list.

listaParaRDD=[]
for i in range(1,4):
    for j in range(1,3):
        listaParaRDD.append((i,None))

print(listaParaRDD)

spark = SparkSession.builder.master("local[6]").appName('ufv Partitions Spark').getOrCreate()

rdd = spark.sparkContext.parallelize(listaParaRDD,8)

print("As expected the number of partitions is ... ",rdd.getNumPartitions(), '... because we set this in parallelize method')
print("the current partitioner is ... ",rdd.partitioner, "... as we have not defined one yet (key needed)")

# Function that returns the number of elements in each partition
def to_map_partitions(partition_data): return iter([sum(1 for x in partition_data)])
rddWithDistribution = rdd.mapPartitions(to_map_partitions)
print("the distribution of data in the partitions is...",rddWithDistribution.collect())
print("the distribution of data in the partitions is...",rdd.glom().collect())


NUM_PARTITIONS=8
def hash_partitioner(clave,num_partitiones): return portable_hash(clave) % num_partitiones
rddWithHashPartitioner=rdd.partitionBy(NUM_PARTITIONS,lambda x:hash_partitioner(x,NUM_PARTITIONS))
print("the current partitioner is ... ",rddWithHashPartitioner.partitioner)
rddWithDistribution = rddWithHashPartitioner.mapPartitions(to_map_partitions)
print("the distribution of data in the partitions is...",rddWithDistribution.collect())
print("the distribution of data in the partitions is...",rddWithHashPartitioner.glom().collect())









