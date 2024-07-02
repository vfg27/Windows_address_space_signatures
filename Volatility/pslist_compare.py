import pandas as pd
import os

# Define column names for different table types
columns_pslist = ["PID", "PPID", "ImageFileName", "Offset(V)", "Threads", "Handles", "SessionId", "Wow64", "CreateTime", "ExitTime", "File output"]
columns_thrdscan = ["Offset", "PID", "TID", "StartAddress", "CreateTime", "ExitTime"]
columns_vadinfo = ["PID", "Process", "Offset", "Start VPN", "End VPN", "Tag", "Protection", "CommitCharge", "PrivateMemory", "Parent File", "File output"]

# Function to read the file into a DataFrame based on provided columns
def read_file(file, columns):
    with open(file, 'r') as f:
        lines = f.readlines()
        
    # Skip the first three lines (header and separator)
    data = lines[4:]
    processes = {}
    # Process each line and split into the correct number of columns
    processed_data = []
    for line in data:
        split_line = line.split(maxsplit=len(columns) - 1)
        if len(split_line) == len(columns):
            processed_data.append(split_line)
    
    # Read the data into a DataFrame
    df = pd.read_csv(file, delimiter='\t', skiprows=4, names=['PID', 'PPID', 'ImageFileName', 'Offset(V)', 'Threads', 'Handles', 'SessionId', 'Wow64', 'CreateTime', 'ExitTime', 'File output'])
    for i in range(len(df)):
        processes[int(df.iloc[i]['PID'])] = {
                    'PPID': int(df.iloc[i]['PPID']),
                    'ImageFileName': df.iloc[i]['ImageFileName'],
                    'Offset': df.iloc[i]['Offset(V)'],
                    'Threads': df.iloc[i]['Threads'],
                    'Handles': df.iloc[i]['Handles'],
                    'SessionId': str(
        'N/A' if (pd.isna(df.iloc[i]['SessionId']) or df.iloc[i]['SessionId'] == '-') 
        else int(df.iloc[i]['SessionId']) if isinstance(df.iloc[i]['SessionId'], float)
        else df.iloc[i]['SessionId']
        ),
                    'Wow64': df.iloc[i]['Wow64'],
                    'CreateTime': df.iloc[i]['CreateTime'],
                    'ExitTime': 'N/A' if (pd.isna(df.iloc[i]['ExitTime'])) else df.iloc[i]['ExitTime'],
                    'FileOutput': df.iloc[i]['File output']
                }
    return processes

def sort_key(change):
    if 'Changed' in change[1]:
        return 0
    elif 'New Process' in change[1]:
        return 1
    elif 'Terminated Process' in change[1]:
        return 2

def compare_process_lists(file1, file2):
    processes1 = read_file(file1, columns_pslist)
    processes2 = read_file(file2, columns_pslist)

    changes = []
    pids1 = set(processes1.keys())
    pids2 = set(processes2.keys())

    # Processes that are new or changed
    for pid in pids2:
        if pid not in pids1:
            changes.append((pid, 'New Process', processes2[pid]))
        else:
            process1 = processes1[pid]
            process2 = processes2[pid]
            for key in process1:
                if process1[key] != process2[key]:
                    changes.append((pid, f'Changed {key}', process1[key], process2[key]))

    # Processes that have terminated
    for pid in pids1 - pids2:
        changes.append((pid, 'Terminated Process', processes1[pid]))

    sorted_changes = sorted(changes, key=sort_key)
    changed_count = 0
    new_count = 0
    terminated_count = 0
    for change in sorted_changes:
        if 'Changed' in change[1]:
            changed_count += 1
        elif 'New Process' in change[1]:
            new_count += 1
        elif 'Terminated Process' in change[1]:
            terminated_count += 1

    return sorted_changes,changed_count,new_count,terminated_count


def main():
    directory ="C:/Users/victo/Desktop/2023-2024/Forensics/volatility_outputs" #MODIFY Path to folder resulted from the execution of analyze_snapshot.py
    output_file = 'pslist_comparison_results.txt'
    files = sorted([f for f in os.listdir(directory) if f.endswith('pslist.txt')])

    with open(output_file, 'w') as out_f:
        for i in range(len(files) - 1):
            file1 = os.path.join(directory, files[i])
            file2 = os.path.join(directory, files[i + 1])
            changes,changed,new,terminated = compare_process_lists(file1, file2)
            out_f.write(f'Comparing {files[i]} and {files[i + 1]}:\n')
            out_f.write(f'\n')
            out_f.write(f'There are {changed} Changed Processes.\n')
            out_f.write(f'There are {new} New Processes.\n')
            out_f.write(f'There are {terminated} Terminated Processes.\n')
            out_f.write(f'\n')
            for change in changes:
                out_f.write(f'{change}\n')
            out_f.write('\n')

if __name__ == '__main__':
    main()

