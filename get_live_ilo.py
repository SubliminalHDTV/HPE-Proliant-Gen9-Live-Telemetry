import os
import sys
import time

# Absolute path setup
script_dir = os.path.dirname(os.path.abspath(__file__))
# REPLACE THIS WITH YOUR ACTUAL WINDOWS SERVER COMPUTER HOSTNAME
remote_host = "YOURSERVERHERE" 
remote_path = rf"\\{remote_host}\iLOData\ilo_live_feed.csv"
clean_txt = os.path.join(script_dir, "ilo_parsed.txt")

# HIGH-SPEED EXECUTION LOOP: Runs 6 times natively over 60 seconds
for _ in range(6):
    try:
        # PURE READ-ONLY STREAM: Zero locks, zero edits, zero risk to HWiNFO
        with open(remote_path, mode='r', encoding='utf-8', errors='ignore') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
        if lines:
            last_line = lines[-1]
            columns = [col.strip() for col in last_line.split(',') if col.strip()]
            
            if len(columns) >= 204:
                # Utilizing your verified custom fan index pointers
                amb = columns[-56]
                cpu = columns[-55]
                fan1 = columns[-44] 
                fan2 = columns[-41] 
                fan3 = columns[-38] 
                
                with open(clean_txt, 'w', encoding='ascii') as out:
                    out.write(f"{amb},{cpu},{fan1},{fan2},{fan3}\n")
    except Exception:
        pass
    
    # Pauses the thread for exactly 10 seconds before hitting the next beat
    time.sleep(10)
