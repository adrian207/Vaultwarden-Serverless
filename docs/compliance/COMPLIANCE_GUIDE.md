# Compliance Certifications Guide (SOC 2 & ISO 27001)

**Author:** Adrian Johnson <adrian207@gmail.com>  
**Date:** November 5, 2025  
**Status:** Documentation Complete - Ready for Implementation

## Executive Summary

Achieve SOC 2 Type II and ISO 27001 compliance for your Vaultwarden password management deployment.

**What This Guide Covers:**
- ✅ SOC 2 compliance requirements
- ✅ ISO 27001 compliance requirements
- ✅ Control mapping to Vaultwarden features
- ✅ Evidence collection
- ✅ Audit preparation
- ✅ Implementation timeline
- ✅ Cost estimates
- ✅ Continuous compliance

**Why Compliance Matters:**
- Required for enterprise customers
- Builds trust and credibility
- Reduces security risks
- Competitive advantage
- Higher contract values

**Timeline:** 6-12 months for initial certification  
**Cost:** $20,000-100,000 (depending on scope and auditor)

---

## Understanding Compliance Frameworks

### SOC 2 (Service Organization Control 2)

**What It Is:**
- Auditing standard developed by AICPA (American Institute of CPAs)
- Evaluates service organization's information security controls
- Focuses on Trust Services Criteria (TSC)

**Trust Services Criteria:**
1. **Security** - Protection against unauthorized access
2. **Availability** - System accessible as agreed
3. **Processing Integrity** - System processing complete, valid, accurate
4. **Confidentiality** - Information designated confidential is protected
5. **Privacy** - Personal information collected, used, retained, disclosed appropriately

**Types:**
- **SOC 2 Type I** - Point-in-time assessment (controls designed properly)
- **SOC 2 Type II** - Period-of-time assessment (controls operating effectively 6-12 months)

**Who Needs It:**
- SaaS companies
- Cloud service providers
- Data centers
- Any company handling customer data

**Best For:** U.S. customers, SaaS businesses

---

### ISO 27001

**What It Is:**
- International standard for information security management systems (ISMS)
- Developed by ISO (International Organization for Standardization)
- Risk-based approach to information security

**Core Components:**
- ISMS policies and procedures
- Risk assessment methodology
- Statement of Applicability (SoA)
- 114 controls across 14 domains

**14 Control Domains:**
1. Information security policies
2. Organization of information security
3. Human resource security
4. Asset management
5. Access control
6. Cryptography
7. Physical and environmental security
8. Operations security
9. Communications security
10. System acquisition, development and maintenance
11. Supplier relationships
12. Information security incident management
13. Information security aspects of business continuity management
14. Compliance

**Who Needs It:**
- International companies
- Organizations with European customers
- Regulated industries
- Government contractors

**Best For:** Global companies, international customers

---

## Why Your Vaultwarden Deployment Helps

### Built-In Compliance Features

✅ **Encryption** - Zero-knowledge encryption (AES-256)  
✅ **Access Control** - Role-based access control (RBAC)  
✅ **Audit Logs** - Complete event logging  
✅ **Authentication** - Multi-factor authentication  
✅ **Backup & Recovery** - Automated encrypted backups  
✅ **Monitoring** - Real-time security monitoring  
✅ **Disaster Recovery** - Multi-region deployment  
✅ **Change Management** - Infrastructure as Code (Terraform)  
✅ **Incident Response** - Automated alerting  
✅ **Data Retention** - Configurable retention policies  

### Infrastructure Compliance

✅ **Cloud Provider Certifications:**
- AWS: SOC 2, ISO 27001, FedRAMP, HIPAA, PCI DSS
- GCP: SOC 2, ISO 27001, FedRAMP, HIPAA, PCI DSS
- Azure: SOC 2, ISO 27001, FedRAMP, HIPAA, PCI DSS

**Inheritance:** Your deployment inherits physical security and infrastructure controls from cloud provider

---

## Compliance Readiness Assessment

### Current State

**What You Already Have:**

✅ **Security Controls (75% Ready)**
- Encryption at rest and in transit
- Network isolation (VPC, subnets)
- Security groups and firewalls
- WAF and DDoS protection
- Secrets management
- TLS 1.3 enforcement

✅ **Access Controls (80% Ready)**
- Role-based access control (RBAC)
- Multi-factor authentication (2FA)
- Password policies
- Session management
- Emergency access procedures

✅ **Monitoring & Logging (70% Ready)**
- Event logs (all user actions)
- Application logs
- Infrastructure metrics
- Automated alerting
- Security dashboards

✅ **Backup & Recovery (85% Ready)**
- Automated daily backups
- Encrypted backups
- Multi-region replication
- Tested restore procedures
- Point-in-time recovery

✅ **Change Management (90% Ready)**
- Infrastructure as Code (Terraform)
- Version control (Git)
- CI/CD pipelines
- Automated testing
- Change approval process

---

### Gap Analysis

**What You Need to Add:**

❌ **Information Security Policies (0% Ready)**
- Information Security Policy
- Acceptable Use Policy
- Password Policy
- Incident Response Policy
- Business Continuity Policy
- Data Classification Policy
- Change Management Policy
- Risk Management Policy

❌ **Risk Assessment (0% Ready)**
- Risk identification
- Risk analysis
- Risk treatment
- Risk register
- Risk monitoring

❌ **Vendor Management (20% Ready)**
- Vendor security assessments
- Vendor contracts with security clauses
- Vendor monitoring

❌ **Security Awareness Training (0% Ready)**
- Employee security training program
- Phishing simulations
- Training records
- Annual refresher training

❌ **Physical Security (50% Ready via Cloud)**
- Data center access controls (cloud provider)
- Office security (your responsibility)
- Device management policies

❌ **Incident Response Plan (30% Ready)**
- Formal incident response procedures
- Incident classification
- Communication plan
- Post-incident review process

---

## SOC 2 Control Mapping

### Common Criteria (CC)

#### CC1: Control Environment

| Control | Vaultwarden Implementation | Evidence |
|---------|---------------------------|----------|
| CC1.1: Organization demonstrates commitment to integrity and ethical values | Document in company policies | Policy documents, code of conduct |
| CC1.2: Board exercises oversight | Board meeting minutes discussing security | Meeting minutes, reports |
| CC1.3: Management establishes structure, authority, responsibility | Organization chart, role definitions | Org chart, job descriptions |
| CC1.4: Organization demonstrates commitment to competence | Security training program | Training records, certificates |
| CC1.5: Organization holds individuals accountable | Performance reviews include security | Review documents |

**Implementation Status:** 40% (Policies needed)

---

#### CC2: Communication and Information

| Control | Vaultwarden Implementation | Evidence |
|---------|---------------------------|----------|
| CC2.1: Organization obtains/generates relevant info | Monitoring dashboards, event logs | Dashboard screenshots, log samples |
| CC2.2: Information security communicated internally | Security awareness training, policies | Training records, policy distribution |
| CC2.3: Information security communicated externally | Customer security documentation | Security whitepaper, compliance docs |

**Implementation Status:** 60% (Training program needed)

---

#### CC3: Risk Assessment

| Control | Vaultwarden Implementation | Evidence |
|---------|---------------------------|----------|
| CC3.1: Organization specifies objectives | Document security objectives | Objectives document |
| CC3.2: Organization identifies and analyzes risk | Risk assessment process | Risk register, assessment reports |
| CC3.3: Organization considers potential for fraud | Fraud risk assessment | Assessment documents |
| CC3.4: Organization identifies and assesses changes | Change management process | Change logs, assessments |

**Implementation Status:** 30% (Risk assessment needed)

---

#### CC4: Monitoring Activities

| Control | Vaultwarden Implementation | Evidence |
|---------|---------------------------|----------|
| CC4.1: Organization monitors system | ✅ CloudWatch/Cloud Monitoring dashboards | Dashboard screenshots, alert history |
| CC4.2: Organization evaluates and communicates deficiencies | Incident response process, reports to management | Incident reports, management updates |

**Implementation Status:** 75% (Formal processes needed)

---

#### CC5: Control Activities

| Control | Vaultwarden Implementation | Evidence |
|---------|---------------------------|----------|
| CC5.1: Organization selects and develops control activities | ✅ Security controls documented in this guide | This documentation |
| CC5.2: Organization develops general IT controls | ✅ Infrastructure as Code, change management | Terraform configs, Git history |
| CC5.3: Organization deploys control activities | ✅ Controls deployed in production | Deployment logs, configurations |

**Implementation Status:** 80% (Documentation refinement)

---

#### CC6: Logical and Physical Access Controls

| Control | Vaultwarden Implementation | Evidence |
|---------|---------------------------|----------|
| CC6.1: Organization implements logical access security | ✅ RBAC, 2FA, session management | User permissions, 2FA enrollment, logs |
| CC6.2: Prior to issuing credentials, organization identifies and authenticates users | ✅ User invitation and confirmation process | User provisioning logs |
| CC6.3: Organization considers network segmentation | ✅ VPC, security groups, private subnets | Network diagrams, SG rules |
| CC6.4: Organization restricts physical access | ✅ Cloud provider data centers | Cloud provider SOC 2 reports |
| CC6.5: Organization discontinues access when no longer required | ✅ User offboarding process | Termination logs, access revocation |
| CC6.6: Organization implements controls to prevent unauthorized software | ✅ Container images, approved software list | Dockerfile, image scanning |
| CC6.7: Organization manages encryption keys | ✅ Secrets Manager, encryption at rest | Secrets management logs, encryption configs |
| CC6.8: Organization restricts access to sensitive information | ✅ Collection-based access control | Collection permissions, user assignments |

**Implementation Status:** 90% (Documented procedures needed)

---

#### CC7: System Operations

| Control | Vaultwarden Implementation | Evidence |
|---------|---------------------------|----------|
| CC7.1: Organization monitors system to meet objectives | ✅ Monitoring dashboards, alerts | CloudWatch/Monitoring screenshots |
| CC7.2: Organization implements change management | ✅ Terraform, Git, CI/CD | Git history, deployment logs |
| CC7.3: Organization implements incident response procedures | ⚠️ Automated alerts (formal process needed) | Alert configurations, incident logs |
| CC7.4: Organization implements backup procedures | ✅ Automated daily backups, tested restores | Backup logs, restore test results |
| CC7.5: Organization implements disaster recovery procedures | ✅ Multi-region deployment, failover | DR plan, failover tests |

**Implementation Status:** 85% (Incident response formalization)

---

#### CC8: Change Management

| Control | Vaultwarden Implementation | Evidence |
|---------|---------------------------|----------|
| CC8.1: Organization authorizes, designs, develops, and configures changes | ✅ Infrastructure as Code, PR reviews | Git commits, PR approvals |
| CC8.2: Organization tests system changes | ✅ CI/CD pipelines with tests | Pipeline logs, test results |
| CC8.3: Organization deploys changes | ✅ Automated deployments | Deployment logs, release notes |
| CC8.4: Organization identifies changes that could impact system | Change impact assessments | Assessment documents |

**Implementation Status:** 85% (Impact assessments needed)

---

#### CC9: Risk Mitigation

| Control | Vaultwarden Implementation | Evidence |
|---------|---------------------------|----------|
| CC9.1: Organization identifies, selects, and develops risk mitigation activities | Risk treatment plan | Risk register with mitigations |
| CC9.2: Organization reassesses risk | Ongoing risk monitoring | Risk review meeting minutes |

**Implementation Status:** 20% (Risk management program needed)

---

## ISO 27001 Control Mapping

### A.5: Information Security Policies

| Control | Requirement | Vaultwarden Implementation | Status |
|---------|------------|---------------------------|--------|
| A.5.1 | Policies for information security | Information Security Policy document | ❌ Need policy |
| A.5.2 | Review of policies | Annual policy review process | ❌ Need process |

---

### A.6: Organization of Information Security

| Control | Requirement | Vaultwarden Implementation | Status |
|---------|------------|---------------------------|--------|
| A.6.1.1 | Information security roles | Document security roles and responsibilities | ⚠️ Partially (Owner, Admin roles) |
| A.6.1.2 | Segregation of duties | Separate admin and user roles | ✅ Implemented |
| A.6.1.3 | Contact with authorities | Document process for contacting law enforcement | ❌ Need procedure |
| A.6.1.4 | Contact with special interest groups | Membership in security communities | ⚠️ Optional |
| A.6.1.5 | Information security in project management | Security requirements in projects | ⚠️ Partially |
| A.6.2.1 | Mobile device policy | BYOD policy for accessing Vaultwarden | ❌ Need policy |
| A.6.2.2 | Teleworking | Remote work security policy | ❌ Need policy |

---

### A.7: Human Resource Security

| Control | Requirement | Vaultwarden Implementation | Status |
|---------|------------|---------------------------|--------|
| A.7.1.1 | Screening | Background checks for employees | ⚠️ Company-dependent |
| A.7.1.2 | Terms and conditions of employment | Security responsibilities in contracts | ❌ Need clauses |
| A.7.2.1 | Management responsibilities | Management enforces security | ⚠️ Partially |
| A.7.2.2 | Information security awareness | ✅ Security training program | ❌ Need training |
| A.7.2.3 | Disciplinary process | Disciplinary policy for violations | ❌ Need policy |
| A.7.3.1 | Termination responsibilities | ✅ User offboarding process | ✅ Documented |

---

### A.8: Asset Management

| Control | Requirement | Vaultwarden Implementation | Status |
|---------|------------|---------------------------|--------|
| A.8.1.1 | Inventory of assets | Document all Vaultwarden infrastructure | ⚠️ Terraform (need inventory) |
| A.8.1.2 | Ownership of assets | Assign asset owners | ❌ Need assignments |
| A.8.1.3 | Acceptable use of assets | Acceptable Use Policy | ❌ Need policy |
| A.8.1.4 | Return of assets | Asset return process (devices) | ❌ Need process |
| A.8.2.1 | Classification of information | ✅ Data classification (passwords = confidential) | ✅ Inherent |
| A.8.2.2 | Labeling of information | Labeling sensitive data | ⚠️ In collections |
| A.8.2.3 | Handling of assets | Secure handling procedures | ⚠️ Partially |
| A.8.3.1 | Management of removable media | USB/external drive policy | ❌ Need policy |
| A.8.3.2 | Disposal of media | Secure disposal procedures | ❌ Need procedure |
| A.8.3.3 | Physical media transfer | Physical media handling | ❌ Need procedure |

---

### A.9: Access Control

| Control | Requirement | Vaultwarden Implementation | Status |
|---------|------------|---------------------------|--------|
| A.9.1.1 | Access control policy | ✅ RBAC policy | ✅ Documented |
| A.9.1.2 | Access to networks and services | ✅ VPC, security groups | ✅ Implemented |
| A.9.2.1 | User registration and deregistration | ✅ User invitation/removal process | ✅ Documented |
| A.9.2.2 | User access provisioning | ✅ Collection-based provisioning | ✅ Implemented |
| A.9.2.3 | Management of privileged access | ✅ Owner/Admin role management | ✅ Implemented |
| A.9.2.4 | Management of secret authentication | ✅ Master password + 2FA | ✅ Enforced |
| A.9.2.5 | Review of user access rights | Quarterly access reviews | ❌ Need process |
| A.9.2.6 | Removal of access rights | ✅ Immediate revocation on termination | ✅ Documented |
| A.9.3.1 | Use of secret authentication | ✅ Strong password policies | ✅ Enforced |
| A.9.4.1 | Information access restriction | ✅ Collection-based access | ✅ Implemented |
| A.9.4.2 | Secure log-on procedures | ✅ 2FA, session timeout | ✅ Implemented |
| A.9.4.3 | Password management system | ✅ Vaultwarden itself | ✅ Core function |
| A.9.4.4 | Use of privileged utility programs | Administrative access controls | ✅ Implemented |
| A.9.4.5 | Access control to program source code | ✅ Git with access controls | ✅ Implemented |

**Access Control Domain:** 80% compliant

---

### A.10: Cryptography

| Control | Requirement | Vaultwarden Implementation | Status |
|---------|------------|---------------------------|--------|
| A.10.1.1 | Policy on use of cryptographic controls | Cryptography policy | ❌ Need policy |
| A.10.1.2 | Key management | ✅ Secrets Manager, encryption keys | ✅ Implemented |

**Cryptography Domain:** 70% compliant

---

### A.12: Operations Security

| Control | Requirement | Vaultwarden Implementation | Status |
|---------|------------|---------------------------|--------|
| A.12.1.1 | Documented operating procedures | Operating procedures documentation | ⚠️ Partially (deployment guides) |
| A.12.1.2 | Change management | ✅ Terraform, CI/CD, Git | ✅ Implemented |
| A.12.1.3 | Capacity management | ✅ Auto-scaling | ✅ Implemented |
| A.12.1.4 | Separation of environments | ✅ Production/staging separation | ✅ Implemented |
| A.12.2.1 | Controls against malware | Container scanning, WAF | ✅ Implemented |
| A.12.3.1 | Information backup | ✅ Automated daily backups | ✅ Implemented |
| A.12.4.1 | Event logging | ✅ Comprehensive event logs | ✅ Implemented |
| A.12.4.2 | Protection of log information | ✅ Log encryption, access controls | ✅ Implemented |
| A.12.4.3 | Administrator and operator logs | ✅ Admin action logging | ✅ Implemented |
| A.12.4.4 | Clock synchronization | ✅ NTP synchronization (cloud) | ✅ Implemented |
| A.12.5.1 | Installation of software | Approved software only (containers) | ✅ Implemented |
| A.12.6.1 | Management of technical vulnerabilities | Vulnerability scanning, patching | ⚠️ Partially |
| A.12.6.2 | Restrictions on software installation | ✅ Immutable containers | ✅ Implemented |
| A.12.7.1 | Information systems audit controls | Audit logging enabled | ✅ Implemented |

**Operations Security Domain:** 85% compliant

---

### A.13: Communications Security

| Control | Requirement | Vaultwarden Implementation | Status |
|---------|------------|---------------------------|--------|
| A.13.1.1 | Network controls | ✅ VPC, security groups, WAF | ✅ Implemented |
| A.13.1.2 | Security of network services | ✅ TLS 1.3, encrypted communications | ✅ Implemented |
| A.13.1.3 | Segregation in networks | ✅ Private subnets for database | ✅ Implemented |
| A.13.2.1 | Information transfer policies | Data transfer security policy | ❌ Need policy |
| A.13.2.2 | Agreements on information transfer | Data sharing agreements | ❌ Need agreements |
| A.13.2.3 | Electronic messaging | Secure communication policy | ❌ Need policy |
| A.13.2.4 | Confidentiality agreements | NDAs for employees/vendors | ⚠️ Company-dependent |

**Communications Security Domain:** 60% compliant

---

### A.14: System Acquisition, Development and Maintenance

| Control | Requirement | Vaultwarden Implementation | Status |
|---------|------------|---------------------------|--------|
| A.14.1.1 | Information security requirements | Security requirements in projects | ⚠️ Partially |
| A.14.1.2 | Securing application services | ✅ Vaultwarden security features | ✅ Implemented |
| A.14.1.3 | Protecting application services transactions | ✅ TLS, authentication | ✅ Implemented |
| A.14.2.1 | Secure development policy | Secure coding standards | ❌ Need policy |
| A.14.2.2 | System change control procedures | ✅ Git, PR reviews, CI/CD | ✅ Implemented |
| A.14.2.3 | Technical review after changes | Code review process | ✅ Implemented (PR) |
| A.14.2.4 | Restrictions on changes | Production change controls | ⚠️ Partially |
| A.14.2.5 | Secure system engineering principles | Infrastructure as Code principles | ✅ Implemented |
| A.14.2.6 | Secure development environment | Isolated development environment | ⚠️ Recommended |
| A.14.2.7 | Outsourced development | Vendor security requirements | ❌ If applicable |
| A.14.2.8 | System security testing | Security testing in CI/CD | ⚠️ Partially |
| A.14.2.9 | System acceptance testing | Acceptance criteria | ❌ Need criteria |
| A.14.3.1 | Protection of test data | Use synthetic data in testing | ⚠️ Recommended |

**System Development Domain:** 60% compliant

---

### A.16: Information Security Incident Management

| Control | Requirement | Vaultwarden Implementation | Status |
|---------|------------|---------------------------|--------|
| A.16.1.1 | Responsibilities and procedures | Incident response plan | ❌ Need formal plan |
| A.16.1.2 | Reporting information security events | Incident reporting procedure | ❌ Need procedure |
| A.16.1.3 | Reporting information security weaknesses | Vulnerability reporting | ❌ Need procedure |
| A.16.1.4 | Assessment and decision on events | Incident classification | ❌ Need process |
| A.16.1.5 | Response to security incidents | ✅ Automated alerting | ⚠️ Partially |
| A.16.1.6 | Learning from incidents | Post-incident review | ❌ Need process |
| A.16.1.7 | Collection of evidence | Evidence preservation procedures | ❌ Need procedures |

**Incident Management Domain:** 30% compliant

---

### A.17: Business Continuity Management

| Control | Requirement | Vaultwarden Implementation | Status |
|---------|------------|---------------------------|--------|
| A.17.1.1 | Planning continuity | ✅ Multi-region deployment | ✅ Implemented |
| A.17.1.2 | Implementing continuity | ✅ Automated failover, backups | ✅ Implemented |
| A.17.1.3 | Verify, review and evaluate continuity | DR testing | ⚠️ Need regular tests |
| A.17.2.1 | Availability of information processing | ✅ High availability architecture | ✅ Implemented |

**Business Continuity Domain:** 80% compliant

---

### A.18: Compliance

| Control | Requirement | Vaultwarden Implementation | Status |
|---------|------------|---------------------------|--------|
| A.18.1.1 | Identification of applicable legislation | Document applicable laws (GDPR, etc.) | ❌ Need documentation |
| A.18.1.2 | Intellectual property rights | Software licensing compliance | ✅ Open source (MIT) |
| A.18.1.3 | Protection of records | ✅ Audit logs, backups | ✅ Implemented |
| A.18.1.4 | Privacy and protection of PII | Data privacy procedures | ❌ Need procedures |
| A.18.1.5 | Regulation of cryptographic controls | Cryptography compliance | ⚠️ Varies by jurisdiction |
| A.18.2.1 | Independent review | Annual security audits | ❌ Need audits |
| A.18.2.2 | Compliance with security policies | Policy compliance monitoring | ❌ Need monitoring |
| A.18.2.3 | Technical compliance review | Vulnerability assessments | ⚠️ Need regular scans |

**Compliance Domain:** 40% compliant

---

## Overall Compliance Readiness

### Summary by Domain

| Domain | SOC 2 | ISO 27001 |
|--------|-------|-----------|
| **Technical Controls** | 85% | 80% |
| **Access Control** | 90% | 80% |
| **Operations** | 85% | 85% |
| **Monitoring & Logging** | 90% | 85% |
| **Backup & Recovery** | 90% | 85% |
| **Change Management** | 90% | 85% |
| **Incident Response** | 40% | 30% |
| **Policies & Procedures** | 20% | 20% |
| **Risk Management** | 25% | 20% |
| **Security Awareness** | 10% | 10% |
| **Vendor Management** | 30% | 30% |
| **Business Continuity** | 85% | 80% |
| **Overall Readiness** | **60%** | **55%** |

**Key Takeaway:** Technical controls are strong (80-90%), but policies, training, and formal processes need development (10-40%).

---

## Implementation Roadmap

### Phase 1: Foundation (Months 1-2)

**Focus:** Policies, procedures, and documentation

**Tasks:**
- [ ] Develop Information Security Policy
- [ ] Develop Acceptable Use Policy
- [ ] Develop Password Policy
- [ ] Develop Incident Response Policy
- [ ] Develop Business Continuity Policy
- [ ] Develop Data Classification Policy
- [ ] Develop Change Management Policy
- [ ] Develop Risk Management Policy
- [ ] Document security roles and responsibilities
- [ ] Create asset inventory

**Deliverables:** 8 policies, organizational documentation

**Time:** 80-120 hours  
**Cost:** $10,000-20,000 (consultant) or internal effort

---

### Phase 2: Risk Assessment (Month 3)

**Focus:** Identify, analyze, and treat risks

**Tasks:**
- [ ] Conduct risk assessment workshop
- [ ] Identify information assets
- [ ] Identify threats and vulnerabilities
- [ ] Assess likelihood and impact
- [ ] Develop risk treatment plan
- [ ] Create risk register
- [ ] Get management approval

**Deliverables:** Risk register, treatment plan

**Time:** 40-60 hours  
**Cost:** $5,000-10,000

---

### Phase 3: Control Implementation (Months 4-5)

**Focus:** Implement missing controls

**Tasks:**
- [ ] Implement vendor management program
- [ ] Establish security awareness training
- [ ] Formalize incident response procedures
- [ ] Create evidence collection process
- [ ] Implement quarterly access reviews
- [ ] Set up vulnerability scanning
- [ ] Document operating procedures
- [ ] Establish business continuity testing schedule

**Deliverables:** Implemented controls, procedures

**Time:** 100-150 hours  
**Cost:** $15,000-25,000

---

### Phase 4: Evidence Collection (Months 6-8)

**Focus:** Gather evidence for audit

**Tasks:**
- [ ] Collect access review evidence
- [ ] Document security incidents (if any)
- [ ] Gather training records
- [ ] Collect change management evidence
- [ ] Document backup tests
- [ ] Collect monitoring evidence
- [ ] Prepare DR test results
- [ ] Organize all policies and procedures

**Deliverables:** Evidence binder/repository

**Time:** 60-80 hours  
**Cost:** Internal effort

---

### Phase 5: Pre-Audit Preparation (Month 9)

**Focus:** Gap remediation and readiness assessment

**Tasks:**
- [ ] Conduct internal audit/self-assessment
- [ ] Remediate identified gaps
- [ ] Prepare System and Organization Controls (SOC) description
- [ ] Prepare Statement of Applicability (ISO)
- [ ] Brief audit team (select auditor)
- [ ] Schedule audit

**Deliverables:** Audit readiness

**Time:** 60-80 hours  
**Cost:** $5,000-10,000

---

### Phase 6: Audit (Months 10-11)

**Focus:** Third-party audit

**Tasks:**
- [ ] Provide documentation to auditor
- [ ] Respond to auditor requests
- [ ] Conduct audit interviews
- [ ] Provide access to systems (read-only)
- [ ] Demonstrate controls
- [ ] Address findings

**Deliverables:** Audit report

**Time:** Auditor-driven  
**Cost:** $15,000-35,000 (SOC 2 Type II) or $20,000-50,000 (ISO 27001)

---

### Phase 7: Continuous Compliance (Month 12+)

**Focus:** Maintain certification

**Tasks:**
- [ ] Conduct quarterly access reviews
- [ ] Annual security training
- [ ] Annual policy reviews
- [ ] Quarterly DR tests
- [ ] Monthly vulnerability scans
- [ ] Continuous monitoring
- [ ] Incident management
- [ ] Annual risk assessment
- [ ] Annual re-audit (SOC 2) or surveillance audit (ISO)

**Deliverables:** Ongoing compliance

**Time:** 10-20 hours/month  
**Cost:** $10,000-20,000/year (re-audit)

---

## Cost Breakdown

### Initial Certification (Year 1)

**Consultant/Internal Effort:**
- Policy development: $10,000-20,000
- Risk assessment: $5,000-10,000
- Control implementation: $15,000-25,000
- Pre-audit preparation: $5,000-10,000

**Audit Costs:**
- SOC 2 Type II: $15,000-35,000
- ISO 27001: $20,000-50,000
- Both: $35,000-70,000

**Tools & Services:**
- Compliance management platform: $3,000-10,000/year
- Vulnerability scanning: $2,000-5,000/year
- Security training platform: $1,000-3,000/year

**Total Year 1:**
- SOC 2 only: $51,000-103,000
- ISO 27001 only: $56,000-118,000
- Both certifications: $71,000-138,000

---

### Ongoing Costs (Year 2+)

**Maintenance:**
- Internal effort: $15,000-30,000/year
- Compliance platform: $3,000-10,000/year
- Security tools: $3,000-8,000/year

**Re-Audit:**
- SOC 2 Type II (annual): $15,000-30,000
- ISO 27001 surveillance (annual): $10,000-20,000

**Total Year 2+:**
- SOC 2 only: $36,000-78,000/year
- ISO 27001 only: $31,000-68,000/year
- Both certifications: $46,000-96,000/year

---

## Evidence Collection Guide

### What Auditors Want to See

**1. Policies & Procedures**
- All security policies (approved, signed)
- Policy review records
- Policy distribution records

**2. Risk Management**
- Risk register (current)
- Risk assessment methodology
- Risk treatment plans
- Management approval

**3. Access Control**
- User provisioning records
- User deprovisioning records
- Access review results (quarterly)
- Privileged access management

**4. Security Monitoring**
- Monitoring dashboard screenshots
- Alert configurations
- Security incidents (if any)
- Incident response records

**5. Change Management**
- Change request records
- Change approvals
- Change implementation evidence
- Rollback procedures

**6. Backup & Recovery**
- Backup logs (daily)
- Restore test results (quarterly)
- DR test results (annual)

**7. Security Awareness**
- Training materials
- Training attendance records
- Training completion certificates
- Phishing simulation results

**8. Vendor Management**
- Vendor list
- Vendor security assessments
- Vendor contracts (security clauses)
- Vendor audit rights

**9. Incident Management**
- Incident log (may be empty)
- Incident response procedures
- Post-incident reviews

**10. Physical Security**
- Cloud provider SOC 2 reports
- Office access control (if applicable)
- Device management policy

---

## Audit Preparation Checklist

### 3 Months Before Audit

- [ ] Select audit firm
- [ ] Define audit scope
- [ ] Review contracts
- [ ] Assign internal audit coordinator
- [ ] Schedule kickoff meeting
- [ ] Begin evidence collection

### 2 Months Before Audit

- [ ] Complete evidence organization
- [ ] Conduct internal audit
- [ ] Remediate gaps
- [ ] Prepare system description (SOC) or SoA (ISO)
- [ ] Schedule audit dates
- [ ] Brief management

### 1 Month Before Audit

- [ ] Provide documentation to auditor
- [ ] Respond to pre-audit questions
- [ ] Prepare staff for interviews
- [ ] Test access for auditor
- [ ] Final gap review

### During Audit (2-4 weeks)

- [ ] Opening meeting
- [ ] Documentation review
- [ ] Staff interviews
- [ ] System demonstrations
- [ ] Control testing
- [ ] Daily debriefs
- [ ] Address findings
- [ ] Closing meeting

### After Audit (2-4 weeks)

- [ ] Receive draft report
- [ ] Review for accuracy
- [ ] Provide comments
- [ ] Receive final report
- [ ] Communicate to stakeholders
- [ ] Plan for continuous compliance

---

## Common Audit Findings (and How to Avoid Them)

### Finding 1: Incomplete Policy Documentation

**Issue:** Policies missing or not approved by management

**How to Avoid:**
- ✅ Develop all required policies
- ✅ Get management sign-off
- ✅ Document approval date
- ✅ Distribute to all staff

---

### Finding 2: Lack of Access Reviews

**Issue:** User access not reviewed regularly

**How to Avoid:**
- ✅ Schedule quarterly access reviews
- ✅ Document review results
- ✅ Remediate excessive access
- ✅ Keep records for audit

---

### Finding 3: No Security Training

**Issue:** Staff not trained on security policies

**How to Avoid:**
- ✅ Implement annual security training
- ✅ Track completion
- ✅ Test comprehension
- ✅ Keep certificates

---

### Finding 4: Incomplete Risk Assessment

**Issue:** Risk assessment not thorough or not current

**How to Avoid:**
- ✅ Conduct comprehensive risk assessment
- ✅ Update annually
- ✅ Document methodology
- ✅ Get management approval

---

### Finding 5: Weak Incident Response

**Issue:** No formal incident response procedures

**How to Avoid:**
- ✅ Develop incident response plan
- ✅ Define incident classification
- ✅ Establish communication plan
- ✅ Conduct tabletop exercises

---

### Finding 6: Insufficient Monitoring

**Issue:** Security events not adequately monitored

**How to Avoid:**
- ✅ Implement comprehensive monitoring (done!)
- ✅ Document monitoring procedures
- ✅ Review alerts regularly
- ✅ Keep alert history

---

### Finding 7: No DR Testing

**Issue:** Disaster recovery not tested

**How to Avoid:**
- ✅ Document DR procedures
- ✅ Test annually (minimum)
- ✅ Document test results
- ✅ Remediate gaps

---

### Finding 8: Vendor Management Gaps

**Issue:** Vendors not assessed for security

**How to Avoid:**
- ✅ Maintain vendor inventory
- ✅ Assess vendor security (questionnaires)
- ✅ Include security clauses in contracts
- ✅ Monitor vendor compliance

---

## Compliance Management Tools

### Recommended Platforms

**1. Vanta**
- **Purpose:** Automated compliance monitoring
- **Features:** Connects to cloud infrastructure, automates evidence collection
- **Certifications:** SOC 2, ISO 27001, HIPAA, PCI DSS
- **Cost:** $4,000-10,000/year
- **Best For:** Growing companies, automated compliance

**2. Drata**
- **Purpose:** Continuous compliance automation
- **Features:** Real-time monitoring, automated evidence
- **Certifications:** SOC 2, ISO 27001, HIPAA, GDPR
- **Cost:** $3,000-8,000/year
- **Best For:** Fast-growing startups, tech companies

**3. Secureframe**
- **Purpose:** Compliance automation and monitoring
- **Features:** Policy management, training, evidence collection
- **Certifications:** SOC 2, ISO 27001, HIPAA, PCI DSS
- **Cost:** $3,500-9,000/year
- **Best For:** Security-focused companies

**4. TrustCloud**
- **Purpose:** Compliance management platform
- **Features:** Policy templates, evidence collection, audit management
- **Certifications:** SOC 2, ISO 27001, HIPAA
- **Cost:** $2,500-6,000/year
- **Best For:** Budget-conscious companies

**5. Manual Process**
- **Purpose:** Self-managed compliance
- **Tools:** Spreadsheets, Google Drive, project management
- **Cost:** Free (internal time only)
- **Best For:** Small teams, limited budget

**Recommendation:** Start with manual process, adopt tool when budget allows (100+ users or $1M+ revenue)

---

## FAQ

**Q: Do I need both SOC 2 and ISO 27001?**  
A: Most companies start with SOC 2 (faster, cheaper). Add ISO 27001 for international customers.

**Q: How long does certification take?**  
A: 9-12 months from start to audit completion. SOC 2 Type II requires 6 months of control operation.

**Q: Can I get certified with 100% self-hosted (no cloud)?**  
A: Yes, but physical security controls become your responsibility. Cloud providers make this easier.

**Q: What if I find a security incident during the audit period?**  
A: Document it thoroughly, show incident response, demonstrate lessons learned. Incidents don't fail audits; poor response does.

**Q: Can I pause my certification?**  
A: No. SOC 2 requires annual re-audit. ISO 27001 requires annual surveillance audits. Let it lapse = start over.

**Q: How much work is continuous compliance?**  
A: 10-20 hours/month for small companies, 1-2 FTE for large companies.

**Q: What happens if I fail the audit?**  
A: Auditor identifies findings. You remediate. Re-audit specific areas. Most companies pass eventually.

**Q: Do I need a dedicated compliance person?**  
A: Part-time (10-20 hours/week) for small companies, full-time for large companies (500+ users).

---

## Next Steps

### Immediate (This Week)

1. **Assess readiness:** Review control mappings above
2. **Decide scope:** SOC 2, ISO 27001, or both?
3. **Budget approval:** $70k-140k year 1, $50k-100k ongoing
4. **Select approach:** DIY, consultant, or compliance platform
5. **Assign owner:** Who will lead compliance effort?

### Short Term (Months 1-3)

6. **Develop policies:** All required policies and procedures
7. **Conduct risk assessment:** Identify and document risks
8. **Select auditor:** Get quotes from 3-5 audit firms

### Medium Term (Months 4-9)

9. **Implement controls:** Fill gaps identified
10. **Collect evidence:** Organize for audit
11. **Pre-audit preparation:** Self-assessment and remediation

### Long Term (Months 10-12+)

12. **Audit:** Complete certification audit
13. **Continuous compliance:** Maintain certification
14. **Communicate:** Share certification with customers

---

## Conclusion

**Your Vaultwarden deployment is 60% ready for SOC 2 and 55% ready for ISO 27001.**

**Strong areas:**
- ✅ Technical security controls (80-90%)
- ✅ Access control (80-90%)
- ✅ Monitoring and logging (85-90%)
- ✅ Backup and disaster recovery (80-90%)
- ✅ Change management (85-90%)

**Areas needing development:**
- ❌ Policies and procedures (20%)
- ❌ Risk management (20-25%)
- ❌ Security awareness training (10%)
- ❌ Formal incident response (30-40%)
- ❌ Vendor management (30%)

**Recommended path:**
1. **Month 1-3:** Develop policies and conduct risk assessment
2. **Month 4-6:** Implement missing controls
3. **Month 7-9:** Evidence collection and pre-audit prep
4. **Month 10-12:** Audit and certification

**Investment:**
- **Year 1:** $70,000-140,000 (certification)
- **Year 2+:** $50,000-100,000/year (maintenance)

**ROI:** Required for enterprise customers, enables higher contract values, builds trust, reduces security risk

**Next action:** Decide on certification scope (SOC 2, ISO 27001, or both) and assign compliance owner.

---

**Document Version:** 1.0  
**Last Updated:** November 5, 2025  
**Next Review:** Quarterly during certification process

**Questions?** adrian207@gmail.com

