@property
def age(self):
    from datetime import datetime
    from datetime import date

    today = date.today()

    try:
        birthdate = datetime.strptime(self.dob, "%Y-%m-%d")
    except (TypeError, ValueError):
        return "N/A"
    else:
        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))