# Security

## What never goes to the cloud

- Password / OTP / payment PIN / card security codes
- Android Keystore private keys
- Screenshots, unless an explicit VISUAL observation is required after redaction
- Shared static device secrets baked into the APK

## SafetyEngine

Safety decisions are application code, not model output.

- GREEN: navigate, read, open apps
- YELLOW: message/call/share — confirm first
- RED: money movement, wipe, uninstall — blocked in v1
- SECRET: never in Agent payloads

## Reporting

Open a GitHub issue with the `security` label, or email the maintainer listed on the GitHub profile.
Do not attach `.env` files, pairing tokens, or live device dumps that contain SECRET fields.

## Deployment

Production secrets live in `/opt/blindpilot/.env` on the VPS with mode `600`.
They are not in git.
