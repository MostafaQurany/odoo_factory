# Workflow: Modify QWeb Report

```text
Locate Report Action -> Locate QWeb Template -> Verify Model Fields -> Inherit Template -> Upgrade -> Render PDF Test
```

1. **Locate Report Action & Template:**
   - Example: Sales Invoice `account.report_invoice_document` or Delivery Slip `stock.report_deliveryslip`.
2. **Field Existence Check:**
   - Confirm all fields you plan to render exist on the corresponding model.
   - If not, implement `workflows/add-field.md` first!
3. **Inherit QWeb Template in `custom/factory_reports` or target addon:**
   ```xml
   <template id="report_delivery_slip_inherit_factory" inherit_id="stock.report_delivery_document">
       <xpath expr="//table[@name='stock_move_table']/thead/tr" position="inside">
           <th>Inspection Status</th>
       </xpath>
       <xpath expr="//table[@name='stock_move_table']/tbody/tr" position="inside">
           <td><span t-field="move.quality_state"/></td>
       </xpath>
   </template>
   ```
4. **Upgrade & Verify:**
   - Upgrade addon: `./scripts/bootstrap.ps1 -Update -Modules <addon_name>`.
   - Run scenario: `python scripts/factory/run_scenario.py -s GX-002`.
