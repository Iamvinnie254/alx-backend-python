from itertools import islice
from stream_users import stream_users


for user in islice(stream_users(), 6):
    print(user)
