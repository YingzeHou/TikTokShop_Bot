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
    def build_campaign_list_payload(start_date, end_date, page=1, size=10):
        return {
            "query_list": [
                "campaign_name", "campaign_status", "campaign_budget", "cost", "onsite_roi2_shopping_value"
            ],
            "start_time": start_date,
            "end_time": end_date,
            "page": page,
            "page_size": size,
            "order_field": "cost",
            "order_type": 1,
            "campaign_status": ["delivery_ok"],
            "campaign_shop_automation_type": 2,
            "external_type_list": ["304", "307"]
        }

    @staticmethod
    def build_campaign_detail_payload(start_date, end_date, campaign_ids=None):
        return {
            "query_list": ["cost", "onsite_roi2_shopping_value", "onsite_roi2_shopping"],
            "start_time": start_date,
            "end_time": end_date,
            "campaign_shop_automation_type": 2,
            "external_type_list": ["307", "304", "305"],
            "campaign_ids": campaign_ids or []
        }

    @staticmethod
    def build_product_performance_general_payload(start_date, end_date, page=0, size=10):
        """
        Builds payload for the product_performance_general endpoint.
        """
        return {
            "request": {
                "time_descriptor": {
                    "start": start_date,
                    "end": end_date,
                    "timezone_offset": -28800
                },
                "ccr_available_date": end_date, # Approximation
                "search": {"voc_statuses": [], "gmv_ranges": []},
                "filter": {},
                "list_control": {
                    "rules": [{"direction": 2, "field": "gmv"}],
                    "pagination": {
                        "size": size,
                        "page": page
                    }
                }
            }
        }

    @staticmethod
    def build_product_list_payload(start_date, end_date, campaign_id="", page=1, size=10):
        return {
            "query_list": [
                "product_id", "product_name", "onsite_roi2_shopping_value", "mixed_real_cost"
            ],
            "start_time": start_date,
            "end_time": end_date,
            "page": page,
            "page_size": size,
            "campaign_id": campaign_id,
            "order_field": "onsite_roi2_shopping_value",
            "order_type": 1
        }

    @staticmethod
    def get_default_dates():
        """
        Returns a default start/end date (last 7 days).
        """
        end = datetime.now()
        start = end - timedelta(days=7)
        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
