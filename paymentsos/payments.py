class Payment(object):

    def __init__(self, client):
        self.client = client

    def create_token(self, *, holder_name, card_number, credit_card_cvv, expiration_date, token_type='credit_card',
                     identity_document=None, billing_address=None, additional_details=None):
        """
        When creating a Token, remember to use the public-key header instead of the private-key header,
        and do not include the app-id header.

        Args:
            holder_name: Name of the credit card holder.
            card_number: Credit card number.
            credit_card_cvv: The CVV number on the card (3 or 4 digits) to be encrypted.
            expiration_date: Credit card expiration date. Possible formats: mm-yyyy, mm-yy, mm.yyyy,
            mm.yy, mm/yy, mm/yyyy, mm yyyy, or mm yy.
            token_type: The type of token
            billing_address: Address.
            identity_document: National identity document of the card holder.
            additional_details: Optional additional data stored with your token in key/value pairs.

        Returns:

        """
        if not isinstance(billing_address, dict):
            raise Exception
        headers = {
            'public_key': self.client.public_key,
        }
        payload = {
            "token_type": token_type,
            "credit_card_cvv": credit_card_cvv,
            "card_number": card_number,
            "expiration_date": expiration_date,
            "holder_name": holder_name,
            "identity_document": identity_document,
            "billing_address": billing_address,
            "additional_details": additional_details,
        }
        return self.client._post(self.client.URL_BASE + '/tokens', json=payload, headers=headers)

    def retrieve_token(self, token):
        """
        Retrieve Token details for a specific Token.

        Args:
            token: The identifier of the token.


        Returns:

        """
        headers = {
            'app_id': self.client.app_id,
            'private_key': self.client.private_key,
        }
        return self.client._get(self.client.URL_BASE + '/tokens/{}'.format(token), headers=headers)

    def create_payment(self, *, amount, currency, order=None, customer_id=None, billing_address=None,
                       shipping_address=None, additional_details=None, statement_soft_descriptor=None):
        """
        Creates a payment object, which provides a single reference to all the transactions that make up a payment.
        This is the first step for all financial transactions.

        Args:
            amount: Amount must be greater than 0. The amount is formatted in Minor Units format.
            currency: The three character currency code in ISO-4217 format.
            order: Details of the order.
            customer_id: Identifier of the customer associated with this payment.
            billing_address: Billing address details. This will only be sent to providers who support
            billing addresses, in requests that support them. Note: The billing address details will be sent "as is",
            without any corrections or substitutions from the billing address in the token resource.
            shipping_address: Shipping address details. This will only be sent to providers who support
            shipping addresses, in requests that support them. Note: The shipping address details will be sent "as is",
            without any corrections or substitutions from the shipping address in the customer resource.
            additional_details: Optional additional data stored in key/value pairs.
            statement_soft_descriptor: The transaction description that will appear in the
            customer's credit card statement, which identifies the merchant and payment.
            Check the relevant provider sites to see if this field is supported.
            If so, see the required content and format. Note: This transaction description is generated by you.
            Providing a clear description helps your customers recognize their transactions, and reduces chargebacks.

        Returns:

        """
        headers = {
            'app_id': self.client.app_id,
            'private_key': self.client.private_key,
        }
        payload = {
            "amount": amount,
            "currency": currency,
            "order": order,
            "customer_id": customer_id,
            "billing_address": billing_address,
            "shipping_address": shipping_address,
            "additional_details": additional_details,
            "statement_soft_descriptor": statement_soft_descriptor,
        }
        return self.client._post(self.client.URL_BASE + '/payments', json=payload, headers=headers)

    def create_charge(self, payment_id, token, credit_card_cvv=None, user_agent=None, ip_address=None):
        headers = {
            'app_id': self.client.app_id,
            'private_key': self.client.private_key,
            'x-client-user-agent': user_agent,
            'x-client-ip-address': ip_address,
        }
        payload = {
            "payment_method": {
                "type": "tokenized",
                "token": token,
                "credit_card_cvv": credit_card_cvv
            }
        }
        return self.client._post(self.client.URL_BASE + '/payments/{}/charges'.format(payment_id), json=payload,
                                 headers=headers)

    def create_authorization(self, payment_id, token, credit_card_cvv=None, user_agent=None, ip_address=None):
        headers = {
            'app_id': self.client.app_id,
            'private_key': self.client.private_key,
            'x-client-user-agent': user_agent,
            'x-client-ip-address': ip_address,
        }
        payload = {
            "payment_method": {
                "type": "tokenized",
                "token": token,
                "credit_card_cvv": credit_card_cvv
            },
            "reconciliation_id": "23434534534"
        }

        return self.client._post(self.client.URL_BASE + '/payments/{}/authorizations'.format(payment_id), json=payload,
                                 headers=headers)

    def create_capture(self, payment_id):
        headers = {
            'app_id': self.client.app_id,
            'private_key': self.client.private_key,
        }
        return self.client._post(self.client.URL_BASE + '/payments/{}/captures'.format(payment_id), headers=headers)
