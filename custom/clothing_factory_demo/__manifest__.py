# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Clothing Factory Demo Data",
    "version": "18.0.1.0.0",
    "category": "Manufacturing",
    "summary": "Realistic Apparel & Garment Manufacturing Demo Data (Fabrics, BOMs, Work Centers, DDMRP Buffers)",
    "author": "Odoo Factory",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        "stock",
        "ddmrp",
        "web_responsive",
        "web_timeline",
    ],
    "data": [
        "data/product_data.xml",
        "data/mrp_routing_data.xml",
        "data/mrp_bom_data.xml",
        "data/ddmrp_buffer_data.xml",
        "data/mrp_production_data.xml",
    ],
    "installable": True,
    "application": False,
}
