# dataproc


### Enable the Compute Engine, Dataproc and BigQuery Storage APIs:

```
gcloud services enable compute.googleapis.com \
dataproc.googleapis.com \
bigquerystorage.googleapis.com
```


gcloud config set project <project_id>

gcloud config set dataproc/region europe-southwest1-a


#### Cluster creation

```shell
CLUSTER_NAME=spark-bigquery-lab

gcloud beta dataproc clusters create ${CLUSTER_NAME} \
--worker-machine-type n1-standard-8 \
--num-workers 8 \
--image-version 1.5-debian \
--initialization-actions gs://dataproc-initialization-actions/python/pip-install.sh \
--metadata 'PIP_PACKAGES=google-cloud-storage' \
--optional-components=ANACONDA \
--enable-component-gateway
```

#### Bucket creation

```shell
BUCKET_NAME=<bucket_name>
gsutil mb gs://${BUCKET_NAME}
```

#### Spark job submit with Dataproc example
```shell
  gcloud dataproc jobs submit pyspark \
        --cluster ${CLUSTER_NAME} \
        --jars gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
        --driver-log-levels root=FATAL \
        backfill.py \
        -- ${year} ${month} ${BUCKET_NAME} &
    sleep 5
```

#### Spark job submit with Dataproc example

BigQuery uses a Columnar Storage Format, similar to Parquet. It is called Capacitor, in this article Google explains how it improves Parquet allowing for better compression:
https://cloud.google.com/blog/products/bigquery/inside-capacitor-bigquerys-next-generation-columnar-storage-format
Interesting thing is that Parquet allows for partitioning in many files and same here
The jar we add in the job submit is a helper from GCP to connect to BigQuery columnar format
table_df = (spark.read.format('bigquery').option('table', table).load())
format('bigquery') needs the connector to be present

```shell
cd
git clone https://github.com/GoogleCloudPlatform/cloud-dataproc
cd ~/cloud-dataproc/codelabs/spark-bigquery
gcloud dataproc jobs submit pyspark --cluster ${CLUSTER_NAME} \
    --jars gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    --driver-log-levels root=FATAL \
    counts_by_subreddit.py
```
