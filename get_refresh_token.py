#!/usr/bin/env python3
"""Run this script ONCE locally to obtain a Google OAuth2 refresh token.

The refresh token is then stored as the GOOGLE_REFRESH_TOKEN GitHub secret.

Usage:
    pip install google-auth-oauthlib
    python get_refresh_token.py
"""
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/blogger",
    "https://www.googleapis.com/auth/drive.file",
]


def main() -> None:
    print("=== Blogger OAuth2 Refresh Token Helper ===\n")
    print("You need a Google OAuth2 Client ID and Client Secret.")
    print("Get them from: https://console.cloud.google.com/apis/credentials\n")

    client_id = input("Google OAuth2 Client ID: ").strip()
    client_secret = input("Google OAuth2 Client Secret: ").strip()

    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"],
            }
        },
        scopes=SCOPES,
    )

    creds = flow.run_local_server(port=0)

    print("\n" + "=" * 50)
    print("SUCCESS — add these values as GitHub repository secrets:\n")
    print(f"  GOOGLE_CLIENT_ID     = {client_id}")
    print(f"  GOOGLE_CLIENT_SECRET = {client_secret}")
    print(f"  GOOGLE_REFRESH_TOKEN = {creds.refresh_token}")
    print("=" * 50)


if __name__ == "__main__":
    main()
