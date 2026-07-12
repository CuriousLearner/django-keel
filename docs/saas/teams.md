# 🏢 Teams & Organizations

Full multi-tenancy with role-based access control for Django Keel SaaS projects.

## Overview

The Teams app provides:

- **Multi-tenant data isolation** - Each team has separate data
- **Role-Based Access Control (RBAC)** - Owner, Admin, Member roles
- **Team Invitations** - Email-based with secure tokens
- **Per-Seat Billing** - Automatic Stripe subscription quantity updates

## Models

### Team

```python
class Team(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Methods:**
- `get_member_count()` - Active members count
- `get_active_members()` - Queryset of active memberships
- `has_member(user)` - Check membership
- `add_user(user, role, added_by)` - Add team member

### TeamMember

```python
class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    joined_at = models.DateTimeField(auto_now_add=True)
```

**Roles:**
- `owner` - Full control, can delete team, manage billing
- `admin` - Manage members, can't delete team or change billing
- `member` - Read/write access, can't manage team

**Methods:**
- `is_owner()` - Check if owner
- `is_admin()` - Check if admin or owner
- `can_manage_members()` - Check if can add/remove members

### TeamInvitation

```python
class TeamInvitation(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True, editable=False)
    status = models.CharField(max_length=20, default='pending')
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
```

The token is generated on save with `secrets.token_urlsafe(32)`, and `expires_at` defaults to 7 days from creation.

**Methods:**
- `is_valid()` - Check if still pending and not expired
- `accept(user)` - Accept invitation and create membership
- `decline()` - Decline invitation
- `send_invitation_email()` - Send invite email

## Usage

### Create Team

```python
from apps.teams.models import Team, TeamMember

# Create team
team = Team.objects.create(
    name="Acme Corp",
    slug="acme-corp",
    owner=request.user
)

# Owner membership is auto-created via signal
# But you can also create manually:
TeamMember.objects.create(
    team=team,
    user=request.user,
    role="owner",
    added_by=request.user
)
```

### Invite Member

```python
from apps.teams.models import TeamInvitation
from datetime import timedelta
from django.utils import timezone

invitation = TeamInvitation.objects.create(
    team=team,
    email="colleague@example.com",
    role="member",
    invited_by=request.user,
    # token and expires_at (7 days) are set automatically on save
)

# Send invitation email
invitation.send_invitation_email()
```

### Accept Invitation

```python
# User clicks link with token
invitation = TeamInvitation.objects.get(token=token)

if invitation.is_valid():
    invitation.accept(request.user)
    # Now user is a team member!
```

### Check Membership

```python
if team.has_member(request.user):
    # User is a member
    pass

# Or get membership
membership = TeamMember.objects.filter(
    team=team,
    user=request.user,
    is_active=True
).first()

if membership and membership.is_admin():
    # User is admin or owner
    pass
```

## Views & Permissions

### Require Team Membership

The mixins resolve the team from the `team_slug` URL kwarg and set `self.team` and `self.team_member` on the view:

```python
from django.views.generic import ListView
from apps.teams.permissions import TeamMemberRequiredMixin

# URL pattern must include <slug:team_slug>
class ProjectListView(TeamMemberRequiredMixin, ListView):
    model = Project

    def get_queryset(self):
        # Filtered to the team from the URL
        return super().get_queryset().filter(team=self.team)
```

### Require Admin Role

```python
from apps.teams.permissions import TeamAdminRequiredMixin

class MemberManageView(TeamAdminRequiredMixin, UpdateView):
    model = TeamMember
    # Only admins and owners can access
```

### Require Owner Role

```python
from apps.teams.permissions import TeamOwnerRequiredMixin

class TeamDeleteView(TeamOwnerRequiredMixin, DeleteView):
    model = Team
    # Only owner can delete team
```

## Signals

Django Keel includes automatic signal handlers:

**On Team Creation:**
- Auto-create owner membership

**On Member Addition (with Stripe advanced mode):**
- Update Stripe subscription quantity for per-seat billing

**On Member Removal:**
- Update Stripe subscription quantity

## URL Patterns

```python
# Teams
/teams/                                # List teams
/teams/create/                         # Create team
/teams/<team_slug>/                    # Team detail (includes member list)
/teams/<team_slug>/edit/               # Edit team
/teams/<team_slug>/delete/             # Delete team

# Members
/teams/<team_slug>/members/<member_id>/edit/    # Edit member role
/teams/<team_slug>/members/<member_id>/remove/  # Remove member
/teams/<team_slug>/leave/                       # Leave team

# Invitations
/teams/<team_slug>/invite/             # Invite member
/teams/invitations/<token>/accept/     # Accept invitation
/teams/invitations/<token>/decline/    # Decline invitation
```

## Templates

Django Keel provides base templates you can customize:

```
templates/teams/
├── team_list.html
├── team_form.html
├── team_detail.html
├── team_confirm_delete.html
├── invitation_form.html
├── member_form.html
└── emails/
    ├── invitation.txt
    └── invitation.html
```

## Testing

```python
# tests/teams/test_models.py
def test_team_creation(user):
    team = Team.objects.create(
        name="Test Team",
        slug="test-team",
        owner=user
    )
    assert team.get_member_count() == 1  # Owner auto-added

def test_add_member(user, team):
    new_user = User.objects.create_user(
        email="new@example.com",
        password="testpass123"
    )
    team.add_user(new_user, role="member", added_by=user)
    assert team.has_member(new_user)
```

## Best Practices

1. **Always check team membership** before showing data
2. **Use mixins** for permission checks
3. **Filter querysets** by team
4. **Log team actions** for audit trail
5. **Handle member limits** based on subscription
6. **Send email notifications** for invitations
7. **Clean up expired invitations** periodically

## Next Steps

- [Stripe Integration](stripe.md) - Per-seat billing
- [Feature Gating](feature-gating.md) - Access control by plan
- [User Impersonation](impersonation.md) - Support tools
