from datetime import datetime

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes and optionally checks GraphQL health
    """
    # --- GraphQL hello health check ---
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
        # GraphQL check is optional; heartbeat must still log
        pass

    # --- Heartbeat logging ---
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as file:
        file.write(message)
