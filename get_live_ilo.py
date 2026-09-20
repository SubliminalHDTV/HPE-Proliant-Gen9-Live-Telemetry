import os
import sys
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
remote_host = "YOURSERVERHERE" 
remote_path = rf"\\{remote_host}\iLOData\ilo_live_feed.csv"
clean_txt = os.path.join(script_dir, "ilo_parsed.txt")

share_base = rf"\\{remote_host}\iLOData"
subprocess.run(f'net use "{share_base}" /delete /y', shell=True, capture_output=True)
login_cmd = f'net use "{share_base}" "YOURPASSWORDHERE" /USER:{remote_host}\\YOURLOGONNAMEHERE /persistent:no'
subprocess.run(login_cmd, shell=True, capture_output=True)

try:
    with open(remote_path, mode='r', encoding='utf-8', errors='ignore') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        if lines:
            last_line = lines[-1]
            columns = [col.strip() for col in last_line.split(',') if col.strip()]
            
            if len(columns) >= 204:
                amb = columns[-56]
                cpu = columns[-55]
                fan1 = columns[-44]
                fan2 = columns[-41] # Grabs Fan 2 sitting in the very next slot
                fan3 = columns[-38] # Grabs Fan 3 sitting right next to it
                
                with open(clean_txt, 'w', encoding='ascii') as out:
                    out.write(f"{amb},{cpu},{fan1},{fan2},{fan3}\n")
except Exception as e:
    pass

subprocess.run(f'net use "{share_base}" /delete /y', shell=True, capture_output=True)
