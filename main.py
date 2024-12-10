import os
import glob
import shutil
import requests
import asyncio
from aiohttp import ClientSession
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Constants
VIDEO_DIR = "./videos"
API_BASE_URL = "https://api.socialverseapp.com/posts"
FLIC_TOKEN = "<Token>"
HEADERS = {
    "Flic-Token": FLIC_TOKEN,
    "Content-Type": "application/json"
}


# Step 1: Get Upload URL
async def get_upload_url(session):
    async with session.get(f"{API_BASE_URL}/generate-upload-url", headers=HEADERS) as response:
        if response.status == 200:
            data = await response.json()
            return data["url"], data["hash"]
        else:
            raise Exception(f"Failed to get upload URL: {await response.text()}")


# Step 2: Upload Video
async def upload_video(session, upload_url, file_path):
    with open(file_path, "rb") as video_file:
        async with session.put(upload_url, data=video_file) as response:
            if response.status == 200:
                print(f"Uploaded {file_path} successfully.")
            else:
                raise Exception(f"Failed to upload {file_path}: {await response.text()}")


# Step 3: Create Post
async def create_post(session, video_hash, title, category_id=1):
    post_data = {
        "title": title,
        "hash": video_hash,
        "is_available_in_public_feed": False,
        "category_id": category_id
    }
    async with session.post(API_BASE_URL, headers=HEADERS, json=post_data) as response:
        if response.status == 200:
            print(f"Post created successfully: {await response.json()}")
        else:
            raise Exception(f"Failed to create post: {await response.text()}")


# Main Processing Function
async def process_video(file_path):
    async with ClientSession() as session:
        try:
            # Get Upload URL and Hash
            upload_url, video_hash = await get_upload_url(session)
            print(f"Obtained upload URL for {file_path}")

            # Upload Video
            await upload_video(session, upload_url, file_path)

            # Create Post
            title = os.path.basename(file_path).replace(".mp4", "")
            await create_post(session, video_hash, title)

            # Auto-delete Local File
            os.remove(file_path)
            print(f"Deleted local file: {file_path}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")


# Monitor Directory for New Videos
class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".mp4"):
            return
        asyncio.run(process_video(event.src_path))


def monitor_directory():
    event_handler = VideoHandler()
    observer = Observer()
    observer.schedule(event_handler, VIDEO_DIR, recursive=False)
    observer.start()
    print(f"Monitoring directory: {VIDEO_DIR}")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# Async Batch Upload for Existing Videos
async def batch_upload():
    video_files = glob.glob(f"{VIDEO_DIR}/*.mp4")
    tasks = [process_video(file_path) for file_path in video_files]
    await asyncio.gather(*tasks)


# Main Execution
if __name__ == "__main__":
    # Create directory if it doesn't exist
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)

    # Start Monitoring and Process Existing Files
    asyncio.run(batch_upload())
    monitor_directory()
