import os
import base64
import requests


class OrangeAPIClient:
    '''
    API Client class for the orange developer
    api with request authorization
    '''
    __API_BASE_URL = "https://api.orange.com"

    def __init__(self, client_id, client_secret):
        secret_string = "%s:%s" % (client_id, client_secret)
        oauth_credentials = base64.b64encode(
            secret_string.encode("utf-8")).decode("utf-8")
        self.oauth_authorization_header = "Basic %s" % oauth_credentials
        self.__set_client_access_credentials()

    def __set_client_access_credentials(self):
        '''
        Sample credentials:
        {
        "token_type": "Bearer",
        "access_token": "i6m2iIcY0SodWSe...L3ojAXXrH",
        "expires_in": "7776000"
        }
        '''
        response = requests.post(f"{self.__API_BASE_URL}/oauth/v2/token",
                                 {'grant_type': 'client_credentials'},
                                 headers={'Authorization': self.oauth_authorization_header})
        self.access_credentials = response.json()

        if 'error' in self.access_credentials:
            raise Exception('Failed to get access credentials: ',
                            self.access_credentials)

        self.authorization = f'{self.access_credentials["token_type"]} {self.access_credentials["access_token"]}'

    def post_json(self, path: str, data: dict) -> dict:
        response = requests.post(f"{self.__API_BASE_URL}{path}", json=data, headers={
                                 'Authorization': self.authorization})
        return response.json()

    def get_json(self, path: str) -> dict:
        response = requests.get(f"{self.__API_BASE_URL}{path}", headers={
                                'Authorization': self.authorization, 'Accept': 'application/json'})
        return response.json()


class TableAnnotationAPIClient(OrangeAPIClient):
    '''
    API Client:
    Orange Table Annotation
    Semantic Annotation Toolkit for Tabular Data

    NOTE: This API is in beta and may not work as intended
    '''

    def __init__(self):
        client_id = os.environ.get('ORANGE_CLIENT_ID')
        if not client_id:
            raise Exception("'ORANGE_CLIENT_ID' not set")

        client_secret = os.environ.get('ORANGE_CLIENT_SECRET')
        if not client_secret:
            raise Exception("'ORANGE_CLIENT_SECRET' not set")

        super().__init__(client_id, client_secret)

    def preprocess(self, data):
        prepared_data = self.prepare_core_data_item(data)
        return self.post_json("/table_annotation/beta/preprocessing", prepared_data)

    def get_preprocess_task_status(self, task_id):
        return self.get_json(f"/table_annotation/beta/preprocessing/{task_id}")

    def get_preprocess_task_result_light(self, task_id):
        return self.get_json(f"/table_annotation/beta/preprocessing/{task_id}/result?format=light")

    def get_preprocess_task_result_heavy(self, task_id):
        return self.get_json(f"/table_annotation/beta/preprocessing/{task_id}/result")

    # pylint: disable=no-self-use
    def annotate(self):
        raise Exception(
            'Check updates from: https://developer.orange.com/apis/table-annotation/getting-started')

    @classmethod
    def prepare_core_data_item(cls, item) -> dict:
        return {
            'data': item['relation']
        }
