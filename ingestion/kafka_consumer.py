import os
import json
import logging
from postprocessing.annotation import TableAnnotationAPIClient
from ingestion.collection import ArangoTableCollector
from kafka import KafkaConsumer


rootLogger = logging.getLogger("ingestion_application")
rootLogger.setLevel(logging.INFO)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.INFO)
rootLogger.addHandler(consoleHandler)

class Consumer:
    '''
    A Kafka ingestion class that collects the messages from the broker,
    validates them against the schema and inserts them into arangodb database
    '''
    __OFFSET_LISTENING_POLICY = 'latest'
    __MAX_POLL_RECORDS = 200

    def __init__(self):
        bootstrap_servers = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')
        if not bootstrap_servers:
            raise Exception('KAFKA_BOOTSTRAP_SERVERS not defined')

        self.topic_name = os.environ.get('KAFKA_TOPIC')
        if not self.topic_name:
            raise Exception('KAFKA_TOPIC not defined')
        
        self.database_collector = ArangoTableCollector()
        self.consumer = KafkaConsumer(bootstrap_servers = bootstrap_servers,
                        auto_offset_reset = self.__OFFSET_LISTENING_POLICY,
                        max_poll_records = self.__MAX_POLL_RECORDS)
        self.annotation_client = TableAnnotationAPIClient()

        rootLogger.info('Connected to Kafka brokers at %s', bootstrap_servers)

    def begin_ingestion(self):
        if not self.consumer.bootstrap_connected():
            raise Exception('Not connected to Kafka servers')

        self.consumer.subscribe([self.topic_name])
        rootLogger.info("Subscribed to the topic %s", self.topic_name)
            
        for message in self.consumer:
            self.__validate_and_insert(message)

    # pylint: disable=broad-except
    def __validate_and_insert(self, message):
        try:
            payload = json.loads(message.value)
        except Exception:
            rootLogger.error('Unable to parse the json incoming message with offset %s', message.offset)
            return

        try:
            preprocess_additions = self.annotation_client.preprocess(payload)

            # check if preprocessing was executed synchronously
            if 'output' in preprocess_additions:
                preprocess_additions = preprocess_additions['output']

            payload['preprocessing'] = preprocess_additions
        except Exception as e:
            rootLogger.exception('Failed to preprocess table: %s', e)

        try:
            # Insert into database
            self.database_collector.append(payload)
            rootLogger.info('Succesfully inserted incoming message with offset %s on topic %s into the database', message.offset, message.topic)
        except Exception as e: # gracefully catch all the exceptions and continue message ingestion
            rootLogger.exception('Unable to process message due to follwing error: %s', e)  


def main():
    kakfa_consumer = Consumer()

    # start the ingestion process
    kakfa_consumer.begin_ingestion()

if __name__ == "__main__":
    main()
