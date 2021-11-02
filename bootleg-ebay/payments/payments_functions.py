from typing import Dict, Any, Sequence, Optional

from mysql.connector import connect, Error

from payments import PaymentCard

PaymentInfo = Dict[str, Any]
PaymentID = int

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
        cmd = "UPDATE {} SET {} WHERE id = %s".format(cls.db_name, set_cmd)

        val = [payment_info[c] for c in cls.db_cols]
        with cls._create_connection() as c:
            with c.cursor() as cursor:
                cursor.execute(cmd, val)
            c.commit()

    @classmethod
    def delete_by_id(cls, payment_id: PaymentID) -> None:
        """Delete a row from the database by payment id
        """
        cmd = "DELETE FROM {} WHERE id = %s".format(cls.db_name)
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
        cmd = "SELECT * FROM {} WHERE id = %s".format(cls.db_name)
        val = (payment_id, )
        
        payment_card = cls._get_payment_by_query(cmd, val)
        return payment_card
