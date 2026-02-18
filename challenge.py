import re
import unittest
import uuid


class UsernameException(Exception):
    pass


class PaymentException(Exception):
    pass


class CreditCardException(Exception):
    pass


class Payment:

    def __init__(self, amount, actor, target, note):
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.actor = actor
        self.target = target
        self.note = note

class User:

    def __init__(self, username):
        self.credit_card_number = None
        self.balance = 0.0

        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException('Username not valid.')


    def retrieve_feed(self):
        return self.feed

    def add_friend(self, new_friend):
        if new_friend and self.friends:
            self.friends.append(new_friend)
        else:
            self.friends = [new_friend]

        return self.friends

    def add_to_balance(self, amount):
        self.balance += float(amount)

    def add_credit_card(self, credit_card_number):
        if self.credit_card_number is not None:
            raise CreditCardException('Only one credit card per user!')

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number

        else:
            raise CreditCardException('Invalid credit card number.')

    def pay(self, target, amount, note):
        amount = float(amount)
        self.feed = Feed(self)

        if self.username == target.username:
            raise PaymentException('User cannot pay themselves.')
        elif amount <= 0.0:
            raise PaymentException('Amount must be a non-negative number.')
        elif self.credit_card_number is None:
            raise PaymentException('Must have a credit card to make a payment.')
        elif self.balance >= amount: # if balance is enough to cover the payment, use balance
            return self.pay_with_balance(target, amount, note)
        else:  # if there is not enough balance we pay with credit card
            return self.pay_with_card(target, amount, note)
        

    def pay_with_card(self, target, amount, note):
        self._charge_credit_card(self.credit_card_number)
        payment = Payment(amount, self, target, note)
        target.add_to_balance(amount)
        self.feed.save_feed(target.username, payment)

        return payment

    def pay_with_balance(self, target, amount, note):
        payment = Payment(amount, self, target, note)
        self.balance -= amount
        self.feed.save_feed(target.username, payment)

        return payment

    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match('^[A-Za-z0-9_\\-]{4,15}$', username)

    def _charge_credit_card(self, credit_card_number):
        # magic method that charges a credit card thru the card processor
        pass

class Feed:

    def __init__(self, user):
        self.user = user

    def save_feed(self, receiver, payment):
        self.sender = self.user.username
        self.receiver = receiver
        self.payment = payment

    def __str__(self):
        return f'{self.sender} paid {self.receiver} ${self.payment.amount:.2f} for {self.payment.note}'

class MiniVenmo:
    def create_user(self, username, balance, credit_card_number):
        User = User(username)
        User.add_to_balance(balance)
        User.add_credit_card(credit_card_number)
        return User

    def render_feed(self, feed):
        return print(feed)

    @classmethod
    def run(cls):
        venmo = cls()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")

        try:
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")
 
            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")
        except PaymentException as e:
            print(e)

        feed = bobby.retrieve_feed()
        venmo.render_feed(feed)

        bobby.add_friend(carol)


class TestUser(unittest.TestCase):

    def test_this_works(self):
        with self.assertRaises(UsernameException):
            raise UsernameException()
        
    def test_create_user(self):
        user = User("Bruce Wayne")
        user.add_to_balance(1000000.0)
        user.add_credit_card("4111-1111-1111-1111")

        assert user.username == "Bruce Wayne"
        assert user.balance == 1000000.0
        assert user.credit_card_number == "4111-1111-1111-1111"


if __name__ == '__main__':
    unittest.main()
