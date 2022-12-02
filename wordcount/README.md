# Wordcount Spark



##### Creation of a project

```shell
PROJECT_ID="ufv-pyspark-wc-javi"
gcloud projects create $PROJECT_ID
gcloud projects list --sort-by=projectId --limit=5
gcloud config set project $PROJECT_ID
# Choose one of the zones for the project
gcloud compute zones list --format="value(selfLink.scope())"
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
gcloud compute instances list --format="json"
```

### Run Spark Job

```shell
gcloud dataproc jobs submit pyspark gs://$PROJECT_ID/spark-wordcount.py --cluster $PROJECT_ID --region us-central1
```

### Fix failure
This is intended to fail here, do the changes you need to do in order to fix this.

```shell
git fetch
git pull
cd spark-hands-on/wordcount/
```

Upload the revised code to the bucket.
```shell
gsutil -m cp spark-wordcount.py gs://$PROJECT_ID
# check the file was replaced seeing the time
gsutil ls -al gs://$PROJECT_ID
```


```shell
gcloud dataproc jobs submit pyspark gs://$PROJECT_ID/spark-wordcount.py --cluster $PROJECT_ID --region us-central1
```

Now it works fine and the result should show something like this:
```shell
[('Dog', ['Noir']), ('Dog', ['Bree']), ('Dog', ['Pickles']), ('Dog', ['Sparky']), ('Cat', ['Tom']), ('Cat', ['Alley']), ('Cat', ['Cleo']), ('Frog', ['Kermit']), ('Pig', ['Bacon']), ('Pig', ['Babe']), ('Dog', ['Gigi']), ('Cat', ['George']), ('Frog', ['Hoppy']), ('Pig', ['Tasty']), ('Dog', ['Fred']), ('Cat', ['Suzy'])]
[('Dog', ['Noir', 'Bree', 'Pickles', 'Sparky', 'Gigi', 'Fred']), ('Cat', ['Tom', 'Alley', 'Cleo', 'George', 'Suzy']), ('Frog', ['Kermit', 'Hoppy']), ('Pig', ['Bacon', 'Babe', 'Tasty'])]
[('Dog', 6), ('Cat', 5), ('Frog', 2), ('Pig', 3)]
```

### Decommissioning

##### Decommission Cluster

```shell
gcloud dataproc clusters delete $PROJECT_ID --region us-central1
gcloud dataproc clusters list --region=us-central1
```

##### Decommission Project
```shell
gcloud projects list --format="table(projectId,parent.id.yesno(yes="YES", no=”NO”):label='Has Parent':sort=2)"
gcloud projects delete $PROJECT_ID
gcloud projects list --format="table(projectId,parent.id.yesno(yes="YES", no=”NO”):label='Has Parent':sort=2)"
# During a period you can undone this hard operation
gcloud projects undelete $PROJECT_ID
gcloud projects list --format="table(projectId,parent.id.yesno(yes="YES", no=”NO”):label='Has Parent':sort=2)"
gcloud projects delete $PROJECT_ID
```

