# Run the migration function via manage.py remote shell (or manage.py shell
# for local development DB)

from datetime import datetime
from minicms.models import Page

def migrate_v2():
    Page._meta.get_field('last_update').default = lambda: datetime.now()
    for page in list(Page.objects.all()):
        page.save()
