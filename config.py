### Global variables ###

CURL_ROOT = "curl"

# URL configuration #
URL_ROOT = "https://dev.chillingeffects.org/notices/"
SEARCH_SUFFIX = "search?"
#

# File configuration #
FILE_ROOT = os.environ["HOME"] + "chillingtools/files/"

# Optional caching #
CACHE_BOOL = True
CACHE_ROOT = ""
if CACHE_BOOL:
    CACHE_ROOT = FILE_ROOT + "cache/"
#

###

DEFAULT_FLAGS = ['-k']
