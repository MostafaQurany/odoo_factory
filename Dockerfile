FROM odoo:18.0

USER root

# Install required external python dependencies for OCA and factory modules
RUN pip3 install --no-cache-dir --break-system-packages \
    packaging \
    "bokeh==3.6.3" \
    marshmallow

USER odoo
