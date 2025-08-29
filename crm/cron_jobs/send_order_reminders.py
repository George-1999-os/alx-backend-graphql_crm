#!/usr/bin/env python3

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta

transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)
client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql("""
query GetRecentOrders($startDate: DateTime!) {
  orders(filter: {order_date_gte: $startDate}) {
    id
    customer {
      email
    }
  }
}
""")

start_date = (datetime.now() - timedelta(days=7)).isoformat()
result = client.execute(query, variable_values={"startDate": start_date})

log_file = "/tmp/order_reminders_log.txt"
with open(log_file, "a") as f:
    for order in result["orders"]:
        order_id = order["id"]
        email = order["customer"]["email"]
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} - Order {order_id} reminder sent to {email}\n")

print("Order reminders processed!")
