import json
from google.cloud import scheduler_v1
from google.oauth2 import service_account
from datetime import datetime
from secret_values import SecretValues


class Schedular:
    @staticmethod
    def update_scheduler(minute, hr):
        key_json, location, project_id = SecretValues.scheduler_secrets()
        schedule = f"{minute} {hr} {datetime.today().day} {datetime.today().month} *"
        job_id = 'gintaa-send-custom-notification-scheduler-trigger'
        credentials = service_account.Credentials.from_service_account_info(json.loads(key_json))
        client = scheduler_v1.CloudSchedulerClient(credentials=credentials)
        job_path = client.job_path(project_id, location, job_id)
        job = client.get_job(request={"name": job_path})
        job.schedule = schedule
        job.time_zone = "Asia/Kolkata"        
        updated_job = client.update_job(request={"job": job})
        print(f"Updated job: {updated_job.name}")
