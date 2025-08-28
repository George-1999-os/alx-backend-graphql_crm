#!/bin/bash

# Move to project root
cd "$(dirname "$0")/../.."

# Run Django cleanup with inline Python code
deleted_count=$(python3 manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(created_at__lt=cutoff, is_active=False)
count = qs.count()
qs.delete()
print(count, end='')  # clean numeric output
")

# Show result on terminal
echo "Deleted $deleted_count inactive customers"

# Log result
echo \"$(date): Deleted $deleted_count inactive customers\" >> ./crm/cron_jobs/customercleanuplog.txt
