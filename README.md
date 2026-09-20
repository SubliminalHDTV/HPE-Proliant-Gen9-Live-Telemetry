# HPE-Proliant-Gen9-Live-Telemetry
Rainmeter skin for HPE Proliant Gen9 Telemetry
# HPE ProLiant Gen9 Live Telemetry Dashboard for Rainmeter

A high-speed, zero-flicker, 5-row custom desktop dashboard built for Rainmeter to monitor a remote HPE ProLiant Gen9 server running Windows Server 2022. It tracks Inlet Ambient temperature, CPU Core Thermal, and three individual chassis fan speeds natively on your desktop wallpaper background.

## 🛠️ How It Works
1. **Server Side:** HWiNFO logs system metrics continuously to a shared network folder (`C:\iLOData\ilo_live_feed.csv`).
2. **Desktop Side:** A background Python script runs every 10 seconds via Windows Task Scheduler. It securely bridges into the network share, handles authentication, extracts the exact telemetry columns by parsing backward from a massive 220+ column CSV layout, and saves it locally.
3. **Rainmeter Side:** A streamlined layout reads the local text matrix and populates 5 neon monitoring bars with 100% stable, zero-flicker memory caching.

## 📁 Repository Structure
* `ilo_temp.ini` - The Rainmeter layout skin.
* `get_live_ilo.py` - The authenticated high-speed Python backend data engine.
* `background.jpg` - Your custom dashboard background image layout.

## 🚀 Setup Instructions - Note: Double check your files locations as Onedrive can mess things up.

### 1. Server Configuration (Windows Server 2022)
* Create a folder at `C:\iLOData\` and share it over the network as `iLOData` with Read/Write permissions.
* Run HWiNFO in Sensors-only mode.
* In HWiNFO Sensor Settings -> **Logging**: Check **"Append to log file"**.
* Start logging (the green sheet icon) and save the file inside your shared folder exactly as `ilo_live_feed.csv`.

### 2. Desktop Configuration
* Install [Python for Windows](https://python.org) (Ensure you check **"Add python.exe to PATH"** during setup).
* Download the files from this repository and place them inside your Rainmeter Skins directory: `Documents\Rainmeter\Skins\iLO-Monitor\`
* Place a `background.jpg` of your choice inside that same folder.
* Open `get_live_ilo.py` and replace `"YOUR-SERVER-NAME"` with your actual server hostname.

### 3. Windows Task Scheduler Setup
To enable the high-speed 10-second background polling without flashing console windows:
* Create a Basic Task in Task Scheduler named `iLO Live Feed Engine`.
* Set the trigger to **Daily**, and action to **Start a program**.
* Point the program path to your absolute `pythonw.exe` executable.
* Add the argument: `"C:\Users\YOUR-USERNAME\Documents\Rainmeter\Skins\iLO-Monitor\get_live_ilo.py" `
* In the task's properties, check **"Run with highest privileges"**.
* Edit the trigger under Advanced Settings: check **"Repeat task every:"** and set it to **1 minute** for a duration of **Indefinitely**. 
