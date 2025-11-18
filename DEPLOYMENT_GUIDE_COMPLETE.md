# 🦫 Capibara6 Complete Deployment Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [VM Preparation](#vm-preparation)
4. [Deployment Steps](#deployment-steps)
5. [Post-Deployment Configuration](#post-deployment-configuration)
6. [Verification and Testing](#verification-and-testing)
7. [Troubleshooting](#troubleshooting)
8. [Maintenance](#maintenance)

## Overview

Capibara6 is a distributed AI system consisting of three primary VMs:

1. **Bounty2** (Model Server) - Ollama with GPT-OSS-20B and backend API
2. **Services VM** (TTS, MCP, N8N) - Auxiliary services
3. **RAG3** (RAG System) - Vector databases, knowledge graph, monitoring

This guide provides step-by-step instructions for deploying the complete system from scratch.

## Prerequisites

### Google Cloud Project Setup
- Active Google Cloud account with billing enabled
- Project with required APIs enabled:
  - Compute Engine API
  - Cloud Resource Manager API
- IAM permissions to create VMs, firewall rules, and other resources

### CLI Tools
- Google Cloud SDK (`gcloud`)
- Docker and Docker Compose
- Git

### Network Requirements
- Sufficient quota for 3 VMs with specified requirements
- Required ports available in your firewall

## VM Preparation

### Step 1: Create VMs

Follow the VM configuration requirements document to create the three VMs:

```bash
# Set your project ID
gcloud config set project mamba-001

# Create VMs (adjust the commands as per your requirements)
# Refer to VM_CONFIG_REQUIREMENTS.md for exact commands
```

### Step 2: Verify VM Creation

Verify that all VMs are created and accessible:

```bash
gcloud compute instances list --project="mamba-001"
```

Test SSH connectivity to each VM:

```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
```

### Step 3: Configure Firewall Rules

Set up the required firewall rules as specified in the VM configuration requirements.

## Deployment Steps

### Phase 1: Deploy RAG3 VM (Database and Monitoring Services)

1. **Connect to VM RAG3:**
```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
```

2. **Run the installation script for backend (RAG configuration):**
```bash
# Download the installation script
curl -O https://raw.githubusercontent.com/anachroni-co/capibara6/main/backend_install_script.sh

# Make it executable
chmod +x backend_install_script.sh

# Run with rag3 role
sudo ./backend_install_script.sh rag3
```

3. **Configure additional services specific to RAG3:**
```bash
cd /opt/capibara6
# Follow the RAG-specific setup instructions from the repo
```

### Phase 2: Deploy Bounty2 VM (Model Server)

1. **Connect to VM Bounty2:**
```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
```

2. **Run the installation script for backend (model configuration):**
```bash
# Download the installation script
curl -O https://raw.githubusercontent.com/anachroni-co/capibara6/main/backend_install_script.sh

# Make it executable
chmod +x backend_install_script.sh

# Run with bounty2 role
sudo ./backend_install_script.sh bounty2
```

3. **Download required models:**
```bash
# Wait for Ollama to start
sleep 10
ollama pull gpt-oss:20b
ollama pull phi3:mini
ollama pull llama2
```

### Phase 3: Deploy Services VM (TTS, MCP, N8N)

1. **Connect to VM Services:**
```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
```

2. **Run the installation script for backend (services configuration):**
```bash
# Download the installation script
curl -O https://raw.githubusercontent.com/anachroni-co/capibara6/main/backend_install_script.sh

# Make it executable
chmod +x backend_install_script.sh

# Run with services role
sudo ./backend_install_script.sh services
```

3. **Configure additional services as needed for TTS, MCP, N8N**

### Phase 4: Deploy Frontend

The frontend can be deployed on any VM or served locally for development. For production, it's typically served via the web components of the system.

1. **On any accessible VM or local machine:**
```bash
# Download the frontend installation script
curl -O https://raw.githubusercontent.com/anachroni-co/capibara6/main/frontend_install_script.sh

# Make it executable
chmod +x frontend_install_script.sh

# Run the frontend installation
sudo ./frontend_install_script.sh
```

## Post-Deployment Configuration

### Configure Service Endpoints

Update the service configuration files to point to the correct VM IPs:

1. **On Bounty2 VM**, update backend configuration:
```bash
# Edit the .env file in the backend directory
sudo nano /opt/capibara6/backend/.env

# Update with the correct IPs:
# SERVICES_VM_URL=http://[SERVICES_VM_IP_ADDRESS]
# RAG3_VM_URL=http://[RAG3_VM_INTERNAL_IP]
```

2. **On Services VM**, update service configuration:
```bash
# Update configuration to point to other VMs
sudo nano /opt/capibara6/backend/.env

# Update with the correct IPs:
# BOUNTY2_VM_URL=http://[BOUNTY2_VM_IP_ADDRESS]
# RAG3_VM_URL=http://[RAG3_VM_INTERNAL_IP]
```

### Configure Load Balancers (Optional)

For production deployments, consider setting up Google Cloud Load Balancers:

```bash
# Create a target pool for backend services
gcloud compute target-pools create capibara6-backend-pool \
    --project="mamba-001" \
    --region="europe-west4"

# Add instances to the pool
gcloud compute target-pools add-instances capibara6-backend-pool \
    --project="mamba-001" \
    --instances="bounty2" \
    --instances-zone="europe-west4-a"
```

### SSL/TLS Configuration (Optional)

For production deployments, configure SSL certificates:

```bash
# Create SSL certificate for your domain
gcloud compute ssl-certificates create capibara6-ssl-cert \
    --project="mamba-001" \
    --certificate="path/to/certificate.crt" \
    --private-key="path/to/private.key"
```

## Verification and Testing

### Service Health Checks

1. **Check backend services on each VM:**
```bash
# On Bounty2
sudo systemctl status capibara6-backend

# On Services VM
sudo systemctl status capibara6-backend

# On RAG3
sudo systemctl status capibara6-backend
```

2. **Test API endpoints:**
```bash
# On Bounty2 - test backend
curl http://localhost:5001/health

# On Services VM - test services
curl http://localhost:5002/health  # TTS
curl http://localhost:5003/api/mcp/health  # MCP

# On RAG3 - test RAG services
curl http://localhost:8000/health  # Bridge API
curl http://localhost:3000/api/health  # Grafana
```

3. **Test cross-VM connectivity:**
```bash
# From Bounty2, test connectivity to other VMs
ping [SERVICES_VM_IP]
curl http://[SERVICES_VM_IP]:5002/health

# From Services VM, test connectivity to other VMs
ping [BOUNTY2_IP]
curl http://[BOUNTY2_IP]:5001/health
```

### Application Testing

1. **Test the chat functionality:**
```bash
curl -X POST http://[BOUNTY2_IP]:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?", "email": "test@example.com"}'
```

2. **Check logs for any errors:**
```bash
# On each VM, check service logs
sudo journalctl -u capibara6-backend -f
```

### Performance Testing

1. **Load testing (optional):**
```bash
# Install and use load testing tools like apache bench
sudo apt-get install apache2-utils

# Test with multiple concurrent requests
ab -n 100 -c 10 http://[BOUNTY2_IP]:5001/api/chat
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Service Not Starting
```bash
# Check service status
sudo systemctl status capibara6-backend

# Check logs
sudo journalctl -u capibara6-backend -f

# Common fixes
sudo systemctl restart capibara6-backend
```

#### 2. Port Not Accessible
```bash
# Check if the service is listening
sudo netstat -tlnp | grep :5001

# Check firewall
sudo ufw status

# Check if process is running
ps aux | grep python
```

#### 3. Cross-VM Communication Issues
```bash
# Test connectivity between VMs
ping [TARGET_VM_IP]

# Test specific port
nc -zv [TARGET_VM_IP] [PORT]

# Check firewall rules in Google Cloud Console
```

#### 4. Model Loading Issues
```bash
# Check if Ollama is running
systemctl status ollama

# Check available models
ollama list

# Try to pull a model manually
ollama pull gpt-oss:20b
```

#### 5. Database Connection Issues (RAG3 VM)
```bash
# Check if Docker services are running
docker ps

# Check specific service logs
docker logs [container_name]

# Check if required ports are open
netstat -tlnp | grep [port_number]
```

### Monitoring and Logs

#### Service Logs
```bash
# View service logs
sudo journalctl -u capibara6-backend -f

# View application logs
tail -f /opt/capibara6/backend/logs/*.log
```

#### System Metrics
```bash
# Check system resources
htop

# Check disk usage
df -h

# Check network connections
netstat -tlnp
```

## Maintenance

### Regular Maintenance Tasks

#### 1. System Updates
```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Update Python packages (if needed)
pip3 install --upgrade pip
```

#### 2. Log Rotation
```bash
# Configure log rotation for application logs
sudo nano /etc/logrotate.d/capibara6
```

#### 3. Backup Procedures
```bash
# Backup configuration files
tar -czf backup-config-$(date +%Y%m%d).tar.gz /opt/capibara6/backend/.env /opt/capibara6/web/config.js

# Backup application data
# (Specific to your data storage approach)
```

### Performance Monitoring

#### 1. Resource Monitoring
Set up monitoring for:
- CPU and memory usage
- Disk space
- Network I/O
- Service response times

#### 2. Database Monitoring (RAG3 VM)
Monitor:
- Milvus collection sizes
- Nebula Graph performance
- PostgreSQL connection pools
- Redis cache hit ratio

### Security Updates

1. **Regularly update system packages**
2. **Monitor security advisories for all components**
3. **Update application dependencies**
4. **Review and update firewall rules**

### Scaling Considerations

#### Horizontal Scaling
- Add more backend instances behind a load balancer
- Scale database components based on load
- Implement caching strategies

#### Vertical Scaling
- Increase VM resources based on load
- Monitor resource utilization to right-size instances

## Production Checklist

### Before Going Live

- [ ] All services are running and healthy
- [ ] API endpoints are accessible
- [ ] SSL certificates are configured (if applicable)
- [ ] Load balancer is set up (if applicable)
- [ ] Monitoring and alerting are configured
- [ ] Backup procedures are tested
- [ ] Security hardening is complete
- [ ] Performance testing is completed
- [ ] Access logs are being collected

### Monitoring Setup

- [ ] Health checks for all services
- [ ] Resource utilization monitoring
- [ ] Error rate tracking
- [ ] Response time monitoring
- [ ] Database performance metrics
- [ ] User activity tracking

### Security Hardening

- [ ] SSH access is restricted to specific IPs
- [ ] Firewall rules are minimized
- [ ] SSL/TLS is enforced
- [ ] Authentication is implemented
- [ ] Regular security scans are scheduled
- [ ] Access logs are monitored

## Support and Operations

### Emergency Procedures

1. **Service Down:**
   - Check service status
   - Review logs
   - Restart service if needed
   - Scale resources if under load

2. **Performance Degradation:**
   - Check resource utilization
   - Review slow query logs
   - Scale database or compute resources
   - Implement caching if needed

3. **Security Incident:**
   - Isolate affected systems
   - Review access logs
   - Implement temporary blocks if needed
   - Update security measures

### Documentation References

- [VM Configuration Requirements](VM_CONFIG_REQUIREMENTS.md)
- [Backend Installation Script](backend_install_script.sh)
- [Frontend Installation Script](frontend_install_script.sh)
- [Original Project README](README.md)

---

**Congratulations!** Your Capibara6 system is now deployed and ready for use. Monitor the system for any issues and perform regular maintenance as outlined in this guide.