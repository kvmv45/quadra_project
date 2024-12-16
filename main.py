# imports
import os
from dotenv import load_dotenv  # type: ignore
from pprint import pprint

# Import your VideoIndexerClient library
from VideoIndexerClient.Consts import Consts
from VideoIndexerClient.VideoIndexerClient import VideoIndexerClient

# Load configuration from .env file
load_dotenv()  # Ensure this is called to load environment variables

# Retrieve configuration values
AccountName = os.getenv('AccountName')
ResourceGroup = os.getenv('ResourceGroup')
SubscriptionId = os.getenv('SubscriptionId')

ApiVersion = '2024-06-01-preview'
ApiEndpoint = 'https://api.videoindexer.ai'
AzureResourceManager = 'https://management.azure.com'

# Create and validate consts
consts = Consts(ApiVersion, ApiEndpoint, AzureResourceManager, AccountName, ResourceGroup, SubscriptionId)

# Create Video Indexer Client
client = VideoIndexerClient()

# Authenticate and get access tokens (ARM and Video Indexer account)
client.authenticate_async(consts)

# Get account information (optional)
account_info = client.get_account_async()
pprint(account_info)

# Define video URL or local path
LocalVideoPath = 'C:/Users/kirth/Downloads/01_module-introduction.mp4'

# Excluded AI features
ExcludedAI = []

# Upload video file asynchronously
try:
    file_video_id = client.file_upload_async(LocalVideoPath, video_name=None, excluded_ai=ExcludedAI)
    print(f"Uploaded video ID: {file_video_id}")

    # Wait for indexing to complete
    client.wait_for_index_async(file_video_id)

    # Retrieve insights after indexing
    insights = client.get_video_async(file_video_id)
    pprint(insights)

    # Get insights widgets URL (optional)
    keywords_url = client.get_insights_widgets_url_async(file_video_id, widget_type='Keywords')
    print(f"Keywords Widget URL: {keywords_url}")

    player_widget_url = client.get_player_widget_url_async(file_video_id)
    print(f"Player Widget URL: {player_widget_url}")

    # Get prompt content (if applicable)
    prompt_content = client.get_prompt_content(file_video_id)
    pprint(prompt_content)

except Exception as e:
    print(f"An error occurred: {e}")