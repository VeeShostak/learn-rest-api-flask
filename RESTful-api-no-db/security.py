from werkzeug.security import safe_str_cmp
from user import User

# in memory table with registered users
users = [
    User(1, 'bob', 'poiu'),
    User(2, 'mary', 'abc'),
]

# use set comprehension to assign key value pairs
username_table = {u.username: u for u in users}
# username_table = { 'bob': {
# 		'id': 1,
# 		'username': 'bob',
# 		'password': 'poiu'
# 	}
# }

# use set comprehension to assign key value pairs
userid_table = {u.id: u for u in users}
# userid_table = { 1: {
# 		'id': 1,
# 		'username': 'bob',
# 		'password': 'poiu'
# 	}
# }

def authenticate(username, password):
	# access dictionary with .get()
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password, password):
    	# if user exists and passwords match for that user
        return user

# param: payload is the contents of the jwt toekn
def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)
