from directory_tree import DisplayTree
import sys  # Import sys to handle stderr and exit
from app.config import Config

import requests
import json
from directory_tree import DisplayTree
from app.config import Config

# Teams Webhook URL (replace with your actual webhook URL)
TEAMS_WEBHOOK_URL = "https://askimsviken.webhook.office.com/webhookb2/d03c16e1-8bbd-4b7e-8343-9187d5451e99@93b10fca-5146-4c74-bc2b-03d9501ffcd2/IncomingWebhook/8b1ab7cc50614625a5c0954221092134/dadc49a4-4001-4982-b3ae-5429dfe49aca/V2pGKgqDiQBqhlYBH8c1nq1nJji5Yytk0J0Mixm1J3x8s1"

def generate_project_tree():
    """
    Generates an ASCII tree representation of the project structure
    and sends it to Microsoft Teams.
    """
    try:
        project_root = Config.BASE_DIR
        ignore_directories = ["venv", "__pycache__", ".git", "node_modules", "media"]

        # Generate directory tree
        tree = DisplayTree(
            dirPath=project_root,
            ignoreList=ignore_directories,
            showHidden=False,
            maxDepth=5,
            stringRep=True  # Ensures the tree is returned as a string, not printed automatically
        )

        directory_structure = str(tree)

        # Prepare message payload for Teams
        message = {
            "text": f"**Updated Project Structure:**\n```\n{directory_structure}\n```"
        }

        # Send to Teams Webhook
        response = requests.post(TEAMS_WEBHOOK_URL, json=message)

        if response.status_code == 200:
            print("✅ Successfully sent project tree to Teams!")
        else:
            print(f"❌ Failed to send message to Teams. Response: {response.text}")

    except Exception as e:
        print(f"Error generating directory tree: {e}")

if __name__ == "__main__":
    generate_project_tree()
