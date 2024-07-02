import os
import subprocess
import json
import wexpect
import shutil

# Define the paths to your memory snapshots
snapshot_dir = "D:/Pilar"  #MODIFY Path to memory dumps
snapshots = [os.path.join(snapshot_dir, f) for f in os.listdir(snapshot_dir) if f.endswith('.mem')]

# Directory to store the output
output_dir = "volshell_outs"
output_dir =os.path.join(snapshot_dir, output_dir)
os.makedirs(output_dir, exist_ok=True)

# Volshell script path
volshell_script = "EPROCESS_script.py"

# Function to run Volshell with the given script
def run_volshell(snapshot):
    command = f"python3 volatility3/volshell.py -f {snapshot} -w --script {volshell_script}" #MODIFY PATH TO VOLATILITY3
    print(command)
    # Start cmd as child process
    child = wexpect.spawn('cmd.exe')

    # Wait for prompt when cmd becomes ready.
    child.expect('>')

    # run list directory command
    child.sendline(command)

    # Wait for prompt when cmd becomes ready.
    child.expect('>', timeout=45)

    # Exit from cmd
    child.sendline('exit()')

    child.expect('>')

    child.sendline('exit')

    # Waiting for cmd termination.
    child.wait()


# Run Volshell and split the JSON output for each snapshot
for snapshot in snapshots:
    print(f'***************{os.path.basename(snapshot)}*******************')
    run_volshell(snapshot)
    
    string="EPROCESS-"+os.path.basename(snapshot).split('.')[0]
    destination = os.path.join(snapshot_dir, string)
    os.makedirs(destination, exist_ok=True)

    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        shutil.move(file_path, destination)
shutil.rmtree(output_dir)
print("Automated Volshell analysis complete.")
