-- DevOps Secrets Management - Initial Schema
-- Author: Adrian Johnson <adrian207@gmail.com>
-- Version: 1.0
-- Date: 2025-11-05

-- ============================================================================
-- SERVICE ACCOUNTS
-- ============================================================================

CREATE TABLE IF NOT EXISTS service_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    permissions JSONB NOT NULL DEFAULT '{}',
    -- Example: {"paths": ["production/*"], "actions": ["read"], "deny_paths": []}
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP WITH TIME ZONE,
    active BOOLEAN DEFAULT true,
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_service_accounts_name ON service_accounts(name);
CREATE INDEX idx_service_accounts_active ON service_accounts(active);
CREATE INDEX idx_service_accounts_created_at ON service_accounts(created_at);

COMMENT ON TABLE service_accounts IS 'Service accounts for machine-to-machine authentication';
COMMENT ON COLUMN service_accounts.permissions IS 'JSONB object defining allowed/denied paths and actions';

-- ============================================================================
-- API KEYS
-- ============================================================================

CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_account_id UUID NOT NULL REFERENCES service_accounts(id) ON DELETE CASCADE,
    key_hash VARCHAR(255) NOT NULL UNIQUE,
    -- bcrypt hash of the API key
    key_prefix VARCHAR(20) NOT NULL,
    -- First 8-10 chars for identification (vw_svc_abcd...)
    key_name VARCHAR(255),
    -- Optional friendly name
    permissions JSONB,
    -- Optional: Override service account permissions
    rate_limit JSONB DEFAULT '{"requests_per_second": 100, "burst": 200}',
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP WITH TIME ZONE,
    last_used_ip INET,
    revoked BOOLEAN DEFAULT false,
    revoked_at TIMESTAMP WITH TIME ZONE,
    revoked_by VARCHAR(255),
    revoked_reason TEXT,
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_api_keys_service_account ON api_keys(service_account_id);
CREATE INDEX idx_api_keys_key_hash ON api_keys(key_hash);
CREATE INDEX idx_api_keys_key_prefix ON api_keys(key_prefix);
CREATE INDEX idx_api_keys_expires_at ON api_keys(expires_at);
CREATE INDEX idx_api_keys_revoked ON api_keys(revoked);

COMMENT ON TABLE api_keys IS 'API keys for authenticating service accounts';
COMMENT ON COLUMN api_keys.key_hash IS 'bcrypt hash of the full API key (never stored plaintext)';
COMMENT ON COLUMN api_keys.key_prefix IS 'First 8-10 characters for user-friendly identification';

-- ============================================================================
-- SECRETS METADATA
-- ============================================================================

CREATE TABLE IF NOT EXISTS secrets_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    path VARCHAR(500) NOT NULL UNIQUE,
    -- e.g., "production/database/password"
    cipher_id UUID,
    -- Reference to Vaultwarden ciphers table (actual encrypted value)
    description TEXT,
    secret_type VARCHAR(50) DEFAULT 'generic',
    -- generic, database, api_key, ssh_key, certificate, etc.
    rotation_enabled BOOLEAN DEFAULT false,
    rotation_policy_id UUID,
    -- Reference to rotation_policies table
    current_version INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(255),
    expires_at TIMESTAMP WITH TIME ZONE,
    tags TEXT[],
    -- Array of tags for organization
    metadata JSONB DEFAULT '{}',
    -- Additional metadata (environment, owner, service, etc.)
    active BOOLEAN DEFAULT true
);

CREATE INDEX idx_secrets_metadata_path ON secrets_metadata(path);
CREATE INDEX idx_secrets_metadata_path_prefix ON secrets_metadata(path text_pattern_ops);
-- For prefix searches like "production/*"
CREATE INDEX idx_secrets_metadata_cipher_id ON secrets_metadata(cipher_id);
CREATE INDEX idx_secrets_metadata_rotation_enabled ON secrets_metadata(rotation_enabled);
CREATE INDEX idx_secrets_metadata_expires_at ON secrets_metadata(expires_at);
CREATE INDEX idx_secrets_metadata_tags ON secrets_metadata USING GIN(tags);
CREATE INDEX idx_secrets_metadata_metadata ON secrets_metadata USING GIN(metadata);

COMMENT ON TABLE secrets_metadata IS 'Metadata for secrets (actual values stored in Vaultwarden ciphers)';
COMMENT ON COLUMN secrets_metadata.path IS 'Hierarchical path for the secret (e.g., production/db/password)';
COMMENT ON COLUMN secrets_metadata.cipher_id IS 'Reference to Vaultwarden cipher containing encrypted value';

-- ============================================================================
-- SECRET VERSIONS
-- ============================================================================

CREATE TABLE IF NOT EXISTS secret_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    secret_id UUID NOT NULL REFERENCES secrets_metadata(id) ON DELETE CASCADE,
    version INTEGER NOT NULL,
    cipher_id UUID,
    -- Each version can have its own cipher
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255),
    -- user email, service account name, or "system"
    creation_method VARCHAR(50) DEFAULT 'manual',
    -- manual, rotation, migration, etc.
    active BOOLEAN DEFAULT false,
    -- Only one version is active at a time
    metadata JSONB DEFAULT '{}',
    UNIQUE(secret_id, version)
);

CREATE INDEX idx_secret_versions_secret_id ON secret_versions(secret_id);
CREATE INDEX idx_secret_versions_version ON secret_versions(secret_id, version);
CREATE INDEX idx_secret_versions_active ON secret_versions(secret_id, active);
CREATE INDEX idx_secret_versions_created_at ON secret_versions(created_at);

COMMENT ON TABLE secret_versions IS 'Version history for secrets';
COMMENT ON COLUMN secret_versions.active IS 'Only one version per secret should be active';

-- ============================================================================
-- ROTATION POLICIES
-- ============================================================================

CREATE TABLE IF NOT EXISTS rotation_policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    secret_path VARCHAR(500) NOT NULL,
    -- Can be specific path or pattern with wildcards
    rotation_interval_days INTEGER NOT NULL,
    -- How often to rotate (e.g., 30 days)
    rotation_window VARCHAR(50) DEFAULT '02:00-04:00',
    -- UTC time window for rotation
    target_system JSONB NOT NULL,
    -- Configuration for where to apply rotated secret
    -- Example: {"type": "postgresql", "host": "db.company.com", "database": "prod"}
    health_check JSONB,
    -- Optional health check after rotation
    -- Example: {"url": "https://api.company.com/health", "expected_status": 200}
    notification JSONB DEFAULT '{}',
    -- Notification settings (email, slack, etc.)
    rollback_on_failure BOOLEAN DEFAULT true,
    last_rotation TIMESTAMP WITH TIME ZONE,
    next_rotation TIMESTAMP WITH TIME ZONE,
    rotation_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_rotation_policies_secret_path ON rotation_policies(secret_path);
CREATE INDEX idx_rotation_policies_next_rotation ON rotation_policies(next_rotation);
CREATE INDEX idx_rotation_policies_active ON rotation_policies(active);

COMMENT ON TABLE rotation_policies IS 'Automatic rotation policies for secrets';
COMMENT ON COLUMN rotation_policies.target_system IS 'JSONB configuration for where to apply the rotated secret';

-- ============================================================================
-- SECRET AUDIT LOG
-- ============================================================================

CREATE TABLE IF NOT EXISTS secret_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    secret_path VARCHAR(500) NOT NULL,
    secret_id UUID REFERENCES secrets_metadata(id) ON DELETE SET NULL,
    action VARCHAR(50) NOT NULL,
    -- read, create, update, delete, rotate, rollback
    actor VARCHAR(255) NOT NULL,
    -- user email, service account name, or "system"
    actor_type VARCHAR(50) NOT NULL,
    -- user, service_account, system
    api_key_id UUID REFERENCES api_keys(id) ON DELETE SET NULL,
    service_account_id UUID REFERENCES service_accounts(id) ON DELETE SET NULL,
    ip_address INET,
    user_agent TEXT,
    success BOOLEAN NOT NULL,
    error_message TEXT,
    version_accessed INTEGER,
    request_id VARCHAR(100),
    -- For correlating related actions
    duration_ms INTEGER,
    -- How long the operation took
    metadata JSONB DEFAULT '{}',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_secret_path ON secret_audit_log(secret_path);
CREATE INDEX idx_audit_secret_id ON secret_audit_log(secret_id);
CREATE INDEX idx_audit_action ON secret_audit_log(action);
CREATE INDEX idx_audit_actor ON secret_audit_log(actor);
CREATE INDEX idx_audit_timestamp ON secret_audit_log(timestamp);
CREATE INDEX idx_audit_success ON secret_audit_log(success);
CREATE INDEX idx_audit_service_account ON secret_audit_log(service_account_id);

COMMENT ON TABLE secret_audit_log IS 'Comprehensive audit log for all secret operations';
COMMENT ON COLUMN secret_audit_log.actor IS 'Who performed the action (user, service account, or system)';

-- ============================================================================
-- ROTATION HISTORY
-- ============================================================================

CREATE TABLE IF NOT EXISTS rotation_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rotation_policy_id UUID NOT NULL REFERENCES rotation_policies(id) ON DELETE CASCADE,
    secret_id UUID NOT NULL REFERENCES secrets_metadata(id) ON DELETE CASCADE,
    old_version INTEGER,
    new_version INTEGER,
    started_at TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) NOT NULL,
    -- pending, in_progress, success, failed, rolled_back
    error_message TEXT,
    health_check_result JSONB,
    rollback_reason TEXT,
    triggered_by VARCHAR(255),
    -- system, manual, user email
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_rotation_history_policy ON rotation_history(rotation_policy_id);
CREATE INDEX idx_rotation_history_secret ON rotation_history(secret_id);
CREATE INDEX idx_rotation_history_started_at ON rotation_history(started_at);
CREATE INDEX idx_rotation_history_status ON rotation_history(status);

COMMENT ON TABLE rotation_history IS 'History of all rotation attempts';

-- ============================================================================
-- VIEWS
-- ============================================================================

-- Active secrets with current version info
CREATE OR REPLACE VIEW active_secrets AS
SELECT 
    sm.id,
    sm.path,
    sm.description,
    sm.secret_type,
    sm.current_version,
    sv.cipher_id,
    sv.created_at as version_created_at,
    sv.created_by as version_created_by,
    sm.rotation_enabled,
    rp.rotation_interval_days,
    rp.next_rotation,
    sm.expires_at,
    sm.tags,
    sm.metadata
FROM secrets_metadata sm
LEFT JOIN secret_versions sv ON sm.id = sv.secret_id AND sv.active = true
LEFT JOIN rotation_policies rp ON sm.rotation_policy_id = rp.id
WHERE sm.active = true;

COMMENT ON VIEW active_secrets IS 'All active secrets with their current version information';

-- Service account usage statistics
CREATE OR REPLACE VIEW service_account_stats AS
SELECT 
    sa.id,
    sa.name,
    sa.active,
    COUNT(DISTINCT ak.id) as total_keys,
    COUNT(DISTINCT ak.id) FILTER (WHERE ak.revoked = false) as active_keys,
    MAX(ak.last_used_at) as last_key_used_at,
    COUNT(DISTINCT sal.id) as total_api_calls,
    COUNT(DISTINCT sal.id) FILTER (WHERE sal.timestamp > CURRENT_TIMESTAMP - INTERVAL '24 hours') as calls_last_24h,
    COUNT(DISTINCT sal.id) FILTER (WHERE sal.success = false) as failed_calls
FROM service_accounts sa
LEFT JOIN api_keys ak ON sa.id = ak.service_account_id
LEFT JOIN secret_audit_log sal ON sa.id = sal.service_account_id
GROUP BY sa.id, sa.name, sa.active;

COMMENT ON VIEW service_account_stats IS 'Usage statistics for service accounts';

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to tables with updated_at column
CREATE TRIGGER update_service_accounts_updated_at BEFORE UPDATE ON service_accounts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_secrets_metadata_updated_at BEFORE UPDATE ON secrets_metadata
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_rotation_policies_updated_at BEFORE UPDATE ON rotation_policies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- SAMPLE DATA (for development/testing)
-- ============================================================================

-- Uncomment to insert sample data in development environment

-- INSERT INTO service_accounts (name, description, permissions, created_by) VALUES
-- ('api-server-production', 'Production API server', 
--  '{"paths": ["production/database/*", "production/api-keys/*"], "actions": ["read"]}', 
--  'admin@company.com'),
-- ('ci-cd-pipeline', 'GitHub Actions CI/CD', 
--  '{"paths": ["staging/*", "production/*"], "actions": ["read"]}', 
--  'admin@company.com'),
-- ('developer-cli', 'Developer CLI tool', 
--  '{"paths": ["development/*"], "actions": ["read", "write"]}', 
--  'admin@company.com');

-- ============================================================================
-- PERMISSIONS
-- ============================================================================

-- Grant appropriate permissions to Vaultwarden database user
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO vaultwarden;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO vaultwarden;

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================

-- Version: 001
-- Date: 2025-11-05
-- Status: Initial schema for DevOps Secrets Management

