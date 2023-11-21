import datetime
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from app import log


async def post_with_retry(url, payload, max_retries=3) -> requests.Response:
    headers_net_cracker = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "env": "it02",
        "Authorization": f'Bearer {"access_token"}',  # Replace with a valid access token
    }
    session = requests.Session()
    retry_strategy = Retry(
        total=max_retries, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        response = session.post(url, json=payload, headers=headers_net_cracker)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to make POST request: {e}")
        raise e


class NetCrackerReservationProvider:
    def __init__(self):
        pass

    async def create_net_cracker_resource(
        self,
        reservation_item,
        related_party_id,
        related_party_role,
        reservation_item_quantity,
        reservation_item_resource_capacity_type,
        reservation_item_resource_capacity_capacity_demand_amount,
        reservation_item_resource_capacity_resource_pool_id,
        ip_am_description,
        ip_am_detail,
    ):
        log.info("Creating net cracker resource")
        reservation_place = (
            reservation_item.reservation_resource_capacity.reservation_place
        )

        create_resource_request_payload = {
            "relatedParty": {
                "partyRole": related_party_role,
                "partyId": related_party_id,
            },
            "@type": "IPRangeReservation",
            "requestedPeriod": {
                "fromToDateTime": str(
                    datetime.datetime.now()
                )  # Replace with a valid datetime object
            },
            "reservationItem": [
                {
                    "quantity": reservation_item_quantity,
                    "@type": "IPRangeReservationItem",
                    "resourceCapacity": {
                        "@type": reservation_item_resource_capacity_type,
                        "capacityDemandAmount": reservation_item_resource_capacity_capacity_demand_amount,
                        "resourcePool": {
                            "@type": "IP Pool",
                            "id": reservation_item_resource_capacity_resource_pool_id,
                            "resourceCollection": [
                                {
                                    "@type": "IP Pool",
                                    "name": "True Static IP",
                                    "resource": [
                                        {
                                            "preferredSubnet": "",
                                            "place": [
                                                {
                                                    "name": place_info.name,
                                                    "role": place_info.type,
                                                }
                                                for place_info in reservation_place
                                            ],
                                            "characteristic": [
                                                {
                                                    "ipRangeCIDR": "29",  # capacity demand amount
                                                    "addressPurpose": "Static",
                                                    "IPAMDescription": ip_am_description,
                                                    "IPAMDetail": ip_am_detail,
                                                    "Customer": {
                                                        "name": "TEST CUSTOMER 11",
                                                        "cpid": "77000001",
                                                        "streetAddress": "2C 4816 50 AVE",
                                                        "province": "AB",
                                                        "postalCode": "T7A1W2",
                                                        "country": "Canada",
                                                        "city": "DRAYTON VALLEY",
                                                        "lpdsid": "5481277",
                                                    },
                                                }
                                            ],
                                        }
                                    ],
                                }
                            ],
                        },
                    },
                }
            ],
        }

        net_cracker_reservation_url = "https://apigw-private-nane-np-001.tsl.telus.com/resource/resourcePoolManagement/v1/reservation"

        log.info("Before creating netcracker resource")
        response = await post_with_retry(
            net_cracker_reservation_url, create_resource_request_payload
        )
        log.info("After creating net cracker resource")

        if response.status_code == 201:
            log.info("Resource created successfully (Reserved Ips)")
        else:
            log.error(f"Failed to create resource. Status code: {response.status_code}")


net_cracker_reservation_instance = NetCrackerReservationProvider()
