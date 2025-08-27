#!/bin/bash

# Move to project root
cd "$(dirname "$0")/../.."

# Run Django cleanup
deleted_count=$(python3 manage.py shell <<'PYCODE'
from django.utils import timezone
from datetime import timedelta
from django.db.models import Max, Q
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)
qs = Customer.objects.annotate(last_order=Max('orders__created_at')).filter(
    Q(last_order__lt=cutoff) | Q(last_order__isnull=True)
)
count = qs.count()
qs.delete()
print(count)
PYCODE
)

# Log result
echo "$(date): Deleted $deleted_count inactive customers" >> /tmp/customercleanuplog.txt
