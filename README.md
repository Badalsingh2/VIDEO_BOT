# Video Upload and Directory Monitoring Script
============================================

This Python script automates the process of uploading `.mp4` videos to a server, 
creating corresponding posts via API, and managing the local directory by deleting 
processed files. It also monitors a specified directory for new videos and processes 
them in real-time.

# Features
--------
- Batch Upload: Automatically uploads all existing `.mp4` videos in the `/videos` directory.
- Real-Time Monitoring: Detects new `.mp4` files in the `/videos` directory and processes them as they are added.
- Asynchronous Operations: Utilizes `asyncio` for concurrent uploads and API interactions, ensuring efficiency.
- Auto-Delete Files: Deletes local video files after successful upload and post creation.
- API Integration: Interacts with the Socialverse API to upload videos and create posts.

# Requirements
------------
- Python 3.7+
- Libraries:
  - `aiohttp`
  - `watchdog`
  - `requests`

# Installation
------------
1. Clone the Repository:
   
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install Dependencies:
   
   pip install aiohttp watchdog requests
   

3. Set Up the Directory:
   - Ensure the `/videos` directory exists:
     
     mkdir videos
     

4. Configure the Script:
   - Replace `<YOUR_TOKEN>` in the script with your actual Flic-Token obtained from the Socialverse API:
     python
     FLIC_TOKEN = "<YOUR_TOKEN>"
     

# Usage
-----
1. Run the Script:
   ```
   python main.py
   ```
   Replace `main.py` with the actual file name of the script.

2. Add Video Files:
   - Place `.mp4` video files in the `/videos` directory.
   - The script will:
     1. Upload each video to the server.
     2. Create a corresponding post.
     3. Delete the local video file after successful processing.

3. Monitor Directory:
   - The script continuously monitors the `/videos` directory for new `.mp4` files and processes them in real-time.

# API Details
-----------
The script interacts with the following API endpoints:

1. Generate Upload URL:
   - Method: `GET`
   - Endpoint: `/posts/generate-upload-url`
   - Response: Pre-signed URL and video hash.

2. Upload Video:
   - Method: `PUT`
   - URL: Pre-signed URL from Step 1.

3. Create Post:
   - Method: `POST`
   - Endpoint: `/posts`
   - Request Body:
     json
     {
         "title": "<video title>",
         "hash": "<hash>",
         "is_available_in_public_feed": false,
         "category_id": 1
     }
     

# Error Handling
--------------
- If any step fails (e.g., API errors, file upload issues), the script prints a detailed error message and skips to the next file.

# License
-------
This project is licensed under the MIT License.

# Contributing
------------
Feel free to fork this repository, make changes, and submit a pull request. Contributions are welcome! 

For questions or issues, contact the repository maintainer.
