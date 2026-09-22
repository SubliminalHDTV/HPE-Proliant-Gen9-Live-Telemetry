import os
import sys
import time
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
clean_txt = os.path.join(script_dir, "ilo_parsed.txt")

remote_host = "YOURSERVERHERE"
username = "USERNAME"
password = "PASSWORD123"

remote_path = rf"\\{remote_host}\iLOData\ilo_live_feed.csv"
share_base = rf"\\{remote_host}\iLOData"

# Memory registers to hold column positions across loops
idx_amb = idx_cpu = idx_fan1 = idx_fan2 = idx_fan3 = idx_ram = idx_pwr = idx_hdd = None
indices_cached = False

# HIGH-SPEED LOOP: Executes natively 6 times over 60 seconds
for _ in range(6):
    try:
        # Establish network lane connection
        subprocess.run(f'net use "{share_base}" /delete /y', shell=True, capture_output=True)
        login_cmd = f'net use "{share_base}" "{password}" /USER:{remote_host}\\{username} /persistent:no'
        subprocess.run(login_cmd, shell=True, capture_output=True)

        with open(remote_path, mode='r', encoding='utf-8', errors='ignore') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
        if len(lines) >= 2:
            last_row = lines[-1]
            columns = [c.strip() for c in last_row.split(',')]

            # ONLY SCAN HEADERS ONCE: Saves huge network and processing overhead
            if not indices_cached:
                header_row = lines[0]
                headers = [h.strip().lower() for h in header_row.split(',')]
                
                idx_amb = next((i for i, h in enumerate(headers) if "inlet" in h or "ambient" in h), None)
                idx_cpu = next((i for i, h in enumerate(headers) if "cpu" in h and "package" in h) or (i for i, h in enumerate(headers) if "cpu 1" in h), None)
                idx_fan1 = next((i for i, h in enumerate(headers) if "fan 1" in h or "fan1" in h), None)
                idx_fan2 = next((i for i, h in enumerate(headers) if "fan 2" in h or "fan2" in h), None)
                idx_fan3 = next((i for i, h in enumerate(headers) if "fan 3" in h or "fan3" in h), None)
                idx_ram  = next((i for i, h in enumerate(headers) if "memory" in h and "load" in h) or (i for i, h in enumerate(headers) if "ram" in h and "load" in h), None)
                idx_pwr  = next((i for i, h in enumerate(headers) if "cpu" in h and "power" in h) or (i for i, h in enumerate(headers) if "package" in h and "power" in h), None)
                idx_hdd  = next((i for i, h in enumerate(headers) if "drive" in h and "temp" in h) or (i for i, h in enumerate(headers) if "smart" in h and "array" in h), None)
                indices_cached = True

            # Instant data mapping using memory registers
            amb = columns[idx_amb] if (idx_amb is not None and idx_amb < len(columns)) else "22.0"
            cpu = columns[idx_cpu] if (idx_cpu is not None and idx_cpu < len(columns)) else "50.0"
            fan1 = columns[idx_fan1] if (idx_fan1 is not None and idx_fan1 < len(columns)) else "13.3"
            fan2 = columns[idx_fan2] if (idx_fan2 is not None and idx_fan2 < len(columns)) else "13.3"
            fan3 = columns[idx_fan3] if (idx_fan3 is not None and idx_fan3 < len(columns)) else "14.1"
            ram = columns[idx_ram] if (idx_ram is not None and idx_ram < len(columns)) else "15.0"
            pwr = columns[idx_pwr] if (idx_pwr is not None and idx_pwr < len(columns)) else "45.0"
            hdd = columns[idx_hdd] if (idx_hdd is not None and idx_hdd < len(columns)) else "35.0"
            
            with open(clean_txt, 'w', encoding='ascii') as out:
                out.write(f"{amb},{cpu},{fan1},{fan2},{fan3},{ram},{pwr},{hdd}\n")
    except Exception:
        pass
    
    subprocess.run(f'net use "{share_base}" /delete /y', shell=True, capture_output=True)
    time.sleep(10)
