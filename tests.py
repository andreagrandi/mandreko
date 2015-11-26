import pytest
from mock import patch
from nameko.testing.services import entrypoint_hook
from paymentservice import PaymentConsumer


@patch('mandrill.Messages.send_template')
def test_payment_consumer_send_email_on_event(
        send_template, container_factory, rabbit_config):
    container = container_factory(PaymentConsumer, rabbit_config)
    container.start()

    with entrypoint_hook(container, 'handle_event', None) as hook:
        payload = {
            'client': {
                'name': 'Jon Doe',
                'email': 'jon@doe.com'
            },
            'payee': {
                'name': 'Justin Case',
                'email': 'jc@email.com'
            },
            'payment': {
                'amount': 10000,
                'currency': 'GBP'
            }
        }

        hook(payload)

        send_template.assert_called_with(
            async=False,
            message={
                'global_merge_vars': [
                    {'content': 'Justin Case', 'name': 'payee'},
                    {'content': 10000, 'name': 'amount'},
                    {'content': 'GBP', 'name': 'currency'},
                    {'content': 'Jon Doe', 'name': 'client'},
                    {'content': 'jon@doe.com', 'name': 'email'}],
                'to': [
                    {
                        'type': 'to',
                        'email': 'jc@email.com',
                        'name': 'Justin Case'}],
                'subject': 'Payment Confirmation',
                'from_email': 'info@student.com'},
            template_content=[],
            template_name='payment-message')
