import aiohttp
import asyncio

class ClassA:
    def __init__(self):
        # JSON body for POST request
        self.post_request_body = {
            "name": "John Doe",
            "age": 30,
            "city": "Example City"
        }

    async def post_method(self):
        async with aiohttp.ClientSession() as session:
            async with session.post("https://example.com/api/user", json=self.post_request_body) as response:
                response_data = await response.json()
                self.user_id = response_data.get("user_id", "")
                self.other_value = response_data.get("other_value", "")

class ClassB(ClassA):
    def __init__(self):
        super().__init__()
        self.patch_request_body = self.prepare_patch_request_body()

    def prepare_patch_request_body(self):
        # Using values extracted from ClassA to prepare the PATCH request body in ClassB
        patch_body = {
            "user_id": self.user_id,
            "new_value": self.other_value,
            "additional_field": "some_value"
        }
        return patch_body

    async def patch_method(self):
        async with aiohttp.ClientSession() as session:
            async with session.patch("https://example.com/api/user", json=self.patch_request_body) as response:
                print("PATCH Request Status Code:", response.status)

# Example usage
async def main():
    instance_b = ClassB()
    await instance_b.post_method()
    await instance_b.patch_method()

# Run the event loop
asyncio.run(main())
