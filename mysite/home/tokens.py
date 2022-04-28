from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user['username']) + text_type(timestamp) +
            text_type(user['email'])
        )
account_activation_token = TokenGenerator()