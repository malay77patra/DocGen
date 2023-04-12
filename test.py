
class RespectableApiException(Exception):
    pass


class RespectableApi:
    BASE_URL = settings.RESPECTABLE_API_BASE_URL

    SALE_ACTION = 'sales'
    REFUND_ACTION = 'refunds'

    def sale(self, payment_card_details, amount):
        params = self._get_sale_params(payment_card_details, amount)
        result = self._run_query(params)
        return self._prase_sale_response(result)

    def refund(self, payment_card_details, amount):
        params = self._get_refund_params(payment_card_details, amount)
        result = self._run_query(params)
        return self._parse_refund_response(result)

    def _get_sale_params(self, payment_card_details, amount):
        return {
            'action': self.SALE_ACTION,
            'pan': payment_card_details.card_number,
            'cvc': payment_card_details.cvc,
            'exp_month': payment_card_details.expiration_date.month,
            'exp_day': payment_card_details.expiration_date.day,
            'amount': amount
        }

    def _get_refund_params(self, payment_card_details, amount):
        return {
            'action': self.REFUND_ACTION,
            'pan': payment_card_details.card_number,
            'amount': amount
        }

    def _parse_refund_response(self, result):
        if 'success' not in result or 'refund_amount' not in result:
            raise RespectableApiException('Malformed refund response: %r', result)

        if result['success'] and result['refund_amount'] > 0:
            return True
        else:
            return False

    def _parse_sale_response(self, result):
        if 'success' not in result:
            raise RespectableApiException('Malformed sale response: %r', result)

        return bool(result['success'])

    def _get_auth_data(self):
        return HTTPBasicAuth(
            settings.RESPECTABLE_API_USERNAME,
            settings.RESPECTABLE_API_PASSWORD
        )

    def _run_query(self, params):
        url = urllib.parse.urljoin(self.BASE_URL, params['action'])
        del params['action']

        auth = self._get_auth_data()

        logger.info('Sending request to %s with amount %s', url, params['amount'])
        try:
            response = requests.post(url, json=params, auth=auth)
        except RequestException as e:
            logger.info(
                'Request to %s with amount %s failed with exception',
                url, params['amount'], e
            )
            raise RespectableApiException('Request failed')
        logger.info(
            'Sent request to %s with amount %s, response %r',
            url, params['amount'], response
        )

        decoded_response = response.json()

        if response.status_code == 200:
            return decoded_response
        else:
            try:
                error_message = decoded_response['error']
            except KeyError:
                error_message = 'Request failed with status {}'.format(response.status_code)

            raise RespectableApiException(error_message)
