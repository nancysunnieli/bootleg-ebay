from typing import Dict, Any, Sequence, Optional
import json

from mysql.connector import connect, Error

from payments import PaymentCard, Transaction, BadInputError

PaymentInfo = Dict[str, Any]
TransactionInfo = Dict[str, Any]
PaymentID = int
TransactionID = int
UserID = int

class PaymentsDBManager:

    @classmethod
    def _create_connection(cls):
        connection = connect(
            host="payments-db",
            port="3306",
            user="%s" % ("root"),
            password="%s" % ("bootleg2"),
            database="payments",
        )
        return connection

    @classmethod
    def insert(cls, data: Sequence):
        """Insert row into payments database.

        Args: 
            data: List of rows to be inserted
        """
        cmd = "INSERT INTO {} ({}) VALUES ({})".format(
            cls.table_name, 
            ', '.join(cls.table_cols),
            ', '.join(['%s'] * len(cls.table_cols)))

        with cls._create_connection() as c:
            with c.cursor() as cursor:
                cursor.execute(cmd, data)

            last_row_id = cursor.lastrowid
            c.commit()

        return last_row_id

    @classmethod
    def update_by_id(cls, info: Dict) -> None:
        """Update the database by id
        """
        set_cmd = ["{} = %s".format(c) for c in cls.table_cols]
        set_cmd = ", ".join(set_cmd)
        cmd = "UPDATE {} SET {} WHERE {} = %s".format(cls.table_name, set_cmd, cls.id_name)

        val = [info[c] for c in cls.table_cols]
        with cls._create_connection() as c:
            with c.cursor() as cursor:
                cursor.execute(cmd, val)
            c.commit()

    @classmethod
    def delete_by_id(cls, id_) -> None:
        """Delete a row from the database by id
        """
        cmd = "DELETE FROM {} WHERE {} = %s".format(cls.table_name, cls.id_name)
        val = (id_, )

        with cls._create_connection() as c:
            with c.cursor() as cursor:
                cursor.execute(cmd, val)
            c.commit()

    @classmethod
    def _get_single_by_query(cls, cmd, val):
        with cls._create_connection() as c:
            with c.cursor(dictionary=True) as cursor:
                cursor.execute(cmd, val)

                info = cursor.fetchall()
                assert len(info) <= 1

                # I.e. we couldn't find any payment
                if len(info) == 0:
                    return None 

                info = info[0]

        single = cls.class_.from_dict(info)

        return single

class TransactionDBManager(PaymentsDBManager):
    table_name = "payments.transactions"
    table_cols = ["user_id", "payment_id", "item_id", "money", "quantity"]
    id_name = "transaction_id"
    class_ = Transaction

    @classmethod
    def get_transaction(cls, transaction_id: TransactionID) -> Optional[Transaction]:
        cmd = "SELECT * FROM {} WHERE {} = %s".format(cls.table_name, cls.id_name)
        val = (transaction_id, )
        
        transaction = cls._get_single_by_query(cmd, val)
        return transaction

    @classmethod
    def get_transactions_by_user_id(cls, user_id: UserID) -> Sequence[Transaction]:
        cmd = "SELECT * FROM {} WHERE {} = %s".format(cls.table_name, 'user_id')
        val = (user_id,)

        with cls._create_connection() as c:
            with c.cursor(dictionary=True) as cursor:
                cursor.execute(cmd, val)

                info = cursor.fetchall()

        transactions = [cls.class_.from_dict(i) for i in info]

        return transactions

class PaymentCardsDBManager(PaymentsDBManager):
    table_name = "payments"
    table_cols = ["user_id", "card_number", "security_code", "expiration_date"]
    id_name = "payment_id"
    class_ = PaymentCard


    @classmethod
    def get_payment_card(cls, payment_id: PaymentID) -> Optional[PaymentCard]:
        """Get the payment from the database by payment id

        Returns:
            payment_card: Returns `None` if we couldn't find the payment. Otherwise, return the payment card.
        """
        cmd = "SELECT * FROM {} WHERE {} = %s".format(cls.table_name, cls.id_name)
        val = (payment_id, )
        
        payment_card = cls._get_single_by_query(cmd, val)
        return payment_card

    @classmethod
    def get_payment_card_by_user_id(cls, user_id: UserID) -> Optional[PaymentCard]:
        """Get the payment from the database by user id

        Returns:
            payment_card: Returns `None` if we couldn't find the payment. Otherwise, return the payment card.
        """
        cmd = "SELECT * FROM {} WHERE user_id = %s".format(cls.table_name)
        val = (user_id, )
        
        payment_card = cls._get_single_by_query(cmd, val)
        return payment_card

def create_payment_card(payment_info: PaymentInfo):
    """Create a payment card.
    """

    # check if user id doesn't have a payment card
    user_id = payment_info['user_id']
    payment_card = PaymentCardsDBManager.get_payment_card_by_user_id(user_id)
    if payment_card is not None:
        raise BadInputError('User {} already has a payment card.'.format(user_id))

    # payment_card = PaymentCard.from_dict(payment_info)
    # payment_info = payment_card.to_dict()
    row = [payment_info[c] for c in PaymentCardsDBManager.table_cols]
    PaymentCardsDBManager.insert(row)

    payment_card = PaymentCardsDBManager.get_payment_card_by_user_id(user_id)

    return payment_card.to_json()

def get_payment_card(payment_id: PaymentID):
    payment_card = PaymentCardsDBManager.get_payment_card(payment_id)
    if payment_card is None:
        raise BadInputError('There is no payment information for payment id: {}'.format(payment_id))

    return payment_card.to_json()

def get_payment_card_by_user_id(user_id: UserID):
    payment_card = PaymentCardsDBManager.get_payment_card_by_user_id(user_id)
    if payment_card is None:
        raise BadInputError('There is no payment information for user id: {}'.format(user_id))

    return payment_card.to_json()

def delete_payment_card(payment_id: PaymentID) -> None:
    payment_card = PaymentCardsDBManager.get_payment_card(payment_id)
    if payment_card is None:
        raise BadInputError('There is no payment information for payment id: {}'.format(payment_id))

    PaymentCardsDBManager.delete_by_id(payment_id)

    return payment_card.to_json()

def create_transaction(transaction_info):
    rows = [transaction_info[c] for c in TransactionDBManager.table_cols]
    
    transaction_id = TransactionDBManager.insert(rows)

    transaction = TransactionDBManager.get_transaction(transaction_id)
    return transaction.to_json()

def get_transaction(transaction_id):
    transaction = TransactionDBManager.get_transaction(transaction_id)

    if transaction is None:
        raise BadInputError('There is no transaction information for transaction id: {}'.format(transaction_id))

    return transaction.to_json()

def get_transactions_by_user_id(user_id):
    transactions = TransactionDBManager.get_transactions_by_user_id(user_id)
    transactions_dict = [t.to_dict() for t in transactions]
    return json.dumps(transactions_dict)


def delete_transaction(transaction_id):
    transaction = TransactionDBManager.get_transaction(transaction_id)

    if transaction is None:
        raise BadInputError('There is no transaction information for transaction id: {}'.format(transaction_id))

    TransactionDBManager.delete_by_id(transaction_id)

    return transaction.to_json()

