#################
#  C O N F I G  #
#################
DEBUG = False

SECRET_KEY = '4001628bb0b22cefcxc6dfde280ba000'
SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

# These are used in integration with the below services. #
INT_USER = "INT_ADMIN"
INT_PASS = "hX82ZilTgalkpqkd6dyp"

# Services (docker images ran and bound to different ports.)
SERVICE_ADDRESSES = {
    # 'auth':'http://127.0.0.1:601',
    # 'opp':'http://127.0.0.1:602',
    # 'prod':'http://127.0.0.1:603',
    # 'doc':'http://127.0.0.1:604'
    'auth':'http://host.docker.internal:601',
    'opp':'http://host.docker.internal:602',
    'prod':'http://host.docker.internal:603',
    'doc':'http://host.docker.internal:604'
}

# Default Contract Term Value for a new opportunity.
DEFAULT_CONTRACT_TERM = 36