# Workflow: Modify View

1. **Locate Target View:**
   - Inspect upstream XML ID (e.g. `stock.view_picking_form`).
2. **Determine View Type:**
   - Form View, List / Tree View, Search View, Kanban View, Pivot View.
3. **Draft XPath Expression:**
   - Prefer specific anchors (`//field[@name='x']`, `//header`, `//sheet`, `//notebook/page[@name='y']`).
   - Avoid brittle index-based paths like `//div[3]/p[2]`.
4. **Position Element:**
   - Choose appropriate position: `inside`, `after`, `before`, `replace`, `attributes`.
5. **Add to Custom Addon Manifest:**
   - Ensure the XML file is listed in `data` in `__manifest__.py`.
   - Ensure the upstream module owning the inherited view is listed in `depends`.
6. **Upgrade & Verify:**
   - Upgrade module: `./scripts/bootstrap.ps1 -Update -Modules <custom_module>`.
   - Verify UI rendering without XML syntax errors.
