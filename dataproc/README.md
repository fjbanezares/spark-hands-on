


gcloud auth list
gcloud config list project
gcloud config set project <PROJECT_ID>
echo $GOOGLE_CLOUD_PROJECT
gcloud config set compute/zone us-central1-f


CLUSTERNAME=${USER}-dplab


gcloud dataproc clusters create ${CLUSTERNAME} \
--region=us-central1 \
--scopes=cloud-platform \
--tags codelab \
--zone=us-central1-c
