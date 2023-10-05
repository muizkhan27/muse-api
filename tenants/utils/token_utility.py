from datetime import datetime, timedelta

import jwt
from django.conf import settings


def generate_access_token(tenant_id):
    access_token_payload = {
      'tenant_id': tenant_id,
      'exp': datetime.utcnow() + timedelta(days=1),
      'iat': datetime.utcnow()
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return access_token


def generate_refresh_token(tenant_id):
    refresh_token_payload = {
      'tenant_id': tenant_id,
      'exp': datetime.utcnow() + timedelta(days=15),
      'iat': datetime.utcnow()
    }
    refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return refresh_token
