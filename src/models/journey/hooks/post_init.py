def post_init(self, is_new_object, kwargs):
    from datetime import datetime

    try:
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d")
    except (TypeError, ValueError):
        self.start_timestamp = None
    else:
        self.start_timestamp = start_date.timestamp()