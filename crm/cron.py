#!/usr/bin/env python3
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

def update_low_stock():
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql("""
    mutation {
      updateLowStockProducts {
        updatedProducts {
          name
          stock
        }
        message
      }
    }
    """)

    try:
        result = client.execute(mutation)
        updated = result["updateLowStockProducts"]["updatedProducts"]
        timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        log_file = "/tmp/low_stock_updates_log.txt"

        with open(log_file, "a") as f:
            for product in updated:
                f.write(f"{timestamp} - Product {product['name']} updated to stock {product['stock']}\n")
    except Exception:
        pass
