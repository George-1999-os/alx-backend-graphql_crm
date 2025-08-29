import requests
from datetime import datetime
from celery import shared_task

@shared_task
def generate_crm_report():
    url = "http://localhost:8000/graphql"
    query = """
    query {
      customers {
        totalCount
      }
      orders {
        totalCount
        totalAmountSum
      }
    }
    """
    try:
        response = requests.post(url, json={'query': query})
        data = response.json()['data']

        customers = data["customers"]["totalCount"]
        orders = data["orders"]["totalCount"]
        revenue = data["orders"]["totalAmountSum"]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = "/tmp/crm_report_log.txt"

        with open(log_file, "a") as f:
            f.write(f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")
    except Exception:
        pass
