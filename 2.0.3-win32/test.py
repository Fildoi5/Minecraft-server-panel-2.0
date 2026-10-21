from pwd import getpwnam
from grp import getgrnam

print(getpwnam('user_name').pw_uid) # Returns UID only
print(getgrnam('group_name').gr_gid) # Returns GID only