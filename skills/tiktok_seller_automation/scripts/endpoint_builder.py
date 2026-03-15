from datetime import datetime, timedelta

class EndpointBuilder:
    @staticmethod
    def build_product_subscription_payload(start_date, end_date, page=0, size=10):
        """
        Builds the payload for the product_subscriptions endpoint.
        """
        return {
            "request": {
                "time_descriptor": {
                    "start": start_date,
                    "end": end_date
                },
                "filter": {},
                "list_control": {
                    "pagination": {
                        "page": page,
                        "size": size
                    },
                    "rules": [
                        {
                            "direction": 2,
                            "field": "active_subscriptions"
                        }
                    ]
                }
            }
        }

    @staticmethod
    def get_default_dates():
        """
        Returns a default start/end date (last 7 days).
        """
        end = datetime.now()
        start = end - timedelta(days=7)
        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
