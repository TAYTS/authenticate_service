from flask import current_app
import boto3


def save_to_dynamoDB(
        id_ticket,
        message,
        message_type,
        create_timestamp,
        fileDS):
    """
    Save the message record to the dynamoDB

    Arguments:
        id_ticket(str): uuid for the associated ticket
        message(str): content of the message
        message_type(int): indicate the message type 1 for client, 2 for admin
        create_timestamp(datetime): timestamp for creating the message
        fileDS(array dict): data structure for all the files info

    Returns:
        status (boolean): True if successfully save the record else False
    """

    status = True
    # Get the dynamoDB service
    dynamodb = boto3.client(
        "dynamodb",
        region_name=current_app.config["AWS_REGION"],
        aws_access_key_id=current_app.config["AWS_KEY"],
        aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"]
    )

    newFileDS = []

    for file in fileDS:
        base = {
            "M": {
                "filename": {
                    "S": file["filename"]
                },
                "filetype": {
                    "S": file["filetype"]
                },
                "url": {
                    "S": file["url"]
                }
            }
        }
        newFileDS.append(base)

    try:
        response = dynamodb.put_item(
            TableName=current_app.config["DYNAMO_TABLENAME"],
            Item={
                "ID_TICKET": {
                    "S": id_ticket
                },
                "MESSAGE": {
                    "S": message
                },
                "CREATE_TIMESTAMP": {
                    "N": str(create_timestamp.timestamp())
                },
                "MESSAGE_TYPE": {
                    "N": str(message_type)
                },
                "MEDIA": {
                    "L": newFileDS
                }
            }
        )

        if (response.get("ResponseMetadata").get("HTTPStatusCode") != 200):
            status = False
    except Exception as e:
        current_app.logger.error(
            "Unable to add record to dynamoDB " + str(e))
        status = False

    return status
