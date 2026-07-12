# AWS EC2 Deployment

Deploy Django Keel projects to AWS EC2 with Ansible.

## What's Generated

```
deploy/ansible/
├── playbooks/
│   └── deploy.yml                     # Server setup + app deployment
├── templates/
│   ├── Caddyfile.j2                   # Caddy reverse proxy config
│   └── <project_slug>.service.j2      # systemd unit for the app
└── README.md
```

## Prerequisites

- AWS account with EC2 access
- An EC2 instance (Ubuntu/Debian) reachable over SSH
- Ansible installed locally
- SSH key pair configured

## Setup

### 1. Create an Inventory

Point Ansible at your instance with a `webservers` group (the playbook targets `hosts: webservers`):

```ini
# inventory/hosts
[webservers]
your-ec2-host.example.com ansible_user=ubuntu
```

### 2. Deploy

The single `deploy.yml` playbook provisions and deploys in one run - it installs system packages (Python, PostgreSQL client, Caddy, git), creates the app user, clones your repository, installs dependencies, runs migrations and `collectstatic`, and configures Caddy and the systemd service:

```bash
ansible-playbook -i inventory/hosts playbooks/deploy.yml \
  --extra-vars "git_repo=git@github.com:you/your-project.git"
```

Use `--extra-vars "git_branch=..."` to deploy a branch other than `main`.

## Features

- **Caddy** with automatic HTTPS
- **systemd** for service management (restart on deploy via handlers)
- Repository-based deploys - re-run the playbook to update

## Updating

```bash
# Deploy the latest code from your branch
ansible-playbook -i inventory/hosts playbooks/deploy.yml \
  --extra-vars "git_repo=git@github.com:you/your-project.git git_branch=main"
```

## Rollback

There is no automated rollback playbook. To roll back, re-run `deploy.yml` with `git_branch` (or a tag) pointing at the last known-good revision.
