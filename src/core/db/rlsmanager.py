from config import settings
from django.contrib.auth.models import User
import os
import core.db.connection


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


class RowLevelSecurityManager:

    def __init__(self, user, table, repo, repo_base):
        if user != 'dh_public' and user != 'postgres':
            user = User.objects.get(username=user)
            self.username = user.username
        else:
            self.username = user

        self.repo_base = repo_base
        self.repo = repo
        self.table = table

        self.user_con = core.db.connection.DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'],
            repo_base='dh_public')

    def add_security_policy(self, policy, policy_type, grantee):
        '''
        Creates a new security policy in the policy table. First, we check
        whether this policy exists in the table. If so, return an error.
        Otherwise, create the policy.
        '''
        return self.user_con.create_security_policy(
            policy, policy_type, grantee, self.username, self.table,
            self.repo, self.repo_base)

    def list_security_policies(self):
        '''
        Returns a list of all the security policies defined on the table.
        '''
        return self.user_con.list_security_policies(
            self.table, self.repo, self.repo_base)

    def find_security_policy(self, policy_id=None, policy=None,
                             policy_type=None, grantee=None, grantor=None):
        '''
        Looks for security policies matching what the user specified in
        the input.
        '''
        return self.user_con.find_security_policy(
            self.table, self.repo, self.repo_base, policy_id, policy,
            policy_type, grantee, grantor)

    def find_security_policy_by_id(self, policy_id):
        '''
        Looks for a security policy matching the specified policy_id.
        '''
        return self.user_con.find_security_policy_by_id(policy_id)

    def update_security_policy(self, policy_id, new_policy, new_policy_type,
                               new_grantee):
        '''
        Updates the existing security policy with the specified inputs.
        '''
        return self.user_con.update_security_policy(
            policy_id, new_policy, new_policy_type, new_grantee)

    def remove_security_policy(self, policy_id):
        '''
        Removes the security policy specified by the policy_id.
        '''
        return self.user_con.remove_security_policy(policy_id)
