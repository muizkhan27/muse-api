def get_tenant_from_request(request):
    hostname = request.get_host().split(':')[0].lower()
    db = hostname.split('.')[0]
    return db
