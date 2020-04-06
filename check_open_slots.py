import httpx
import asyncio
import json
import time


def post_to_slack(slack_webhook, msg):
    httpx.post(
        "https://hooks.slack.com/services/{}".format(slack_webhook),
        data='{"text": "' + msg + '"}', 
        headers={"Content-type": "application/json"},
)


async def main():
    while True:
        # Connect using your credentials
        r = httpx.post(f"{login}", data=login_data, headers=headers_login,)

        # Get your access token
        headers_delivery = {
            "Authorization": "Bearer " + r.json()["access_token"],
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15",
        }

        # Pull delivery times
        delivery_times = httpx.get(
            f"{delivery_time_path}",
            headers=headers_delivery,
            cookies=r.cookies,
        )

        # Check for availability
        any_slot = False
        for slot in delivery_times.json()["time_slots"]:
            if slot["available"]:
                any_slot = True

        if any_slot:
            print(f"{time.strftime('%X')}")
            print("Found a slot!!!")
            post_to_slack(slack_webhook, "Found a slot - hurry up!")
        else:
            print("No slots available :(")

        await asyncio.sleep(600)  # don't swamp their server!


# Credientials
username = "YOUR EMAIL"
password = "YOUR PASSWORD"
slack_webhook = "SLACK WEB HOOK"

# API paths
login = "https://api.shipt.com/auth/v2/oauth/token?white_label_key=shipt"
delivery_time_path = "https://app.shipt.com/api/v1/orders/available_slots.json?customer_address_id=7673640"

# HTML headers
login_data = {
    "MIME Type": "application/x-www-form-urlencoded",
    "username": username,
    "password": password,
    "grant_type": "password",
}
headers_login = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15",
    "X-User-Type": "Customer",
}

# Infinite loop
loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(main())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()
