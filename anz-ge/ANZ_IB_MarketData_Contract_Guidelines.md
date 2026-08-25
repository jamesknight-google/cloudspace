# ANZ Banking Group — Institutional Banking & Technology Procurement
## Policy Document: Market Data & FinTech Vendor Contracting Guidelines
**Document ID:** ANZ-POL-IB-PROC-2026-V3.2  
**Effective Date:** 1 January 2026  
**Applicability:** All contracts, Master Services Agreements (MSAs), Order Forms, and End User License Agreements (EULAs) for Institutional Market Data Feeds, Pricing Engines, Low-Latency Trading APIs, and FinTech Analytics Platforms.

---

### 1. Executive Summary & Regulatory Authority
ANZ Institutional Banking relies on third-party market data, real-time pricing feeds, and quantitative analytics to service institutional clients, manage trading books, and execute foreign exchange/capital market transactions. 

All procurement contracts must comply with Australian Prudential Regulation Authority (**APRA**) standards, specifically **APRA CPS 234 (Information Security)**, **APRA CPS 230 (Operational Resilience)**, the **Australian Privacy Act 1988 (Cth)**, and internal ANZ Risk Management Frameworks.

---

### 2. Mandatory Evaluation Criteria (Rule Matrix)

When evaluating vendor contracts against this policy, the evaluating agent must assess the contract against the **Five Core Pillars** below.

| Pillar | Policy Requirement | Pass Criteria | Hard Rejection Trigger | Review Required Trigger |
| :--- | :--- | :--- | :--- | :--- |
| **1. Data Sovereignty & Hosting** | Primary production data and transactional metadata must reside within Australia. | Data Centers located in Sydney / Melbourne (AWS/GCP/Azure AU Regions or vendor-owned AU facilities). | Data stored/processed exclusively outside Australia (e.g., US, EU, Asia-Pac) without encryption isolation. | Secondary disaster recovery (DR) or cross-border failover in APRA-recognized jurisdictions (e.g., Singapore, UK) with customer notification. |
| **2. Information Security (APRA CPS 234)** | Vendor must maintain ISO 27001 / SOC 2 Type II certification, annual independent pen testing, and notify ANZ of security incidents within 24 hours. | Explicit clause guaranteeing SOC 2 / ISO 27001 + 24-hour incident notification + right for ANZ/APRA to audit. | No audit rights, no security certifications, or incident notification window > 72 hours. | Standard certifications present, but audit rights require mutual agreement or 30 days advance notice. |
| **3. Service Availability (SLA) & Credits** | Critical market data feeds require 99.99% monthly availability with financial penalty credits for downtime. | Monthly uptime SLA >= 99.99% with graduated service fee rebates (credits) on outages. | Uptime < 99.5% or contract specifically disclaims all financial credits / remedies for downtime. | Uptime between 99.90% and 99.98%, or downtime remedies limited to contract termination without rebates. |
| **4. Liability & Indemnification** | Standard aggregate liability cap must be at least 2.0x Annual Contract Value (ACV). Uncapped liability required for IP infringement, data breach, and confidentiality breaches. | Vendor liability cap >= 2x ACV, with standard unlimited carve-outs for IP indemnity, gross negligence, and breach of confidentiality. | Liability capped below 1.0x ACV, or vendor completely excludes liability for data breaches or IP infringement. | Liability cap is exactly 1.0x ACV, or includes mutual super-caps (e.g. 3x ACV) for data protection breaches. |
| **5. Governing Law & Dispute Jurisdiction** | Contracts must be governed by the laws of an Australian State (preferable New South Wales or Victoria). | Governing law: New South Wales (NSW) or Victoria (VIC), Australia, with Australian court jurisdiction. | Governing law: Foreign jurisdiction (e.g., Delaware/US, Cayman Islands) with mandatory offshore arbitration. | Governing law: England & Wales or New Zealand (requires Legal Counsel approval). |

---

### 3. Classification & Recommendation Decision Logic

The evaluating agent must categorize the evaluated contract into one of three strict states:

#### State A: APPROVAL (Compliant)
- **Condition:** Contract satisfies **all five pillars** without exception.
- **Action:** Issue **Contract Approval Memorandum**, certify APRA CPS 234/230 alignment, and forward directly to Authorized Delegate for digital execution.

#### State B: DENIAL (Non-Compliant)
- **Condition:** Contract triggers **one or more Hard Rejection triggers** (e.g., offshore data storage, no APRA audit rights, uptime < 99.5%, or liability disclaimers).
- **Action:** Issue **Formal Contract Rejection Notice** itemizing non-compliant sections, citing regulatory risk (APRA / Privacy Act), and providing remediation guidelines for vendor re-drafting.

#### State C: HUMAN-IN-THE-LOOP REVIEW (Conditional / Exception)
- **Condition:** Contract has **no Hard Rejections**, but triggers **one or more Review Required triggers** (e.g., secondary DR outside Australia, SLA between 99.90% - 99.98%, 1x ACV liability cap, or UK/NZ jurisdiction).
- **Action:** Issue **Escalation & Risk Review Brief** flagging the specific clause variances for review by the ANZ Legal & Procurement Oversight Committee prior to final sign-off.

---

### 4. Required Output Document Structure
For automated workflows, output documents generated must include:
1. **Contract Metadata:** Vendor Name, Contract Title, Agreement Effective Date, Evaluated Term, ACV.
2. **Executive Assessment Summary:** Clear verdict (**APPROVED**, **DENIED**, or **ESCALATED FOR REVIEW**).
3. **Pillar-by-Pillar Compliance Breakdown:** Itemized audit findings citing exact contract clauses.
4. **Risk & Action Matrix:** Specific next steps, sign-off requirements, or vendor renegotiation redlines.
