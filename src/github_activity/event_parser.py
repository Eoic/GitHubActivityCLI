from datetime import datetime
from collections import defaultdict


class EventParser:
    @classmethod
    def summarize_events(cls, data: list[dict]):
        summary = defaultdict(list)

        for event in data:
            created_at = datetime.strptime(event["created_at"], '%Y-%m-%dT%H:%M:%SZ')
            year_month_key = created_at.strftime("%Y-%m")

            match event['type']:
                case 'PushEvent':
                    message = f'Pushed {event["payload"]["size"]} commits to {event["repo"]["name"]}'
                    summary[year_month_key].append((message, created_at))

        return summary
