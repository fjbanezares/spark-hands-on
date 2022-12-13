
from pyspark.sql import SparkSession
from tempfile import NamedTemporaryFile
tempFile = NamedTemporaryFile(delete=True) # creates temp file and folder with random name
tempFile.close()

spark = SparkSession.builder.master("local[6]").appName('ufv Partitions Spark').getOrCreate()

rdd = spark.sparkContext.parallelize(range(10)).saveAsTextFile(tempFile.name)

from fileinput import input
from glob import glob
print(tempFile.name + "/part-0000*")
print(sorted(input(glob(tempFile.name + "/part-0000*"))))
print(''.join(sorted(input(glob(tempFile.name + "/part-0000*")))))



## with compression
tempFile3 = NamedTemporaryFile(delete=True)
tempFile3.close()
codec = "org.apache.hadoop.io.compress.GzipCodec"
spark.sparkContext.parallelize(['foo', 'bar']).saveAsTextFile(tempFile3.name, codec)
from fileinput import input, hook_compressed
result = sorted(input(glob(tempFile3.name + "/part*.gz"), openhook=hook_compressed))
print(result)
print(''.join([r.decode('utf-8') if isinstance(r, bytes) else r for r in result]))
