from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

# six.text_type: Type for representing(Unicode) textual data.


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.email_confirmed)
        )


class EmailResetToken(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(user.email_reset) + six.text_type(timestamp)
        )


account_activation_token = AccountActivationTokenGenerator()
email_reset_token = EmailResetToken()
