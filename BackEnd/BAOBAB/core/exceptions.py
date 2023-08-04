from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
    # 1.
    response = exception_handler(exc, context)
    
    # 2.
    handlers = {
        'ValidationError': _handle_generic_error
    }
    
    # 3.
    exception_class = exc.__class__.__name__

    # 4.
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
	# 5.
    return response

# 6.
def _handle_generic_error(exc, context, response):
    response.data = {
        'errors': response.data
    }

    return response