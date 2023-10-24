import requests
from datetime import datetime as dt
from collections import deque


class NumberRequester:

    endpoint = 'http://numbersapi.com/random/math'

    def __init__(self):
        self.__call_number = 0
        self.log = []

    def call(self):
        timestamp = dt.now().isoformat()
        self.__call_number += 1
        response = requests.get(self.endpoint)
        status = response.status_code
        if status == 200:
            awesome_fact = response.text
            number = int(awesome_fact.split()[0])
            result = {'result': 'SUCCESS',
                      'number': number, "fact": awesome_fact}
            log_item = {
                'request_number': self.__call_number,
                'call_time': timestamp,
                'end_point': self.endpoint,
                'result': 'SUCCESS',
                'number': number
            }
            self.log.append(log_item)
            return result
        else:
            result = {'result': 'FAILURE', 'error_code': status}
            log_item = {
                'request_number': self.__call_number,
                'call_time': timestamp,
                'end_point': self.endpoint,
                'result': 'FAILURE'
            }
            self.log.append(log_item)
            return result


class NumberCruncher:

    def __init__(self, size_of_tummy, requester):
        self._tummy = deque(maxlen=size_of_tummy)
        self.max_tummy_size = size_of_tummy
        self.requester = requester

    def crunch(self):
        try:
            result = self.requester.call()
            if result['number'] % 2 == 0:
                digested = {
                    'number': result['number'],
                    "fact": result['fact']
                }
                if len(self._tummy) < self.max_tummy_size:
                    self._tummy.append(digested)
                    return f'Yum! {digested["number"]}'
                else:
                    popped = self._tummy[0]
                    self._tummy.append(digested)
                    return f'Burp! {popped["number"]}'
            else:
                return f'Yuk! {result["number"]}'
        except Exception as e:
            print(e)
            raise RuntimeError('Unexpected error')

    def tummy(self):
        return list(self._tummy)
