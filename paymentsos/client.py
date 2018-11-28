import logging

import requests

from paymentsos.payments import Payment

fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)


class Client(object):
    URL_BASE = 'https://api.paymentsos.com'

    def __init__(self, app_id, private_key, api_version='1.2.0', test=False, debug=False):
        self.app_id = app_id
        self.private_key = private_key
        self.api_version = api_version
        self.test = test
        self.debug = debug

        self.payments = Payment(self)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    @property
    def is_test(self):
        return self.test

    @property
    def is_debug(self):
        return self.debug

    def _get(self, url, **kwargs):
        return self._request('GET', url, **kwargs)

    def _post(self, url, **kwargs):
        return self._request('POST', url, **kwargs)

    def _put(self, url, **kwargs):
        return self._request('PUT', url, **kwargs)

    def _delete(self, url, **kwargs):
        return self._request('DELETE', url, **kwargs)

    def _request(self, method, url, headers=None, **kwargs):
        _headers = {
            'app_id': self.app_id,
            'private_key': self.private_key,
            'api-version': self.api_version,
            'x-payments-os-env': 'test' if self.test else 'live',
            'idempotency_key': '123',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        if headers:
            _headers.update(headers)

        if self.is_debug:
            self.logger.debug('{} {} {} {}'.format(method, url, headers, kwargs))
        return self._parse(requests.request(method, url, headers=_headers, timeout=60, **kwargs))

    def _parse(self, response):
        if 'Content-Type' in response.headers and 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            if self.is_debug:
                fmt = 'The response with status code ({}) is not JSON deserializable. Response: {}'
                self.logger.warning(fmt.format(response.status_code, response.text))

            r = response.text
        return r