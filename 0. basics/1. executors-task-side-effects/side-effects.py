from pyspark.sql import SparkSession
import random
import time


NUM_SAMPLES=1000000


def inside(dummy):
    '''
    :param dummy: we give this because the lambda in the filter will pass a number that we will not use but need to take
    :return: wheher or not a random generated number is between a circle d^2 rectangle, Pi*d^2/4 circle, Pi/4 division
    '''
    x, y = random.random(), random.random()
    return x*x + y*y < 1


spark = SparkSession.builder.master("local[4]").appName('ufv Pi estimate Spark').getOrCreate()

count = spark.sparkContext.parallelize(range(0, NUM_SAMPLES)).filter(inside).count()


print('The number of samples in the circle is...', count)
print('The total number of samples is...', NUM_SAMPLES)
print("Pi is roughly %f" % (4.0 * count / NUM_SAMPLES))



counter = 10
rdd = spark.sparkContext.parallelize(range(0, 5))

print(rdd.take(12))

# Wrong: Don't do this!!
def increment_counter(x):
    time.sleep(random.random())
    print(x)
    global counter
    print("contador es...", counter)
    time.sleep(random.random())
    counter += x
    print("ahora contador es...",counter)

print("the current partitioner is ... ",rdd.partitioner)
print("As expected the number of partitions is ... ",rdd.getNumPartitions())
rdd.foreach(increment_counter)

print("Counter value: ", counter, "...this is because the variable is within driver thread instead of executor's")

# In local mode, in some circumstances, the foreach function will actually execute within the same JVM as the driver
# and will reference the same original counter, and may actually update it.

# In general, closures - constructs like loops or locally defined methods,
# should not be used to mutate some global state. Spark does not define or guarantee the behavior of mutations
# to objects referenced from outside of closures. Some code that does this may work in local mode,
# but that’s just by accident and such code will not behave as expected in distributed mode.
# Use an Accumulator instead if some global aggregation is needed.

accum = spark.sparkContext.accumulator(0)
print(accum)

def increment_accumulator(x):
    time.sleep(random.random())
    print(x)
    time.sleep(random.random())
    accum.add(x)


rdd.foreach(lambda x:increment_accumulator(x))
print(accum.value)
# now we have what we want!

