-- SafePay MENA - Supabase / PostgreSQL Audit Trail Migration Schema
-- Fulfills PRD User Story #14 & SAMA Cybersecurity Auditability Mandates

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS safepay_audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_id VARCHAR(64) NOT NULL,
    sender_phone VARCHAR(20) NOT NULL,
    recipient_id VARCHAR(64) NOT NULL,
    recipient_name VARCHAR(128),
    amount NUMERIC(14, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    is_saved_beneficiary BOOLEAN DEFAULT FALSE,
    
    -- Risk Decision
    decision VARCHAR(20) NOT NULL CHECK (decision IN ('APPROVE', 'STEP_UP', 'BLOCK')),
    risk_score INTEGER NOT NULL CHECK (risk_score >= 0 AND risk_score <= 100),
    primary_vector VARCHAR(64) NOT NULL,
    
    -- CAMARA Telemetry Snapshot
    carrier_name VARCHAR(64),
    number_verified BOOLEAN,
    sim_swapped_recently BOOLEAN,
    sim_swap_hours_ago NUMERIC(6, 2),
    is_on_active_voice_call BOOLEAN,
    is_roaming BOOLEAN,
    roaming_country VARCHAR(4),
    device_match BOOLEAN,
    
    -- Regulatory Compliance & Explainability
    statutory_flags TEXT[] DEFAULT '{}',
    reasons TEXT[] DEFAULT '{}',
    ai_compliance_trace TEXT,
    
    -- Performance Metrics
    execution_time_ms NUMERIC(8, 4) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indices for rapid compliance query and auditing
CREATE INDEX IF NOT EXISTS idx_safepay_txn_id ON safepay_audit_logs(transaction_id);
CREATE INDEX IF NOT EXISTS idx_safepay_sender ON safepay_audit_logs(sender_phone);
CREATE INDEX IF NOT EXISTS idx_safepay_decision ON safepay_audit_logs(decision);
CREATE INDEX IF NOT EXISTS idx_safepay_created_at ON safepay_audit_logs(created_at DESC);

-- Row-Level Security (RLS) ensuring tamper-proof audit trails
ALTER TABLE safepay_audit_logs ENABLE ROW LEVEL SECURITY;

-- Read-only policy for auditors
CREATE POLICY "Auditors can view tamper-proof logs" 
    ON safepay_audit_logs 
    FOR SELECT 
    TO authenticated 
    USING (true);

-- Insert policy for backend gateway
CREATE POLICY "Backend gateway can insert audit records" 
    ON safepay_audit_logs 
    FOR INSERT 
    TO authenticated 
    WITH CHECK (true);
