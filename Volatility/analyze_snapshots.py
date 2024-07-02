import os
import subprocess
import wexpect

# Define the paths to your memory snapshots
snapshot_dir = "D:\Pilar" 
# snapshots = ["D:\Shared\memdump1.mem"]  # Add more snapshots as needed
snapshots = [os.path.join(snapshot_dir, f) for f in os.listdir(snapshot_dir) if f.endswith('.mem')]

# Define the Volatility 3 command and plugins you want to use
volatility_cmd = "python3 volatility3/vol.py -f {} {}"

# List of Volatility 3 plugins to run
plugins = ["windows.pslist", "windows.vadinfo", "windows.thrdscan", "windows.info"]

# Create a directory to store the output
output_dir = "volatility_outputs"
os.makedirs(output_dir, exist_ok=True)

for snapshot in snapshots:
    print(f'***************{os.path.basename(snapshot)}*******************\n')
    for plugin in plugins:
        print(f'***************{plugin}*******************\n')
        output_file = os.path.join(output_dir, f"{os.path.basename(snapshot).split('.')[0]}_{plugin.split('.')[1]}.txt")
        command = f"python3 volatility3/vol.py -f {snapshot} {plugin} > {output_file}"
        print(command) 
        result = subprocess.run(command, shell=True, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"An error occurred: {result.stderr}")
        else:
            print("Command executed successfully")

print("Analysis complete. Check the 'volatility_outputs' directory for results.")
