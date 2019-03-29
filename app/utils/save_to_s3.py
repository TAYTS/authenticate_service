from flask import current_app
import boto3
import shutil


def save_to_s3(local_filepaths, fileDS, directory_path):
    # Upload to S3 bucket
    S3_BUCKET = current_app.config["S3_BUCKET"]
    S3_KEY = current_app.config["AWS_KEY"]
    S3_SECRET = current_app.config["AWS_SECRET_ACCESS_KEY"]
    S3_LOCATION = current_app.config["S3_LOCATION"]

    # Create the instance connection to the S3 bucket
    s3 = boto3.client(
        's3',
        aws_access_key_id=S3_KEY,
        aws_secret_access_key=S3_SECRET
    )

    try:
        for i in range(len(local_filepaths)):
            path = local_filepaths[i].replace(
                current_app.config["TEMP_DIR"],
                ""
            )
            s3.upload_file(
                Bucket=S3_BUCKET,
                Filename=local_filepaths[i],
                Key=path
            )
            fileDS[i]["url"] = S3_LOCATION + path
    except Exception as e:
        current_app.logger.info("Unable to upload files to S3: " + str(e))
    finally:
        shutil.rmtree(directory_path)

    return fileDS
