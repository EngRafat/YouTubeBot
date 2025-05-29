from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# === READ LINKS FROM FILE ===
try:
    with open("links.txt", "r") as file:
        links = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print("Error: File 'links.txt' not found.")
    exit()

# === GET USER INPUT ===
timeToReopenBrowser = int(input("Reopen the browser how many times?\n"))
videoLength = int(input("How long is each video (in seconds)?\n"))

# === MAIN LOOP ===
for i in range(timeToReopenBrowser):
    print(f"Session {i + 1} starting...")

    # Use the next link in order (loop back if shorter than required)
    url = links[i % len(links)]

    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")
    # Optional: comment this out to see the browser
    # chrome_options.add_argument("--headless=new")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        sleep(5)  # Wait for page to load

        # Try to click the play button using JavaScript
        play_script = """
            var video = document.querySelector('video');
            if (video) {
                video.muted = true;  // Mute to allow autoplay
                video.play();
            }
        """
        driver.execute_script(play_script)

        print(f"Watching video {url} for {videoLength} seconds...")
        sleep(videoLength)
        driver.quit()
    except Exception as e:
        print(f"Error during session: {e}")

    print(f"Session {i + 1} finished.\n")

print("Automation complete.")
