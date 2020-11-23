import json
import boto3

from logger import logger
from jsonschema_validator.validator import validate, validator
from jsonschema_validator.exceptions import JsonSchemaError, ValidationError

_SQS_CLIENT = None

_QUEUE_NAME = "valid-events-queue"


def send_event_to_queue(event, queue_name):
    """
     Responsável pelo envio do evento para uma fila
    :param event: Evento  (dict)
    :param queue_name: Nome da fila (str)
    :return: None
    """

    sqs_client = boto3.client("sqs", region_name="us-east-1")
    response = sqs_client.get_queue_url(QueueName=queue_name)
    queue_url = response["QueueUrl"]
    response = sqs_client.send_message(
        QueueUrl=queue_url, MessageBody=json.dumps(event)
    )
    print(f"Response status code: [{response['ResponseMetadata']['HTTPStatusCode']}]")


def handler(event, schema=None):
    """
    #  Função principal que é sensibilizada para cada evento
    Aqui você deve começar a implementar o seu código
    Você pode criar funções/classes à vontade
    Utilize a função send_event_to_queue para envio do evento para a fila,
        não é necessário alterá-la
    """
    try:
        validate(event, validator, schema)
        send_event_to_queue(event, _QUEUE_NAME)
    except (ValidationError, JsonSchemaError) as error:
        logger.error(msg=error.message)
