class Details:
    def __init__(
        self,
        sponsor: str | None,
        company: str | None,
        badge_number: str | None,
        notify_date: str | None,
    ):
        self.sponsor = sponsor
        self.company = company
        self.badge_number = badge_number
        self.notify_date = notify_date

    def __str__(self):
        return f"Sponsor: {self.sponsor}, Company: {self.company}, Badge Number: {self.badge_number}, Notify Date: {self.notify_date}"