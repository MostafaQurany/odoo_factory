# Reference: Reporting & QWeb Customization

## Principles for Report Modification
1. **Never edit upstream report XML directly.**
2. **Locate report action & root template:** Find the QWeb report ID (e.g., `mrp.report_mrp_production`).
3. **Check underlying model fields:** If a requested column does not exist on the model, add the field to Python first!
4. **Inherit using `xpath`:**
   ```xml
   <template id="report_mrp_production_inherit_factory" inherit_id="mrp.report_mrp_production">
       <xpath expr="//div[hasclass('page')]/table/thead/tr" position="inside">
           <th>Batch Certificate</th>
       </xpath>
       <xpath expr="//div[hasclass('page')]/table/tbody/tr" position="inside">
           <td><span t-field="raw_line.batch_certificate"/></td>
       </xpath>
   </template>
   ```
5. **Test PDF Rendering:** Always execute headless report render test or inspect PDF output.
