# Custom Vaultwarden Dockerfile with Optimizations
# Author: Adrian Johnson <adrian207@gmail.com>
#
# [Inference] This Dockerfile extends the official Vaultwarden image
# with additional optimizations for serverless deployment

FROM vaultwarden/server:latest

# Metadata
LABEL maintainer="Adrian Johnson <adrian207@gmail.com>"
LABEL description="Optimized Vaultwarden for serverless deployment"
LABEL version="1.0.0"

# Install additional tools for health checks and monitoring
RUN apk add --no-cache \
    curl \
    ca-certificates \
    && rm -rf /var/cache/apk/*

# Copy custom configuration
COPY docker/scripts/healthcheck.sh /healthcheck.sh
RUN chmod +x /healthcheck.sh

# Health check configuration
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD /healthcheck.sh

# Set environment defaults optimized for serverless
ENV ROCKET_ADDRESS=0.0.0.0 \
    ROCKET_PORT=80 \
    ROCKET_WORKERS=10 \
    DATABASE_MAX_CONNS=10 \
    WEB_VAULT_ENABLED=true \
    WEBSOCKET_ENABLED=true \
    SENDS_ALLOWED=true \
    EMERGENCY_ACCESS_ALLOWED=true

# Expose port
EXPOSE 80

# Use the original entrypoint from vaultwarden/server
ENTRYPOINT ["/vaultwarden"]

