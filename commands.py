from requests import *
from config import *



if __name__ == "__main__":
    directories_needed = [FILE_ROOT]
    if CACHE_BOOL:
        directories_needed.append(CACHE_ROOT)
    print "Checking directory structure."
    for d in directories_needed:
        if not os.path.exists(d):
            print "Building directory: " + d
            os.makedirs(d)
    # Define commands here
    pass
