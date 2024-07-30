# Daily Video Scheduler for TikTok Videos

This repository contains Python code that automates content planning on TikTok. It simulates user actions to upload videos and schedule their posting.

## Dependencies

* Selenium: Web automation library.
* SeleniumBase (Optional): Built on top of Selenium, provides additional functionalities (already included in this project).


## Files

* main.py: Entry point, initializes the WebDriver and calls the automate_content_planner function from PgTikTok.py.
* PgTikTok.py: Contains functions for various tasks:
    * get_info_from_script: Reads information (email, password, video path, etc.) from a text file.
    * login_to_tiktok: Logs in to TikTok using the provided credentials.
    * automate_content_planner: Handles the automation process:
        * Uploads a video.
        * Waits for upload progress to reach 100%.
        * Sets the video description.
        * Schedules the video for posting at a specific date and time (extracted from the script file).
        * Clicks "Upload Another Video" to repeat for subsequent days.


## Script.txt

* This text file must contain the following information:
```sh
Email: your_email@example.com
Password: your_password
Data_path: location of the video file
Description: Description text for the videos
Start_date: MM/DD/YYYY (format of your starting date)
Time: Time for scheduling (in HH:MM format)
Last_day_uploaded: Integer (last uploaded day)
Upload_until_day: Integer (day to stop uploading)
```

## Usage

* Install Selenium and SeleniumBase (if needed) using:
```sh
pip install selenium seleniumbase.
``` 
* Place your video file in the specified Data_path in Script.txt.
* Update any necessary information in the script file (email, password, etc.).
* To initiate the automation process use:
```sh
main.py
``` 


## Notes

* This code utilizes explicit waits and error handling mechanisms for a more robust experience.
* Customize the script file to suit your specific needs.
* The code interacts with the TikTok web interface. It's recommended to test on a non-production account and be aware of potential changes in the website structure.

