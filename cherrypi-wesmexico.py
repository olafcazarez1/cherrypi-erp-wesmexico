import argparse

import logging
import configparser
import cherrypy

from utils.singleton_meta import MetaConfig
from utils.custom_json_encoder import CustomJSONEncoder

from blueprints.asset import MapAsset
from blueprints.auth import MapAuth
from blueprints.users import MapUsers
from blueprints.locations import MapLocations
from blueprints.customs import MapCustoms
from blueprints.categories import MapCategories
from blueprints.bank_accounts import MapBankAccounts
from blueprints.companies import MapCompanies
from blueprints.employees import MapEmployees
from blueprints.clients import MapClients
from blueprints.contractors import MapContractors
from blueprints.suppliers import MapSuppliers
from blueprints.measures import MapMeasures
from blueprints.taxes import MapTaxes
from blueprints.brands import MapBrands
from blueprints.warehouses import MapWarehouses
from blueprints.products import MapProducts
from blueprints.quote_document import MapQuoteDocument
from blueprints.sale_document import MapSaleDocument
from blueprints.delivery_orders import MapDeliveryOrders
from blueprints.invoice_document import MapInvoiceDocument
from blueprints.helpers import MapHelpers

from blueprints.divitions import MapDivisions
from blueprints.concepts import MapConcepts


def json_handler(*args, **kwargs):
    # Adapted from cherrypy/lib/jsontools.py
    value = cherrypy.serving.request._json_inner_handler(*args, **kwargs)
    return CustomJSONEncoder().iterencode(value)


def main():

    parser = argparse.ArgumentParser(
        description="ERP - Service API WesMexico", usage="%(prog)s [-h] [--config-file FILE]"
    )

    parser.add_argument(
        "--config-file",
        type=str,
        default="/etc/wesmexico/conf/default.conf",
        help="Initial Access Values",
    )

    args = parser.parse_args()

    """Load Config file"""
    config = configparser.ConfigParser()
    config.read_file(open(args.config_file))

    meta = MetaConfig.instance()
    """ Set Data Base Config """
    meta.set_config(key="database", data=dict(config["database"]))

    """ Set Email Config """
    meta.set_config(key="smtp", data=dict(config["smtp"]))

    """ Set Asset Config """
    meta.set_config(key="asset", data=dict(config["asset"]))

    """ Set Settings Config """
    meta.set_config(key="settings", data=dict(config["settings"]))

    """ Setting Web Configurations """
    cherrypy.server.socket_host = config.get("server", "host")
    cherrypy.server.socket_port = int(config.get("server", "port"))

    # cherrypy.server.ssl_module = 'pyopenssl'
    # cherrypy.server.ssl_certificate = '../cert/cert.pem'
    # cherrypy.server.ssl_private_key = '../cert/privkey.pem'

    """ Setting Log Configurations """
    # cherrypy.config.update({'environment' : 'staging'})

    logging.basicConfig(
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        filename=config.get("global", "db_sync_file"),
        level=logging.INFO,
    )

    cherrypy.log.error_file = config.get("global", "error_file")
    cherrypy.log.access_file = config.get("global", "access_file")

    cherrypy.log.error_log.setLevel("DEBUG")
    cherrypy.log.access_log.setLevel("DEBUG")

    cherrypy.log.screen = True
    cherrypy.log(traceback=True)

    """ Init Mappers """
    m_assets = MapAsset()
    m_auth = MapAuth()
    m_user = MapUsers()
    m_locations = MapLocations()
    m_customs = MapCustoms()
    m_categories = MapCategories()
    m_bank_accounts = MapBankAccounts()
    m_companies = MapCompanies()
    m_employees = MapEmployees()
    m_clients = MapClients()
    m_contractors = MapContractors()
    m_suppliers = MapSuppliers()
    m_measures = MapMeasures()
    m_taxes = MapTaxes()
    m_brands = MapBrands()
    m_warehouses = MapWarehouses()
    m_products = MapProducts()
    m_quotes = MapQuoteDocument()
    m_sales = MapSaleDocument()
    m_orders = MapDeliveryOrders()
    m_invoices = MapInvoiceDocument()
    m_helpers = MapHelpers()

    m_divisions = MapDivisions()
    m_concepts = MapConcepts()

    """ Setting URI for server """
    mapping = cherrypy.dispatch.RoutesDispatcher()
    mapping.mapper.explicit = False

    # mapping.connect('index',"/",controller=server, action='index')
    m_assets.init(mapping)
    m_auth.init(mapping)
    m_user.init(mapping)
    m_locations.init(mapping)
    m_customs.init(mapping)
    m_categories.init(mapping)
    m_bank_accounts.init(mapping)
    m_companies.init(mapping)
    m_employees.init(mapping)
    m_clients.init(mapping)
    m_contractors.init(mapping)
    m_suppliers.init(mapping)
    m_measures.init(mapping)
    m_taxes.init(mapping)
    m_brands.init(mapping)
    m_warehouses.init(mapping)
    m_products.init(mapping)
    m_quotes.init(mapping)
    m_sales.init(mapping)
    m_orders.init(mapping)
    m_invoices.init(mapping)
    m_helpers.init(mapping)

    m_divisions.init(mapping)
    m_concepts.init(mapping)

    """ Set custom JSON handler """
    cherrypy.config["tools.json_out.handler"] = json_handler

    """Removing cache"""
    cherrypy.lib.caching.get(invalid_methods=("POST", "PUT", "PATCH", "DELETE", "GET"))

    """Define Reply Template """
    cherrypy._cperror._HTTPErrorTemplate = "%(status)s - %(message)s"

    """ Start Engine Service """
    cherrypy.tree.mount(None, config={"/": {"request.dispatch": mapping}})
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    main()
