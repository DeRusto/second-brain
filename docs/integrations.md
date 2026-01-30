# Second Brain Integrations Guide

This document covers how to configure the integrations for **Vikunja**, **Google Calendar**, and **Slack Context**.

---

## 1. Notion Events Database

You need to create a new database for Events.

1.  Create a new Database in Notion named **"Events Database"**.
2.  Set up the following properties:

| Field | Type | Purpose |
|-------|------|---------|
| Name | Title | Event name |
| Date | Date | Start and End time |
| Location | Rich Text | Location |
| Description | Rich Text | Notes/Details |
| Calendar | Select | Options: `personal`, `family`, `maggie` |

3.  Copy the Database ID and update the **Events Database** node in n8n.

---

## 2. Vikunja Integration (To-Do List)

The system automatically sends tasks classified as `admin` to Vikunja.

### Prerequisites
- A self-hosted or cloud Vikunja instance.
- An API Token.
- A specific Project (List) ID where tasks will be created.

### Configuration Steps

1.  **Generate API Token**:
    - Go to User Settings -> API Tokens in Vikunja.
    - Create a new token with read/write access to tasks.
2.  **Find Project ID**:
    - Open the list/project in Vikunja.
    - The ID is usually in the URL (e.g., `/namespaces/1/lists/42` -> ID is 42) or available in the project settings.
3.  **Configure n8n**:
    - Open the **Vikunja Task** node.
    - Update `URL`: replace `VIKUNJA_API_URL` with your instance URL (e.g., `https://vikunja.mydomain.com/api/v1`).
    - Update `Project ID`: replace `VIKUNJA_PROJECT_ID` in the URL path.
    - Update **Headers**:
        - `Authorization`: `Bearer <YOUR_API_TOKEN>`

---

## 3. Google Calendar Integration

The system routes events to different calendars based on context.

### Prerequisites
- Google Cloud Console Project with Google Calendar API enabled.
- OAuth Client ID and Secret configured in n8n credentials.

### Calendar IDs
You need to identify the Calendar IDs for:
- **Personal**: Your main calendar (usually your email address).
- **Family**: The shared family calendar ID.
- **Maggie**: Your wife's calendar ID (if you have write access).

**To find a Calendar ID:**
1.  Open Google Calendar.
2.  Go to Settings for the specific calendar.
3.  Scroll down to "Integrate calendar".
4.  Copy the "Calendar ID".

### Configure n8n Nodes
Update the `Calendar ID` field in the following nodes with the actual IDs:
- **GCal Personal**
- **GCal Family**
- **GCal Maggie**
- **GCal Due Date** (uses Personal calendar by default)

---

## 4. Slack Context (User Identification)

To correctly identify messages "From Maggie" or "From Me", you need to map Slack User IDs.

1.  **Find User IDs**:
    - In Slack, click on a user's profile picture.
    - Click on the three dots (...) -> "Copy member ID".
    - Do this for yourself and your wife/partner.
2.  **Update n8n Code**:
    - Open the **Enrich Context** node.
    - Update the `userMap` object:

```javascript
const userMap = {
  'U12345678': 'Maggie', // Replace with actual Wife's ID
  'U87654321': 'Me'      // Replace with your ID
};
```
