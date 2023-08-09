import os
import shutil

from boto3 import Session


class RemoteFileStore:
    bucket = os.getenv("S3_BUCKET")

    @property
    def s3(self):
        return Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
            region_name=os.getenv("AWS_REGION"),
        ).client('s3')

    def upload(self, filepath, filename):
        self.s3.upload_file(
            filepath,
            Bucket=self.bucket,
            Key=filename,
        )

    def upload_object(self, file_object, filename):
        self.s3.put_object(
            Body=file_object,
            Bucket=self.bucket,
            Key=filename,
        )

    def download(self, filename: str):
        self.s3.download_file(
            Bucket=self.bucket,
            Key=filename,
            Filename=os.path.join("jobs", filename),
        )

    def download_to_dir(self, filename: str, filepath: str):
        self.s3.download_file(
            Bucket=self.bucket,
            Key=filename,
            Filename=filepath,
        )

    def delete(self, filename: str):
        self.s3.delete_object(
            Bucket=self.bucket,
            Key=filename,
        )

    def list_buckets(self):
        """S3 client list of buckets with name and is creation date"""
        response = self.s3.list_buckets()['Buckets']
        for bucket in response:
            print('Bucket name: {}, Created on: {}'.format(bucket['Name'], bucket['CreationDate']))

    def list_contents(self, bucket):
        """S3 client list of Keys in specified Bucket"""
        for key in self.s3.list_objects(Bucket=bucket)['Contents']:
            print(key['Key'])

    @staticmethod
    def zip_job(job_id: str):
        job_path = os.path.join("jobs", job_id)
        shutil.make_archive(
            base_name="archive",
            format="zip",
            root_dir=job_path,
        )
