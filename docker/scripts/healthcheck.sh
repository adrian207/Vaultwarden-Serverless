#!/bin/sh
##
## Vaultwarden Health Check Script
## Author: Adrian Johnson <adrian207@gmail.com>
##
## This script performs a comprehensive health check for Vaultwarden
##

# Check if the service is responding
if ! curl -f http://localhost:80/alive >/dev/null 2>&1; then
    echo "Health check failed: /alive endpoint not responding"
    exit 1
fi

# Check if web vault is accessible
if ! curl -f http://localhost:80/ >/dev/null 2>&1; then
    echo "Health check failed: web vault not accessible"
    exit 1
fi

# All checks passed
exit 0

