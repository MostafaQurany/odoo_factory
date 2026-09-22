# Workflow: Modify Integration & External Connectors

1. **Target Module:**
   - Always place external connectors, REST/GraphQL APIs, MES/WMS abstractions in `custom/factory_integration`.
   - Never couple direct external database connectors into `factory_base` or `factory_mrp`.
2. **Asynchronous Execution:**
   - All bulk imports or sync jobs MUST use `queue_job` (Background Jobs capability).
   - Use `@job` decorator on model methods:
     ```python
     from odoo.addons.queue_job.job import job

     @job
     def sync_machine_telemetry(self, machine_id):
         ...
     ```
3. **Verify:**
   - Run cross-cutting test: `python scripts/factory/run_scenario.py -s GX-003`.
