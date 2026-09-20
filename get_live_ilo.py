import os
import sys
import time
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
clean_txt = os.path.join(script_dir, "ilo_parsed.txt")

remote_host = "servername"
username = "username"
password = "password123"

remote_path = rf"\\{remote_host}\iLOData\ilo_live_feed.csv"
share_base = rf"\\{remote_host}\iLOData"

for _ in range(6):
    try:
        subprocess.run(f'net use "{share_base}" /delete /y', shell=True, capture_output=True)
        login_cmd = f'net use "{share_base}" "{password}" /USER:{remote_host}\\{username} /persistent:no'
        subprocess.run(login_cmd, shell=True, capture_output=True)

        with open(remote_path, mode='r', encoding='utf-8', errors='ignore') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
        if lines:
            last_line = lines[-1]
            columns = [col.strip() for col in last_line.split(',') if col.strip()]
            
            if len(columns) >= 56:
                # Core Telemetry (Original Indices)
                amb = columns[-61]
                cpu = columns[-60]
                fan1 = columns[-49] 
                fan2 = columns[-46] 
                fan3 = columns[-43] 
                
                # ==================================================
                # NEW EXPANDED SLOTS (MANUALLY ADJUST THESE THREE INDICES)
                # ==================================================
                ram_load = columns[-255]     # Swap with exact index from search tool for RAM load
                cpu_watts = columns[-160]    # Swap with exact index from search tool for CPU Power
                hdd_temp = columns[-96]     # Swap with exact index from search tool for Storage Temp
                
                with open(clean_txt, 'w', encoding='ascii') as out:
                    # Streams all 8 rows straight to the local cache file
                    out.write(f"{amb},{cpu},{fan1},{fan2},{fan3},{ram_load},{cpu_watts},{hdd_temp}\n")
    except Exception:
        pass
    
    subprocess.run(f'net use "{share_base}" /delete /y', shell=True, capture_output=True)
    time.sleep(10)
