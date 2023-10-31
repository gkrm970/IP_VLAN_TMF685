import httpx
import requests

from app import log, schemas

BASE_URL = "http://127.0.0.1:8000"
headers = {
    "Content-Type": "application/json",
    "accept": "application/json"
}


def generate_unique_vlan(capacity_amount, used_vlans):
    for vlan in range(1, capacity_amount + 1):
        if vlan not in used_vlans:
            used_vlans.add(vlan)
            return vlan
    return None


def create_resource_item(request_body):
    tmf_639_post_url = "https://dc452315-b9e6-4396-a5de-c6219eca37ee.mock.pstmn.io"
    response = requests.post(url=tmf_639_post_url, headers=headers, json=request_body)
    return response


from typing import TypeAlias, Literal
from asgi_correlation_id import correlation_id

Method: TypeAlias = Literal["GET"]


async def _send_request(method: Method, href: str) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        await client.request(method, href, headers={"X-Request-ID": correlation_id.get() or ""})


async def fetch_resource_pool_data(url):
    response = httpx.AsyncClient()
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from {url}. Status code: {response.status_code}")


def process_reservation_item(item: schemas.ReservationItem, used_vlans: set[int]):
    item.reservation_resource_capacity.resource_pool.href
    resource_pool_href_url = item["reservation_resource_capacity"]["resource_pool"]["href"]
    resource_pool_id = item["reservation_resource_capacity"]["resource_pool"]["pool_id"]
    resource_pool_data = fetch_resource_pool_data(resource_pool_href_url)
    demand_amount = int(item["reservation_resource_capacity"]["capacity_demand_amount"])
    reserved_vlans = set()

    # self._extract_capacity_amount()
    # self._extract_related_party()
    #
    # reserved_vlans = self._reserve_tinaa_resources()
    # self._reserve_netcracker_resources()
    #
    # self._create_logical_resources_in_inventory()
    #
    # self._assemble_resource_creation_request()

    for capacity_item in resource_pool_data.get("capacity", []):
        capacity_amount = capacity_item.get("capacityAmount", 0)
        related_party_id = capacity_item.get("relatedParty", {}).get("id")
        if related_party_id == "TINAA":
            if demand_amount <= capacity_amount:
                remaining_amount = capacity_amount - demand_amount

                for _ in range(demand_amount):
                    unique_vlan = generate_unique_vlan(capacity_amount, used_vlans)
                    if unique_vlan is not None:
                        reserved_vlans.add(unique_vlan)
                applied_capacity_amount = reserved_vlans
                break
        elif related_party_id == "netcracker":
            # If IP Address generate Reservation endpoint for netcraker \
            # and trigger wait for Ip Addresses as a responses.
            pass

    are_enough_vlans_available = len(reserved_vlans) == demand_amount

    if are_enough_vlans_available:
        create_resource_request = {
            "category": "UPF NFs",
            "description": "Ericsson UPF 25 IOT NF",
            "href": "https://api.develop.tinaa.teluslabs.net/plan/inventory/resourceInventoryManagement/v1"
                    "/resource/5ca5aaa7-edd5-49b1-b5c2-05390ca87a35",
            "id": "5ca5aaa7-edd5-49b1-b5c2-05390ca87a35",
            "name": "Eric_IOT_UPF_25_MTLXPQVV-IOTUPF-01",
            "operationalState": "enable",
            "place": [
                {
                    "name": "Montreal",
                    "role": "geographicRegion"
                },
                {
                    "name": "Viger_POD 1",
                    "role": "podId"
                }
            ],
            "resourceCharacteristic": [{"name": related_party_id, "value": vlan} for vlan in applied_capacity_amount]
        }
        response = create_resource_item(create_resource_request)

        if response.status_code == 201:
            resource_pool_json = response.json()
            href = resource_pool_json.get("href")
            pool_id = resource_pool_json.get("id")

            resource_pool_patch_url = f"http://127.0.0.1:8000/resourcePoolManagement/v1/resourcePool/{resource_pool_id}"
            resource_pool_patch_response = {
                "@type": "VLAN",
                "name": "VLAN",
                "capacity": [
                    {
                        "capacityAmount": 10,
                        "capacityAmountFrom": "172.7.6.0/24",
                        "capacityAmountTo": "172.7.6.255/24",
                        "relatedParty": {
                            "id": "TINAA",
                            "name": "8021qVLAN",
                            "role": "VLANPool"
                        },
                        "place": [
                            {
                                "name": "AB",
                                "type": "region"
                            },
                            {
                                "name": "Viger-1",
                                "type": "pod"
                            }
                        ]
                    },
                    {
                        "capacityAmount": 5,
                        "capacityAmountFrom": "172.7.7.0/24",
                        "capacityAmountTo": "172.7.7.255/24",
                        "relatedParty": {
                            "id": "TINAA",
                            "name": "8021qVLAN",
                            "role": "VLANPool"
                        },
                        "place": [
                            {
                                "name": "BC",
                                "type": "region"
                            },
                            {
                                "name": "Viger-2",
                                "type": "pod"
                            }
                        ]
                    }
                ],
                "id": "fe18c37c-c92c-4e0b-9f3f-826c3928aa5a",
                "href": "/resourcePoolManagement/v1/resourcePool/fe18c37c-c92c-4e0b-9f3f-826c3928aa5a"
            }

            for resource_pool_item in resource_pool_patch_response["capacity"]:
                resource_pool_item["capacityAmount"] = remaining_amount
            log.info("resource_pool_patch_response", resource_pool_patch_response)

            characteristic_list = []
            applied_capacity_amount = {
                "appliedCapacityAmount": str(demand_amount),
                "resource": []
            }
            for vlan in used_vlans:
                characteristic = {
                    "8021qVLAN": vlan
                }

                applied_capacity_amount["resource"].append({
                    "@referredType": "VLAN",
                    "href": href,
                    "resource_id": pool_id,
                    "characteristic": characteristic
                })

            log.info("applied_capacity_amount", applied_capacity_amount)

            item["appliedCapacityAmount"] = applied_capacity_amount

        if response.status_code == 201:
            log.info("Resource created successfully.")
        else:
            log.info(f"Failed to create resource. Status code: {response.status_code}")
            log.info("Response:", response.text)
    else:
        log.info("Insufficient available VLANs.")


def create_reservation_response(reservation_create: schemas.ReservationCreate):
    for reservation_item in reservation_create.reservation_item:
        used_vlans = set()
        process_reservation_item(reservation_item, used_vlans)
    return reservation_create
