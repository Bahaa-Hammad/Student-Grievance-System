from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

# six.text_type: Type for representing(Unicode) textual data.


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, account, timestamp):
        return (
            six.text_type(account.pk) + six.text_type(timestamp) +
            six.text_type(account.email_confirmed)
        )



account_activation_token = AccountActivationTokenGenerator()
