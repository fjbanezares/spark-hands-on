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

##### Clone this repo in your gcloud machine
```shell
git clone https://github.com/fjbanezares/spark-hands-on.git
cd spark-hands-on/wordcount/
```

##### Copy of files in the bucket
```shell
gsutil -m cp animal-funny-names.txt gs://$PROJECT_ID
gsutil -m cp spark-wordcount.py gs://$PROJECT_ID
gsutil ls gs://$PROJECT_ID
```

### Create a Dataproc cluster
```shell
gcloud dataproc clusters create $PROJECT_ID --region=us-central1
# This will take minutes to procure
gcloud dataproc clusters list --region=us-central1
```

### Run Spark Job
gcloud dataproc jobs submit pyspark gs://$PROJECT_ID/spark-wordcount.py


```shell
gcloud dataproc jobs submit pyspark gs://$PROJECT_ID/spark-wordcount.py --cluster $PROJECT_ID --region us-central1
```

