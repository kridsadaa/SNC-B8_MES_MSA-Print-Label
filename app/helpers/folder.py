from datetime import datetime, timedelta

from app.utils import delete_folder


def deleting_folders_that_are_not_from_today():
    folder_yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    delete_folder(f'temp/{folder_yesterday}')