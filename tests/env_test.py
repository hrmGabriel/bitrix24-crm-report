"""
Environment and basic Bitrix API connectivity test.

This test validates:
- Environment variables loading
- Bitrix webhook authentication
- Basic API reachability

It does NOT validate business data.

Run this test with:
    $ python -m tests.env_test
"""

from src.bitrix_client import BitrixClient

def test_environment_connection() -> None:
    """
    Tests whether the Bitrix API is reachable using the configured webhook.

    Expected behavior:
    - No exception raised
    - A valid response containing user profile data
    """

    client = BitrixClient()

    try:
        response = client.call("profile")
    except Exception as exc:
        raise RuntimeError(
            "Failed to connect to Bitrix API. "
            "Please verify .env configuration and webhook permissions."
        ) from exc

    if "result" not in response:
        raise RuntimeError(
            "Unexpected API response structure. "
            "The 'result' field is missing."
        )

    print("✅ Environment and Bitrix API connection test passed.")


if __name__ == "__main__":
    test_environment_connection()
