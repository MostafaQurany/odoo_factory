# Reference: Security, Access Rights & Approvals

## Security Architecture in Factory Platform

### Role Segregation
1. **Operator (`group_factory_user`):**
   - Access: View assigned Work Orders, record production quantities, report scrap.
   - Forbidden: Approving MOs, adjusting standard costs, viewing customer invoices.
2. **Quality Inspector (`group_factory_quality`):**
   - Access: Inspect incoming receipts, in-process check points, final goods inspection.
   - Forbidden: Modifying financial ledgers, creating sales orders.
3. **Process Engineer (`group_factory_engineer`):**
   - Access: Manage BOMs, configure work center capacities, maintain routings.
4. **Factory Manager (`group_factory_manager`):**
   - Full operational access across manufacturing, inventory, and procurement.

### Rule for Adding Models
Whenever creating a new model `x_factory_*`:
1. Add entry in `security/ir.model.access.csv`.
2. Define record rules if multi-company or department separation applies.
