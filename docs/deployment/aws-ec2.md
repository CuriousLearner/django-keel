# AWS EC2 Deployment

Deploy Django Keel projects to AWS EC2 with Ansible.

## Prerequisites

- AWS account with EC2 access
- Ansible installed
- SSH key pair configured

## Setup

### 1. Configure Inventory

```bash
cd deploy/ansible
cp inventory/hosts.example inventory/hosts
# Edit with your EC2 instance details
```

### 2. Configure Variables

```bash
cp group_vars/all.yml.example group_vars/all.yml
# Update with your settings
```

### 3. Initial Provisioning

```bash
ansible-playbook -i inventory/hosts playbooks/setup.yml
```

This installs:

- Python, PostgreSQL, Redis
- Caddy reverse proxy
- Systemd service files

### 4. Deploy Application

```bash
ansible-playbook -i inventory/hosts playbooks/deploy.yml
```

## Features

- **Caddy** with automatic HTTPS
- **Systemd** for service management
- **Zero-downtime** deployments
- **Automatic rollback** on failure
- **Database backups** configuration

## Updating

```bash
# Deploy new version
ansible-playbook -i inventory/hosts playbooks/deploy.yml --extra-vars "version=v1.1.0"
```

## Rollback

```bash
ansible-playbook -i inventory/hosts playbooks/rollback.yml
```
