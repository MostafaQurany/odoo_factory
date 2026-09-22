# Workflow: Add Field to Model

```text
Requirement -> Locate Model -> Check Existing -> Custom Addon -> Python Field -> View Inheritance -> Security -> Upgrade -> Test
```

1. **Locate Target Model:**
   - Example: Adding `machine_number` to `mrp.production`.
2. **Check Existing Fields:**
   - Inspect OCA/Core addons to avoid duplicate field definitions.
3. **Select or Create Custom Module:**
   - Use `custom/factory_<domain>` (e.g., `custom/factory_mrp`).
4. **Define Python Field:**
   ```python
   from odoo import models, fields

   class MrpProduction(models.Model):
       _inherit = 'mrp.production'

       machine_number = fields.Char(string="Machine Number", tracking=True)
   ```
5. **Inherit View (`views/mrp_production_views.xml`):**
   ```xml
   <record id="view_mrp_production_form_inherit_machine" model="ir.ui.view">
       <field name="name">mrp.production.form.inherit.machine</field>
       <field name="model">mrp.production</field>
       <field name="inherit_id" ref="mrp.mrp_production_form_view"/>
       <field name="arch" type="xml">
           <xpath expr="//field[@name='bom_id']" position="after">
               <field name="machine_number"/>
           </xpath>
       </field>
   </record>
   ```
6. **Upgrade & Verify:**
   - Run `./scripts/bootstrap.ps1 -Update -Modules factory_mrp`.
   - Run impacted scenario: `python scripts/factory/run_scenario.py -s GS-007`.
