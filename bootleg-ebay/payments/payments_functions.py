from typing import Dict, Any, Sequence, Optional
import json

from mysql.connector import connect, Error

from payments import PaymentCard, BadInputError

PaymentInfo = Dict[str, Any]
PaymentID = int
UserID = int

class PaymentsDBManager:
    db_name = "payments"
    db_cols = ["user_id", "card_number", "security_code", "expiration_date"]

    @classmethod
    def _create_connection(cls):
        connection = connect(
            host="payments-db",
            port="3306",
            user="%s" % ("root"),
            password="%s" % ("bootleg2"),
            database=cls.db_name,
        )
        return connection

    @classmethod
    def insert_many(cls, data: Sequence):
        """Insert many rows into payments database.

        Args: 
            data: List of rows to be inserted
        """
        cmd = "INSERT INTO {} ({}) VALUES (%s, %s, %s, %s)".format(
            cls.db_name, 
            ', '.join(cls.db_cols))

        with cls._create_connection() as c:
            with c.cursor() as cursor:
                cursor.executemany(cmd, data)
            c.commit()
    
    @classmethod
    def update_by_id(cls, payment_info: PaymentInfo) -> None:
        """Update the database by id
        """
        set_cmd = ["{} = %s".format(c) for c in cls.db_cols]
        set_cmd = ", ".join(set_cmd)
        cmd = "UPDATE {} SET {} WHERE payment_id = %s".format(cls.db_name, set_cmd)

        val = [payment_info[c] for c in cls.db_cols]
        with cls._create_connection() as c:
            with c.cursor() as cursor:
                cursor.execute(cmd, val)
            c.commit()

    @classmethod
    def delete_by_id(cls, payment_id: PaymentID) -> None:
        """Delete a row from the database by payment id
        """
        cmd = "DELETE FROM {} WHERE payment_id = %s".format(cls.db_name)
        val = (payment_id, )

        with cls._create_connection() as c:
            with c.cursor() as cursor:
                cursor.execute(cmd, val)
            c.commit()

    @classmethod
    def _get_payment_by_query(cls, cmd, val):
        with cls._create_connection() as c:
            with c.cursor(dictionary=True) as cursor:
                cursor.execute(cmd, val)

                payment_info = cursor.fetchall()
                assert len(payment_info) <= 1

                # I.e. we couldn't find any payment
                if len(payment_info) == 0:
                    return None 

                payment_info = payment_info[0]


        payment = PaymentCard.from_dict(payment_info)

        return payment

    @classmethod
    def get_payment_card(cls, payment_id: PaymentID) -> Optional[PaymentCard]:
        """Get the payment from the database by payment id

        Returns:
            payment_card: Returns `None` if we couldn't find the payment. Otherwise, return the payment card.
        """
        cmd = "SELECT * FROM {} WHERE payment_id = %s".format(cls.db_name)
        val = (payment_id, )
        
        payment_card = cls._get_payment_by_query(cmd, val)
        return payment_card

    @classmethod
    def get_payment_card_by_user_id(cls, user_id: UserID) -> Optional[PaymentCard]:
        """Get the payment from the database by user id

        Returns:
            payment_card: Returns `None` if we couldn't find the payment. Otherwise, return the payment card.
        """
        cmd = "SELECT * FROM {} WHERE user_id = %s".format(cls.db_name)
        val = (user_id, )
        
        payment_card = cls._get_payment_by_query(cmd, val)
        return payment_card

def create_payment_card(payment_info: PaymentInfo):
    """Create a payment card.
    """

    # check if user id doesn't have a payment card
    user_id = payment_info['user_id']
    payment_card = PaymentsDBManager.get_payment_card_by_user_id(user_id)
    if payment_card is not None:
        raise BadInputError('User {} already has a payment card.'.format(user_id))

    # payment_card = PaymentCard.from_dict(payment_info)
    # payment_info = payment_card.to_dict()
    rows = [[payment_info[c] for c in PaymentsDBManager.db_cols]]
    PaymentsDBManager.insert_many(rows)

    payment_card = PaymentsDBManager.get_payment_card_by_user_id(user_id)

    return payment_card.to_json()

def get_payment_card(payment_id: PaymentID):
    payment_card = PaymentsDBManager.get_payment_card(payment_id)
    if payment_card is None:
        raise BadInputError('There is no payment information for payment id: {}'.format(payment_id))

    return payment_card.to_json()

def delete_account(payment_id: PaymentID) -> None:
    payment_card = PaymentsDBManager.get_payment_card(payment_id)
    if payment_card is None:
        raise BadInputError('There is no payment information for payment id: {}'.format(payment_id))

    PaymentsDBManager.delete_by_id(payment_id)

    return payment_card.to_json()
