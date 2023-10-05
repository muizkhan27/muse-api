from drf_yasg import openapi


refresh_token_parameter = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Enter refresh token...'), })

tax_return_file_parameter = [
    openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Upload tax return pdf...'),
]
