from rest_framework_simplejwt.tokens import RefreshToken

def generate_jwt_for_user(user):
    """
    Returns refresh + access token pair for a user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

