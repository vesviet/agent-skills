# Alistair Cockburn Scoping & The 13-Field Use Case Standard

> Authoritative reference guide for Use Case engineering based on Alistair Cockburn's *Writing Effective Use Cases* and Karl Wiegers' / IIBA industry standard template.

---

## 1. Alistair Cockburn Scoping Framework

### The Coffee-Break Test (Elementary Business Process)
An Elementary Business Process (EBP) is a task performed by one person in one place at one time, in response to a business event, which adds measurable business value and leaves the data in a consistent state.

```
[ Too Large: Summary Level ] ──► "Recruit New Faculty Member" (Takes weeks, involves multiple departments)
     │
     ▼  Decomposes into User-Goal Level (The Sweet Spot)
[ Just Right: Blue Level ]   ──► "Submit Faculty Application" (Done in one sitting, 15 minutes)
[ Just Right: Blue Level ]   ──► "Approve Faculty Application" (Dean reviews and signs off, 10 minutes)
     │
     ▼  Decomposes into Subfunction Level
[ Too Small: Black Level ]   ──► "Validate Captcha", "Upload Resume PDF" (Steps within a Use Case)
```

### The 3 Goal Levels

| Icon | Level | Cockburn Altitude | Description & Criterion |
|:---:|---|---|---|
| 🌊 | **Summary** | White / Cloud / Kite | Enterprise or cross-departmental lifecycle; encompasses multiple user goals. |
| 🎯 | **User-Goal** | Blue / Sea Level | **The primary target for software requirements.** Delivers immediate user value; satisfies coffee-break test. |
| 🐟 | **Subfunction** | Black / Underwater | Sub-step; does not deliver standalone business value outside the parent Use Case context. |

---

## 2. Karl Wiegers 13-Field Use Case Template

```markdown
# UC-[MODULE]-[NUM]: [Active Verb + Noun Title]

## 1. Metadata
- **Use Case ID**: UC-FIN-003
- **Title**: Approve Commercial Loan Application
- **Scope**: Commercial Banking Platform
- **Goal Level**: User-Goal Level (Blue)
- **Primary Actor**: Senior Underwriter
- **Secondary Actors**: Core Banking Ledger API, Risk Scoring Engine

## 2. Preconditions
- Underwriter is authenticated with Level 3 credit approval permissions.
- Loan application status is "Underwriting Queue - Pending Review".
- Risk score report has been generated and attached to the loan dossier.

## 3. Trigger
- Underwriter selects "Review Application" from the active underwriting queue.

## 4. Normal Course (Happy Path)
1. System displays loan dossier, credit report, and automated risk scoring breakdown.
2. Underwriter reviews financial statements and confirms regulatory compliance.
3. Underwriter enters approval notes and selects approved credit limit.
4. System validates approved credit limit against Underwriter's authorization matrix.
5. System records loan approval, updates application status to "Approved - Awaiting Disbursal".
6. System dispatches approval confirmation notice to Applicant and Loan Officer.
7. System generates binding commitment letter and queues for e-signature.

## 5. Alternative Courses
- **3a. Underwriter requests additional collateral documentation**:
  - 3a1. Underwriter specifies missing documentation checklist and sets 5-business-day hold.
  - 3a2. System updates status to "Information Requested" and notifies Applicant.
  - 3a3. Use Case ends at Minimal Guarantee state.
- **4a. Approved amount exceeds Underwriter authorization limit**:
  - 4a1. System prompts for Senior Credit Committee escalation.
  - 4a2. Underwriter attaches recommendation brief and escalates.
  - 4a3. System assigns dossier to Credit Committee queue; Use Case ends.

## 6. Exception Courses (Failure Modes)
- **4b. Credit audit reveals active sanction or fraud match**:
  - 4b1. System freezes dossier immediately.
  - 4b2. System logs security event to Fraud Operations and alerts Compliance Officer.
  - 4b3. System terminates approval workflow; status set to "Suspended - Fraud Review".
- **6a. Notification service timeout (downstream external dependency failure)**:
  - 6a1. System queues message in resilient outbox for retry with exponential backoff.
  - 6a2. System logs warning to observability pipeline and continues workflow.

## 7. Postconditions
- **Success Guarantee**: Loan status is "Approved - Awaiting Disbursal", audit trail records underwriter ID and timestamp, commitment letter generated.
- **Minimal / Failure Guarantee**: If rejected or suspended, application state is locked with reasons recorded; no credit limit or fund disbursement authorization is issued.

## 8. Business Rules
- `BR-CR-012`: Underwriters may approve uncollateralized credit up to their authorized tier limit without dual sign-off.
- `BR-KYC-004`: Any international applicant requires enhanced due diligence (EDD) verification before approval.

## 9. Assumptions & Open Questions
- Assumption: Downstream core banking ledger operates with idempotent transaction submission.
```

---

## 3. The 10 Use Case Writing Anti-Patterns

| # | Anti-Pattern | Bad Example | Corrected Standard | Rationale |
|---|---|---|---|---|
| 1 | **UI Prescriptions** | *"User clicks on blue Submit button"* | *"User submits payment authorization"* | UI layouts change; business intent remains stable. |
| 2 | **Embedded If/Else** | *"Step 4: If balance > 100 system deducts, else system errors"* | Move condition to Alternative `4a` and Exception `4b` | Keeps normal course clean and readable. |
| 3 | **Generic Actors** | *"User views account details"* | *"Account Holder views account details"* | Obscures permissions and role boundaries. |
| 4 | **Missing Failure State** | Only writes steps 1-5 with no exceptions | Specify at least 2 realistic failure branches | Software engineering spends 80% time on exceptions. |
| 5 | **Precondition as Rule** | Precondition: *"User must be over 18"* | Precondition: *"User age is verified"*; Rule: `BR-01` | Preconditions are states; rules are logic constraints. |
| 6 | **Too Fine-Grained** | Use case for "Enter Password" | Step inside "Authenticate User" | Clutters specification with subfunction trivia. |
| 7 | **System Silence** | 4 actor steps in a row without system feedback | Alternate actor action and system response | Use cases are dialogues between actor and system. |
| 8 | **Vague Outcomes** | Postcondition: *"System is updated"* | Postcondition: *"Order status is Paid; inventory -1"* | Unverifiable postconditions break QA test authoring. |
| 9 | **Passive Voice** | *"The invoice is processed by the application"* | *"System validates invoice line items"* | Passive voice hides who is responsible for the action. |
| 10 | **Orphaned Steps** | Branch `3a` has no return or termination point | Explicitly end branch or specify `Return to Step 4` | Loose branches cause unhandled states in code. |

---

## 4. 20-Point Quality Checklist

Every Use Case must achieve **>= 18/20** to pass the Quality Gate:
1. [ ] Title is Active Verb + Noun phrase
2. [ ] Primary Actor has a distinct domain role (not generic "User")
3. [ ] Goal level is Blue / User-Goal (satisfies coffee-break test)
4. [ ] System boundary is clear (actor tasks vs system tasks separated)
5. [ ] Trigger event is unambiguous and singular
6. [ ] Preconditions describe true system states, not business rules
7. [ ] Preconditions are verifiable prior to step 1
8. [ ] Normal course contains 3 to 9 numbered atomic steps
9. [ ] Steps alternate between Actor action and System response
10. [ ] Steps are written in active voice, present tense
11. [ ] Zero UI/GUI widget prescriptions (no clicks, dropdowns, buttons)
12. [ ] Zero nested if/else or loops in the normal course
13. [ ] Alternative courses explicitly branch from a numbered normal step
14. [ ] Exception courses explicitly branch from a numbered normal step
15. [ ] Every branch clearly defines return step or terminal end-state
16. [ ] Success guarantee defines exact state of system upon completion
17. [ ] Minimal (failure) guarantee defines protected state upon error
18. [ ] Business rules are referenced by ID, not embedded in course text
19. [ ] Non-functional requirements (SLAs, latency) separated from flow
20. [ ] Assumptions and open questions explicitly surfaced
