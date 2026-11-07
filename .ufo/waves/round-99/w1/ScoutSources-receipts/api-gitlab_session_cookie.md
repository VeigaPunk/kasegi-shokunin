# GitLab session cookie

## Description

A GitLab session cookie was identified. The `_gitlab_session` cookie identifies a signed-in browser session.
The value is a 64-character hexadecimal session ID, with an optional `cell-<ID>-` prefix.

A malicious actor with access to this cookie can use GitLab as the authenticated user until the session ends.

## Remediation

For general guidance on handling security incidents with regards to leaked keys, see the GitLab documentation on
[Credential exposure to the internet](https://docs.gitlab.com/ee/security/responding_to_security_incidents.html#credential-exposure-to-public-internet).

To revoke the session:

1. In the upper-right corner, select your avatar.
1. Select **Edit profile**.
1. In the left sidebar, select **Access** > **Active sessions**.
1. By the session, select **Revoke**.

You cannot revoke the session that you use now. To end it, sign out. For more information, see
[Revoke a session](https://docs.gitlab.com/user/profile/active_sessions/#revoke-a-session).
