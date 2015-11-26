import mandrill
import os


def send_payment_email(payload):
    try:
        """
            Dear *|payee|*,

            You have received a payment of *|amount|* *|currency|* from *|client|* (*|email|*).

            Yours,
            student.com
        """

        MANDRILL_API_KEY = os.environ.get('MANDRILL_API_KEY')
        mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)

        template_content = []

        message = {
            'from_email': 'info@student.com',
            'subject': 'Payment Confirmation',
            'to': [{'email': payload['payee']['email'],
                    'name': payload['payee']['name'],
                    'type': 'to'}],
            'global_merge_vars': [
                {
                    'name': 'payee',
                    'content': payload['payee']['name']},
                {
                    'name': 'amount',
                    'content': payload['payment']['amount']},
                {
                    'name': 'currency',
                    'content': payload['payment']['currency']},
                {
                    'name': 'client',
                    'content': payload['client']['name']},
                {
                    'name': 'email',
                    'content': payload['client']['email']}
            ]
        }

        result = mandrill_client.messages.send_template(
            template_name='payment-message',
            template_content=template_content,
            message=message,
            async=False)

    except mandrill.Error, e:
        print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
        raise
