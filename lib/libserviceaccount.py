from charmhelpers import layer
from charmhelpers.core import fetch
from charmhelpers.core.hookenv import (
    status_set,
    log
)
from subprocess import check_call

class ServiceAccountHelper():
    def __init__(self):
        self.charm_config = hookenv.config()
        self.layer_config = dict(layer.options('service-account'))
        self.accounts = []
        self.system_passwd = []
        self.system_groups = []
        self.passwd_path = '/etc/passwd'
        self.groups_path = '/etc/groups'

    def install_deps(self):
        fetch.apt_install('passwd')

    def parse_passwd(self):
        passwd_file = open(self.passwd_path, 'r')
        users = []
        for entry in passwd_file:
            user = {}
            fields = entry.strip().split(':')
            user['name'] = fields[0]
            user['id'] = fields[2]
            users.extend(user)
        self.system_passwd = users

    def parse_groups(self):
        groups_file = open(self.groups_path, 'r')
        groups = []
        for entry in groups_file:
            group = {}
            fields = entry.strip().split(':')
            group['name'] = fields[0]
            group['id'] = fields[2]
            group['members'] = fields[3].split(',')
            groups.extend(user)
        self.system_groups = groups

    def check_user_exists(self, user):
        self.parse_passwd()
        for user in self.system_passwd:
            if user['name'] == user:
                return True
        return False

    def set_uid(self, user, uid):
        try:
            check_call(['usermod', '-u', uid, user])
        except CalledProcessError as e:
            status_set('ERROR',
                       'Invalid or in-use UID {} for user {} provided'.format(
                           uid,
                           user
                       ))
            log('Invalid or in-use UID {} for account {}: {}'.format(
                    uid,
                    user,
                    e['message']),
                'ERROR'
            )
        else:
            log(
                'Set UID {} for account {}'.format(uid, user),
                'DEBUG'
            )

    
    def check_uid_conflict(self, user, uid):
        self.parse_passwd()
        for user in self.system_passwd:
            if user['id'] == uid:
                if user['name'] == user:
                    return False
                else:
                    return True
        return False

    def check_group_exists(self, group):
        self.parse_groups()
        for group in self.system_groups:
            if group['name'] == group:
                return True
        return False

    def check_gid_conflict(self, group, gid):
        self.parse_groups()
        for group in self.system_groups:
            if group['id'] == uid:
                if group['name'] == group:
                    return False
                else:
                    return True
        return False
    
    def set_gid(self, user, gid):
        try:
            check_call(['groupmod', '-g', gid, group])
        except CalledProcessError as e:
            status_set('ERROR',
                       'Invalid or in-use GID {} for group {} provided'.format(
                           gid,
                           group
                       ))
            log('Invalid or in-use GID {} for group {}: {}'.format(
                    gid,
                    group,
                    e['message']),
                'ERROR'
            )
        else:
            log(
                'Set GID {} for group {}'.format(gid, group),
                'DEBUG'
            )

    def check_member_of_group(self, user, group):
        self.parse_groups()
        self.parse_passwd()
        group = {}
        for group_entry in self.groups:
            if group['name'] == group:
                if name in group['members']:
                    return True
        return False

    def add_group_member(self, group, user):
        try:
            check_call(['usermod', '-A', '-G', group, user])
        except CalledProcessError as e:
            status_set('ERROR',
                       'Invalid group {} being added for user {}'.format(
                           group,
                           user
                       ))
            log('Invalid group {} being added for user {}: {}'.format(
                    group,
                    user,
                    e['message']),
                'ERROR'
            )
        else:
            log(
                'Added group {} for user {}'.format(group, user),
                'DEBUG'
            )
        

    def build_config(self):
        # read account list
        # this is comma separated
        config_users = self.charm_config['system-additional-users']
        layer_users = self.layer_config['users']
        users = []
        if config_users:
            users.append(config_users.split(','))
        if layer_users:
            users.append(layer_users)

        # read UID mapping
        # this is comma separated, user=uid format
        user_mapping = {}
        config_uidmap = self.charm_config['system-uidmap']
        layer_uidmap = self.layer_config['uidmap']
        if config_uidmap:
            uidmappings = config_uidmap.split(',')
            for uidmapping in uidmappings:
                if '=' in uidmapping:
                    user, uid = uidmapping.split('=')
                    user_mapping[user] = uid
        if layer_uidmap:
            for user, uid in layer_uidmap:
                user_mapping[user] = uid

        # read group list
        # this is comma separated
        config_groups = self.charm_config['system-aditional-groups']
        layer_groups = self.layer_config['groups']
        groups = []
        if config_groups:
            users.append(config_groups.split(','))
        if layer_groups:
            users.append(layer_groups)

        # read GID mapping
        # this is comma separated, group=gid format
        group_mapping = {}
        config_gidmap = self.charm_config['system-gidmap']
        layer_gidmap = self.layer_config['gidmap']
        if config_gidmap:
            gidmappings = config_gidmap.split(',')
            for gidmapping in gidmappings:
                if '=' in gidmapping:
                    group, gid = gidmapping.split('=')
                    group_mapping[group] = gid
        if layer_gidmap:
            for group, gid in layer_gidmap:
                group_mapping[group] = gid

        # add memberships to groups
        # this is comma separated, with mapping between group and a list of users
        # the group and list are separated by '='
        # the list of users to ensure are in the group are separated by ':'
        config_membership = self.charm_config['system-group-membership']
        layer_membership = self.layer_config['membership']


    def process_user_accounts(self):

    def process_groups(self):

    def process_group_membership(self):

    def apply_config(self):
        # loop over account and ensure they exist with correct UIDs
        self.process_user_accounts()
        # loop over groups and ensure they exist with correct GIDs
        self.process_groups()
        # loop over memberships, and add users to groups if missing
        self.process_group_membership()

    def update_accounts(self):
        ''' Idempotently configure service accounts and groups '''
        # build current state dictionaries
        self.parse_groups()
        self.parse_passwd()
        # build dictionary of desired state
        self.build_config()
        # apply configuration
        self.apply_config()
        return
