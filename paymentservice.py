from faker import Factory
from nameko.events import EventDispatcher, event_handler
from nameko.timer import timer
from emails import send_payment_email

fake = Factory.create()


class PaymentService(object):
    name = "payments"

    dispatch = EventDispatcher()

    @timer(interval=5)
    def emit_event(self):

        payload = {
            'client': {
                'name': fake.name(),
                'email': fake.safe_email()
            },
            'payee': {
                'name': fake.name(),
                'email': fake.safe_email()
            },
            'payment': {
                'amount': fake.random_int(),
                'currency': fake.random_element(
                    ("USD", "GBP", "EUR")
                )
            }
        }
        self.dispatch("payment_received", payload)


class PaymentConsumer(object):
    """ Process the Payment messages. """
    name = "payments_consumer"

    @event_handler("payments", "payment_received")
    def handle_event(self, payload):
        print("payments_consumer received:", payload)
        send_payment_email(payload=payload)
