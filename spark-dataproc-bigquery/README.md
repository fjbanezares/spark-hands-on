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
