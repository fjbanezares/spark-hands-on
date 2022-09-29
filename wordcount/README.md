# Wordcount Spark



##### Creation of a project

```shell
PROJECT_ID="ufv-pyspark-wc-javi"
gcloud projects create $PROJECT_ID
gcloud projects list --sort-by=projectId --limit=5
gcloud config set project $PROJECT_ID
```

##### Enable billing
```shell
gcloud billing accounts list
BILLING_ACCOUNT=`gcloud alpha billing accounts list | grep ACCOUNT | awk -F ':' '{print $2}'`
gcloud alpha billing projects link $PROJECT_ID --billing-account $BILLING_ACCOUNT
```

### Data will be in a GCP bucket

##### Creation of a Bucket

gsutil is a tool that lets you access Cloud Storage from the command line

```shell
gsutil mb gs://$PROJECT_ID
```

##### Copy of files in the bucket
```shell
gsutil -m cp animal-funny-names.txt gs://ufv_pyspark_wc_demo-developer-javi
gsutil -m cp spark-wordcount.py gs://ufv_pyspark_wc_demo-developer-javi
``` 

### Create a Dataproc cluster
```shell
gcloud dataproc clusters create ufv-dataproc-cluster --region=us-central1

```

### Run Spark Job
gcloud dataproc jobs submit pyspark gs://ufv_pyspark_wc_demo-developer-javi/spark-wordcount.py



