def create_log_extra(request_id, **kwargs):
    extra = {}
    if request_id:
        extra['request_id'] = request_id
    extra.update(kwargs)
    return extra

