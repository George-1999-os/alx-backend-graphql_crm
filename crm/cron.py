from datetime import datetime

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes and checks GraphQL health
    """
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=True,
            retries=3,
        )
        client = Client(
            transport=transport,
            fetch_schema_from_transport=False,
        )

        query = gql(
            """
            query {
                hello
            }
            """
        )
        client.execute(query)
    except Exception:
        pass

    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as file:
        file.write(message)


def update_low_stock():
    """
    Updates low stock products and logs the updates
    """
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(
        transport=transport,
        fetch_schema_from_transport=False,
    )

    mutation = gql(
        """
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                message
            }
        }
        """
    )

    try:
        result = client.execute(mutation)
        updated_products = result["updateLowStockProducts"]["updatedProducts"]
        timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

        with open("/tmp/low_stock_updates_log.txt", "a") as file:
            for product in updated_products:
                file.write(
                    f"{timestamp} - Product {product['name']} updated to stock {product['stock']}\n"
                )
    except Exception:
        pass
