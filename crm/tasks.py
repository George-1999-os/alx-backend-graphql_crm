from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
      customers {
        totalCount
      }
      orders {
        totalCount
        totalAmountSum
      }
    }
    """)

    try:
        result = client.execute(query)
        customers = result["customers"]["totalCount"]
        orders = result["orders"]["totalCount"]
        revenue = result["orders"]["totalAmountSum"]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = "/tmp/crm_report_log.txt"

        with open(log_file, "a") as f:
            f.write(f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")
    except Exception:
        pass
