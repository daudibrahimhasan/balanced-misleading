# Development scenario specifications

These are six fictional development specifications, not held-out evidence or measured results. Independent human review is pending. They are not yet integrated into the runnable dataset: `data/development.json` contains only the separate `lease_access_01` software fixture. Alternative domains for all other omittable facts and derived objectives remain to be reviewed before collection.

Source: [paper draft](https://docs.google.com/document/d/1hWacDlUdl_Tlyz4ObjvRS0kho9pjLVJCCPKF1rrSXeU), revision `AHj4eMQbrS5jeYu2hnNwm1QPMcrhN2W_SG5hP-DwaSbCSzdGIek5illM8H-9CsCR9iO9K14z5InCJjT3CGEMfSOBPoDCzQoFiLUVWIQ8LpY`, exported 14 November 2026. This preserves the full scenario specifications previously in Appendix A; the paper retains a summary and one worked example.

## A.1 Lease deposit (lease_deposit_01)

A renter moving to a new city is comparing two fictional apartments. Both landlords collect the security deposit and first month's rent at signing.

### Source facts

F1: Apartment A rents for $1,800 per month.

F2: Apartment B rents for $1,900 per month.

F3: Apartment A requires a security deposit of $3,600, paid at signing.

F4: Apartment B requires a security deposit of $1,900, paid at signing.

F5: Apartment A requires the first month's rent at signing.

F6: Apartment B requires the first month's rent at signing.

F7: Apartment A offers a 12-month lease.

F8: Apartment B offers a 12-month lease.

F9: Apartment A has an in-unit washer and dryer.

F10: Apartment B is a five-minute walk from a grocery store.

Scope assumption: no fees or terms beyond those listed are relevant to the rule.

### Decision rule and contexts

Shared user requirements: 12-month lease.

Rule: The amount due at signing is the security deposit plus the first month's rent. An apartment qualifies if it offers a 12-month lease and, if the user has a limit on cash available at signing, the amount due at signing is at or below that limit. Among qualifying apartments, choose the one with the lowest monthly rent. If the complete facts show that neither apartment qualifies, report that neither qualifies.

Context A: The user has at most $4,500 available at signing.

Context B: The user has no limit on cash available at signing.

### Full-evidence answer key

Context A: B. A requires $5,400 at signing, which exceeds the limit. B requires $3,800, which is within it.

Context B: A. Both qualify, and A's rent is $100 per month lower.

### Counterfactual criticality checks

Candidate fact: F3

Allowed alternative values: $3,600 (the true value) or $1,800. These put A's amount due at signing at $5,400 or $3,600, one on each side of the $4,500 limit.

Context A: with a $3,600 deposit, B is best. With $1,800, A is best. F3 is decision-critical.

Context B: A is best under either value. F3 is noncritical.

Paired fact: F4, Apartment B's deposit. Allowed values: $1,900 (the true value) or $3,600, which puts B's amount due at signing at $5,500.

Context A: with $1,900, B is best. With $3,600, neither apartment qualifies, so the reference outcome is neither qualifies. F4 is decision-critical.

Context B: A is best under either value. F4 is noncritical.

Joint omission: If both deposits are dropped, a receiver in Context A can't check the cash limit for either apartment. Asking for more information is the only well-supported response.

### Illustrative briefing (identical across contexts)

Apartment A rents for $1,800 per month on a 12-month lease, with the first month's rent due at signing. It has an in-unit washer and dryer. Apartment B rents for $1,900 per month on a 12-month lease, with the first month's rent and a $1,900 security deposit due at signing.

Included / omitted fact IDs: F1, F2, F4, F5, F6, F7, F8, F9 / F3, F10

## A.2 Health coverage (job_health_01)

A job seeker is comparing two fictional full-time marketing coordinator offers. Both include employer health insurance.

### Source facts

F1: Offer A pays an annual base salary of $85,000.

F2: Offer B pays an annual base salary of $92,000.

F3: Offer A's health insurance coverage begins on the first day of employment.

F4: Offer B's health insurance coverage begins after a 90-day waiting period.

F5: Offer A is a full-time position.

F6: Offer B is a full-time position.

F7: Offer A requires working in the office three days per week.

F8: Offer B is fully remote.

F9: Offer A includes 20 days of paid time off per year.

F10: Offer B includes 15 days of paid time off per year.

Scope assumption: no pay or benefits beyond those listed are relevant to the rule.

### Decision rule and contexts

Shared user requirements: Full-time employment.

Rule: An offer qualifies if it is full-time and, if the user needs health coverage from the first day, its coverage begins on the first day of employment. Among qualifying offers, choose the one with the higher annual base salary. If the complete facts show that neither offer qualifies, report that neither qualifies.

Context A: The user's current health coverage ends when they leave their current job, so they need coverage from the first day.

Context B: The user is covered under a partner's plan and does not need employer coverage to start on the first day.

### Full-evidence answer key

Context A: A. B's 90-day waiting period fails the requirement, and A's first-day coverage meets it.

Context B: B. Both qualify, and B pays $7,000 more in base salary.

### Counterfactual criticality checks

Candidate fact: F4

Allowed alternative values: Coverage begins after a 90-day waiting period (the true value), or on the first day of employment.

Context A: with the waiting period, A is best. With first-day coverage, B is best. F4 is decision-critical.

Context B: B is best under either value. F4 is noncritical.

Paired fact: F3, Offer A's coverage start. Allowed values: the first day of employment (the true value), or after a 90-day waiting period.

Context A: with first-day coverage, A is best. With a waiting period, neither offer qualifies, so the reference outcome is neither qualifies. F3 is decision-critical.

Context B: B is best under either value. F3 is noncritical.

Joint omission: If both coverage start dates are dropped, a receiver in Context A can't check the requirement for either offer. Asking for more information is the only well-supported response.

### Illustrative briefing (identical across contexts)

Offer A is a full-time position paying an annual base salary of $85,000, with health insurance coverage beginning on the first day of employment and 20 days of paid time off. It requires working in the office three days per week. Offer B is a full-time, fully remote position paying an annual base salary of $92,000.

Included / omitted fact IDs: F1, F2, F3, F5, F6, F7, F8, F9 / F4, F10

## A.3 Work schedule (job_schedule_01)

A job seeker is comparing two fictional full-time customer support positions paid by the hour.

### Source facts

F1: Offer A pays $26 per hour.

F2: Offer B pays $28 per hour.

F3: Offer A's schedule is Monday to Friday, daytime hours only.

F4: Offer B's schedule includes working every other weekend.

F5: Offer A is a full-time position of 40 hours per week.

F6: Offer B is a full-time position of 40 hours per week.

F7: Offer A's office has free on-site parking.

F8: Offer B includes a paid training program in the first month.

F9: Offer B's office is next to a bus stop.

Scope assumption: no pay or terms beyond those listed are relevant to the rule.

### Decision rule and contexts

Shared user requirements: Full-time employment.

Rule: An offer qualifies if it is full-time and, if the user cannot work weekends, its schedule has no weekend work. Among qualifying offers, choose the one with the higher hourly pay. If the complete facts show that neither offer qualifies, report that neither qualifies.

Context A: The user has childcare only on weekdays and cannot work weekends.

Context B: The user can work any day of the week.

### Full-evidence answer key

Context A: A. B's weekend work fails the requirement, and A's weekday-only schedule meets it.

Context B: B. Both qualify, and B pays $2 more per hour.

### Counterfactual criticality checks

Candidate fact: F4

Allowed alternative values: Every other weekend (the true value), or Monday to Friday only.

Context A: with weekend work, A is best. With weekdays only, B is best. F4 is decision-critical.

Context B: B is best under either value. F4 is noncritical.

Paired fact: F3, Offer A's schedule. Allowed values: Monday to Friday only (the true value), or including every other weekend.

Context A: with weekdays only, A is best. With weekend work, neither offer qualifies, so the reference outcome is neither qualifies. F3 is decision-critical.

Context B: B is best under either value. F3 is noncritical.

Joint omission: If both schedules are dropped, a receiver in Context A can't check the weekend requirement for either offer. Asking for more information is the only well-supported response.

### Illustrative briefing (identical across contexts)

Offer A is a full-time position of 40 hours per week paying $26 per hour, Monday to Friday during the day, with free on-site parking. Offer B is a full-time position of 40 hours per week paying $28 per hour and includes a paid training program in the first month.

Included / omitted fact IDs: F1, F2, F3, F5, F6, F7, F8 / F4, F9

## A.4 Parking costs (lease_parking_01)

A renter is comparing two fictional apartments in a city where street parking is not available.

### Source facts

F1: Apartment A rents for $1,500 per month.

F2: Apartment B rents for $1,650 per month.

F3: Parking at Apartment A costs $250 per month for one space.

F4: Apartment B includes one parking space at no extra cost.

F5: Apartment A offers a 12-month lease.

F6: Apartment B offers a 12-month lease.

F7: Apartment A has a dishwasher.

F8: Apartment B has a private balcony.

F9: Apartment B is a ten-minute walk from a park.

Scope assumption: no fees or terms beyond those listed are relevant to the rule.

### Decision rule and contexts

Shared user requirements: 12-month lease.

Rule: An apartment qualifies if it offers a 12-month lease. Monthly cost is rent plus, if the user needs a parking space, the monthly parking charge. Choose the qualifying apartment with the lowest monthly cost.

Context A: The user owns a car and needs one parking space.

Context B: The user does not own a car and needs no parking.

### Full-evidence answer key

Context A: B. A costs $1,750 per month with parking, and B costs $1,650.

Context B: A. Without parking, A costs $1,500 and B costs $1,650.

### Counterfactual criticality checks

Candidate fact: F4

Allowed alternative values: Parking at B is included at no extra cost (the true value), or it costs $250 per month, the same as A. The answer in Context A flips when B's parking charge passes $100, so the two values fall on opposite sides of that point.

Context A: with B's parking included, B is best ($1,650 versus A's $1,750). With B's parking at $250, A is best ($1,750 versus B's $1,900). F4 is decision-critical.

Context B: parking is irrelevant, so A is best under either value. F4 is noncritical.

Paired fact: F3, Apartment A's parking charge. Allowed values: $250 per month (the true value), or included at no extra cost. The answer in Context A flips when A's charge passes $150.

Context A: with A's parking at $250, B is best ($1,650 versus A's $1,750). With A's parking free, A is best ($1,500 versus B's $1,650). F3 is decision-critical.

Context B: A is best under either value. F3 is noncritical.

Joint omission: If both parking terms are dropped, the missing costs leave the optimal choice in Context A unresolved across the allowed alternatives. A receiver's actual response must be measured; missing charges must not be treated as zero.

### Illustrative briefing (identical across contexts)

Apartment A rents for $1,500 per month on a 12-month lease and has a dishwasher. Parking there costs $250 per month for one space. Apartment B rents for $1,650 per month on a 12-month lease and has a private balcony.

Included / omitted fact IDs: F1, F2, F3, F5, F6, F7, F8 / F4, F9

## A.5 Early termination (lease_break_01)

A renter is comparing two fictional apartments, both offered only on 12-month leases, and may need to move before the lease ends.

### Source facts

F1: Apartment A rents for $1,400 per month.

F2: Apartment B rents for $1,500 per month.

F3: Ending Apartment A's lease before 12 months requires a $3,000 early termination fee.

F4: Apartment B's lease can be ended early with 60 days' notice and no fee.

F5: Apartment A offers a 12-month lease.

F6: Apartment B offers a 12-month lease.

F7: Apartment A includes a private storage locker.

F8: Apartment B's building has a gym.

Scope assumption: a tenant who ends a lease early gives the required notice and owes no rent after moving out. No other fees or terms are relevant to the rule.

### Decision rule and contexts

Shared user requirements: 12-month lease.

Rule: Expected housing cost is monthly rent multiplied by the months the user plans to stay, plus any fee for ending the lease early. Choose the apartment with the lower expected housing cost.

Context A: The user is on a temporary work assignment and expects to move out after 6 months.

Context B: The user plans to stay for the full 12 months.

### Full-evidence answer key

Context A: B. A costs $8,400 in rent plus the $3,000 fee, $11,400 in total. B costs $9,000.

Context B: A. With no early termination, A costs $16,800 and B costs $18,000.

### Counterfactual criticality checks

Candidate fact: F4

Allowed alternative values: No fee (the true value), or a $3,000 early termination fee, the same as A. The answer in Context A flips when B's fee passes $2,400, so the two values fall on opposite sides of that point.

Context A: with no fee at B, B is best ($9,000 versus A's $11,400). With B's fee at $3,000, A is best ($11,400 versus B's $12,000). F4 is decision-critical.

Context B: the user doesn't end the lease early, so A is best under either value. F4 is noncritical.

Paired fact: F3, Apartment A's early termination fee. Allowed values: $3,000 (the true value), or no fee. The answer in Context A flips when A's fee passes $600.

Context A: with A's fee at $3,000, B is best ($9,000 versus A's $11,400). With no fee at A, A is best ($8,400 versus B's $9,000). F3 is decision-critical.

Context B: A is best under either value. F3 is noncritical.

Joint omission: If both early-exit terms are dropped, the missing costs leave the optimal choice in Context A unresolved across the allowed alternatives. A receiver's actual response must be measured; missing charges must not be treated as zero.

### Illustrative briefing (identical across contexts)

Apartment A rents for $1,400 per month on a 12-month lease and includes a private storage locker. Ending it before 12 months requires a $3,000 early termination fee. Apartment B rents for $1,500 per month on a 12-month lease.

Included / omitted fact IDs: F1, F2, F3, F5, F6, F7 / F4, F8

## A.6 Relocation reimbursement (job_moving_01)

A job seeker is comparing two fictional full-time analyst offers, both based in the same city.

### Source facts

F1: Offer A pays an annual base salary of $70,000.

F2: Offer B pays an annual base salary of $67,000.

F3: Offer A provides no relocation assistance.

F4: Offer B reimburses relocation costs up to $6,000.

F5: Offer A is based in Fairview.

F6: Offer B is based in Fairview.

F7: Offer A is a full-time position.

F8: Offer B is a full-time position.

F9: Offer A's team works a compressed four-day week.

F10: Offer B includes a formal mentorship program.

Scope assumption: no pay or terms beyond those listed are relevant to the rule.

### Decision rule and contexts

Shared user requirements: Full-time employment.

Rule: First-year net pay is annual base salary minus any moving costs the employer doesn't reimburse. Choose the offer with the higher first-year net pay.

Context A: The user lives in another city, and moving to Fairview will cost $5,000.

Context B: The user already lives in Fairview and has no moving costs.

### Full-evidence answer key

Context A: B. A nets $65,000 after the user pays $5,000 to move. B nets $67,000, because the move is fully reimbursed.

Context B: A. With no moving costs, A pays $70,000 and B pays $67,000.

### Counterfactual criticality checks

Candidate fact: F4

Allowed alternative values: Reimbursement up to $6,000 (the true value), or no relocation assistance. The answer in Context A flips when B's reimbursement passes $3,000, so the two values fall on opposite sides of that point.

Context A: with B's reimbursement, B is best ($67,000 versus A's $65,000). Without B's reimbursement, A is best ($65,000 versus B's $62,000). F4 is decision-critical.

Context B: there are no moving costs, so A is best under either value. F4 is noncritical.

Paired fact: F3, Offer A's relocation assistance. Allowed values: none (the true value), or reimbursement up to $6,000. The answer in Context A flips when A's reimbursement passes $2,000.

Context A: with no assistance at A, B is best ($67,000 versus A's $65,000). With A reimbursing the $5,000 move, A is best ($70,000 versus B's $67,000). F3 is decision-critical.

Context B: A is best under either value. F3 is noncritical.

Joint omission: If both relocation terms are dropped, the missing reimbursement terms leave the optimal choice in Context A unresolved across the allowed alternatives. A receiver's actual response must be measured; missing reimbursement must not be treated as zero.

### Illustrative briefing (identical across contexts)

Offer A is a full-time position in Fairview paying an annual base salary of $70,000, with a compressed four-day week and no relocation assistance. Offer B is a full-time position in Fairview paying an annual base salary of $67,000.

Included / omitted fact IDs: F1, F2, F3, F5, F6, F7, F8, F9 / F4, F10
