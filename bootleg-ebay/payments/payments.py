from typing import Dict, Any
import copy
import json

CardInfo = Dict[str, Any]
TransactionInfo = Dict[str, Any]
PaymentID = int
TransactionID = int

class APIError(Exception):
    """All custom API Exceptions"""
    pass 

class BadInputError(APIError):
    """Custom bad input error class."""
    code = 400
    description = "Bad input Error"
    
class PaymentCard:
    """Class for containing information regarding the payment card
    """

    def __init__(self, payment_id: PaymentID, card_info: CardInfo):
        self._payment_id = payment_id

        self._card_info = {
            'user_id': None,
            'card_number': None,
            'security_code': None,
            'expiration_date': None,
        }

        for k in card_info.keys():
            if k not in self._card_info:
                raise ValueError('You cannot have key: {} in card_info!'.format(k))

        self._card_info.update(card_info)

    @property
    def payment_id(self):
        return self._payment_id

    @property
    def card_info(self):
        return self._card_info

    @classmethod
    def from_dict(cls, dict_):
        payment_id = dict_['payment_id']
        del dict_['payment_id']
        payment_card = cls(payment_id, card_info=dict_)
        return payment_card

    def to_dict(self):
        dict_ = copy.deepcopy(self.card_info)
        dict_['payment_id'] = self.payment_id
        dict_['expiration_date'] = dict_['expiration_date'].strftime("%-Y-%-m-%-d")
        return dict_

    def to_json(self):
        user_info = self.to_dict()
        return json.dumps(user_info)


class Transaction:
    """Class for containing information regarding transactions
    """

    def __init__(self, transaction_id: PaymentID, transaction_info: CardInfo):
        self._transaction_id = transaction_id

        self._transaction_info = {
            'user_id': None,
            'payment_id': None,
            'money': None,
        }

        for k in transaction_info.keys():
            if k not in self._transaction_info:
                raise ValueError('You cannot have key: {} in transaction_info!'.format(k))

        self._transaction_info.update(transaction_info)

    @property
    def transaction_id(self):
        return self._transaction_id

    @property
    def transaction_info(self):
        return self._transaction_info

    @classmethod
    def from_dict(cls, dict_):
        transaction_id = dict_['transaction_id']
        del dict_['transaction_id']
        transaction = cls(transaction_id, card_info=dict_)
        return transaction

    def to_dict(self):
        dict_ = copy.deepcopy(self.transaction_info)
        dict_['transaction_id'] = self.transaction_id
        return dict_

    def to_json(self):
        user_info = self.to_dict()
        return json.dumps(user_info)
