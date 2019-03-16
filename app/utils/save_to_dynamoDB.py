from flask import current_app
import boto3


def save_to_dynamoDB(id_message, id_ticket, message, create_timestamp):
    """
    Save the message record to the dynamoDB

    Arguments:
        id_message(str): uuid for the message
        id_ticket(str): uuid for the associated ticket
        message(str): content of the message
        create_timestamp(datetime): timestamp for creating the message

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

    try:
        response = dynamodb.put_item(
            TableName=current_app.config["DYNAMO_TABLENAME"],
            Item={
                "ID_MESSAGE": {
                    "S": id_message
                },
                "ID_TICKET": {
                    "S": id_ticket
                },
                "MESSAGE": {
                    "S": message
                },
                "CREATE_TIMESTAMP": {
                    "N": str(create_timestamp.timestamp())
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
