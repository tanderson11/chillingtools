import json

### Custom handler functions ###

#def custom_handler():

# Default handlers #

def default_download_handler(response):
    return json.loads(response)

def default_search_handler(response):
    return json.loads(response)

DOWNLOAD_HANDLER = default_download_handler
SEARCH_HANDLER = default_search_handler

### Custom search paramaters ###

#Param(name_string, description_string, require_all_boolean)


###
