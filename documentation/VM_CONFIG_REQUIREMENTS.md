# VM Configuration Requirements for Capibara6 System

## Overview

The Capibara6 system is a distributed AI platform that consists of three primary VMs:

1. **VM Bounty2** (Model Server) - Hosts Ollama with GPT-OSS-20B and backend API
2. **VM Services** (Auxiliary Services) - Hosts TTS, MCP, N8N services
3. **VM RAG3** (RAG System) - Hosts Milvus, Nebula Graph, PostgreSQL, and monitoring

## VM Specifications

### VM Bounty2 (Model Server) - `bounty2`
- **Name**: bounty2
- **IP External**: 34.12.166.76
- **Zone**: europe-west4-a
- **Project**: mamba-001

#### Hardware Requirements:
- **CPU**: 8+ cores (recommended: 16 cores)
- **Memory**: 32GB+ RAM (recommended: 64GB for optimal performance)
- **Disk**: 200GB+ SSD storage (recommended: 500GB for model files)
- **GPU**: Optional but recommended for faster inference (NVIDIA GPU with CUDA support)

#### Ports to Expose:
- `8080` - GPT-OSS-20B model server (Ollama)
- `5001` - Backend API Flask

#### Software Stack:
- Ubuntu 20.04 LTS or 22.04 LTS
- Docker and Docker Compose
- Python 3.9+
- Ollama
- Git
- Node.js (optional for frontend development)

### VM Services (Auxiliary Services) - `gpt-oss-20b`
- **Name**: gpt-oss-20b
- **IP External**: 34.175.136.104
- **Zone**: europe-southwest1-b
- **Project**: mamba-001

#### Hardware Requirements:
- **CPU**: 4+ cores (recommended: 8 cores)
- **Memory**: 16GB+ RAM (recommended: 32GB)
- **Disk**: 100GB+ SSD storage (recommended: 200GB)
- **GPU**: Not required

#### Ports to Expose:
- `5002` - TTS (Text-to-Speech)
- `5003` - MCP (Model Context Protocol)
- `5678` - N8N (Automatization)

#### Software Stack:
- Ubuntu 20.04 LTS or 22.04 LTS
- Docker and Docker Compose
- Python 3.9+
- Node.js
- Redis
- Git

### VM RAG3 (RAG System) - `rag3`
- **Name**: rag3
- **IP Internal**: 10.154.0.2
- **Zone**: europe-west2-c
- **Project**: mamba-001

#### Hardware Requirements:
- **CPU**: 8+ cores (recommended: 16 cores)
- **Memory**: 32GB+ RAM (recommended: 64GB)
- **Disk**: 500GB+ SSD storage (recommended: 1TB for vector databases)
- **GPU**: Not required

#### Ports to Expose:
- `8000` - Bridge API (capibara6-api)
- `19530` - Milvus vector database
- `9669` - Nebula Graph
- `5432` - PostgreSQL
- `5433` - TimescaleDB
- `6379` - Redis
- `9090` - Prometheus
- `3000` - Grafana
- `16686` - Jaeger

#### Software Stack:
- Ubuntu 20.04 LTS or 22.04 LTS
- Docker and Docker Compose
- Milvus (v2.3.10)
- Nebula Graph (v3.1.0)
- PostgreSQL
- TimescaleDB
- Redis
- Prometheus
- Grafana
- Jaeger
- Git

## Network Configuration

### VPC and Subnets
- All VMs should be deployed in the same VPC for internal communication
- Use private IP ranges for internal communication between VMs
- Enable internal communication on the following ports:
  - 11434 - Ollama API (internal)
  - 5001 - Backend API (internal)
  - 5002 - TTS (internal)
  - 5003 - MCP (internal)
  - 8000 - RAG Bridge API (internal)

### Firewall Rules
- Allow traffic between VMs on internal ports
- Expose only required external ports to the internet
- Use security groups to limit access to necessary IP ranges

### Required Firewall Rules:

#### For VM Bounty2:
```bash
# Allow HTTP/HTTPS
gcloud compute firewall-rules create allow-http-https \
  --project="mamba-001" \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:80,tcp:443 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=capibara6-models

# Allow backend API
gcloud compute firewall-rules create allow-backend-api \
  --project="mamba-001" \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:5001 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=capibara6-models

# Allow Ollama (internal use)
gcloud compute firewall-rules create allow-ollama \
  --project="mamba-001" \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:11434 \
  --source-ranges=10.0.0.0/8 \
  --target-tags=capibara6-models
```

#### For VM Services:
```bash
# Allow TTS
gcloud compute firewall-rules create allow-tts \
  --project="mamba-001" \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:5002 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=capibara6-services

# Allow MCP
gcloud compute firewall-rules create allow-mcp \
  --project="mamba-001" \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:5003 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=capibara6-services

# Allow N8N
gcloud compute firewall-rules create allow-n8n \
  --project="mamba-001" \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:5678 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=capibara6-services
```

#### For VM RAG3:
```bash
# Allow Bridge API
gcloud compute firewall-rules create allow-bridge-api \
  --project="mamba-001" \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:8000 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=capibara6-rag

# Allow monitoring services
gcloud compute firewall-rules create allow-monitoring \
  --project="mamba-001" \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:3000,tcp:9090,tcp:16686 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=capibara6-rag
```

## Storage Requirements

### VM Bounty2
- **Boot Disk**: 50GB SSD
- **Additional Disk**: 200GB+ SSD for model files (can be mounted separately)
- **Model Storage**: GPT-OSS-20B model requires approximately 40GB of space

### VM Services
- **Boot Disk**: 50GB SSD
- **Additional Disk**: 50GB for service logs and temporary files

### VM RAG3
- **Boot Disk**: 50GB SSD
- **Additional Disk**: 500GB+ SSD for vector databases and monitoring data
- **Milvus Storage**: Varies based on data size, but plan for 100GB+ initially
- **Nebula Graph Storage**: Varies based on graph size

## Compute Engine Setup Commands

### Creating VMs using gcloud CLI:

#### VM Bounty2 (Model Server):
```bash
gcloud compute instances create bounty2 \
    --project="mamba-001" \
    --zone="europe-west4-a" \
    --machine-type="c2-standard-16" \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=100GB \
    --boot-disk-type=pd-ssd \
    --boot-disk-device-name="bounty2-boot" \
    --tags=capibara6-models \
    --shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --reservation-affinity=any
```

#### VM Services:
```bash
gcloud compute instances create gpt-oss-20b \
    --project="mamba-001" \
    --zone="europe-southwest1-b" \
    --machine-type="e2-standard-8" \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=100GB \
    --boot-disk-type=pd-ssd \
    --boot-disk-device-name="gpt-oss-20b-boot" \
    --tags=capibara6-services \
    --shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --reservation-affinity=any
```

#### VM RAG3:
```bash
gcloud compute instances create rag3 \
    --project="mamba-001" \
    --zone="europe-west2-c" \
    --machine-type="c2-standard-16" \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=200GB \
    --boot-disk-type=pd-ssd \
    --boot-disk-device-name="rag3-boot" \
    --tags=capibara6-rag \
    --shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --reservation-affinity=any
```

## SSH Access Configuration

### SSH Connection Commands:

#### VM Bounty2:
```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
```

#### VM Services:
```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
```

#### VM RAG3:
```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
```

## Additional Configuration Requirements

### System-level optimizations

#### For VM Bounty2 (High I/O):
```bash
# Increase file descriptor limits
echo '* soft nofile 65536' | sudo tee -a /etc/security/limits.conf
echo '* hard nofile 65536' | sudo tee -a /etc/security/limits.conf

# Optimize I/O scheduler
echo 'none' | sudo tee /sys/block/*/queue/scheduler

# Increase memory mapping limits for large models
echo 'capibara6 soft memlock unlimited' | sudo tee -a /etc/security/limits.conf
echo 'capibara6 hard memlock unlimited' | sudo tee -a /etc/security/limits.conf
```

#### For VM RAG3 (Database VM):
```bash
# Optimize for database workloads
echo 'vm.swappiness=1' | sudo tee -a /etc/sysctl.conf
echo 'vm.dirty_ratio=15' | sudo tee -a /etc/sysctl.conf
echo 'vm.dirty_background_ratio=5' | sudo tee -a /etc/sysctl.conf

# Apply changes
sudo sysctl -p
```

### Monitoring and Logging Setup

All VMs should have:
- Stackdriver logging and monitoring agents installed
- Proper service account with required permissions
- Log retention policies configured

### Backup and Recovery

#### Automatic backup configuration:
- Configure scheduled snapshots of boot disks
- Set up monitoring for backup status
- Test backup restoration procedures

### Security Considerations

#### VM-level security:
- Enable confidential computing if handling sensitive data
- Use secure boot and integrity monitoring
- Regular OS updates and security patches
- Limit SSH access to specific IP ranges when possible

#### Network security:
- Use private IPs for internal communication
- Restrict firewall rules to minimum required ports
- Implement proper authentication and authorization mechanisms
- Enable VPC flow logs for network monitoring

## Cost Optimization Suggestions

1. **Use committed use discounts** for long-running workloads
2. **Consider preemptible instances** for non-critical workloads
3. **Implement automated shutdown** during non-business hours
4. **Monitor resource utilization** and right-size instances as needed
5. **Use regional disks** instead of multi-regional for cost savings

## Maintenance Considerations

- Regular monitoring of resource utilization
- Automated alerts for system health
- Regular backup verification
- Update management schedule
- Capacity planning for growth