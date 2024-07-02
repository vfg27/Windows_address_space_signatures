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
    df = pd.read_csv(file, delimiter='\t', skiprows=4, names=["Offset", "PID", "TID", "StartAddress", "CreateTime", "ExitTime"])
    for i in range(len(df)):
        processes[int(df.iloc[i]['TID'])] = {
                'Offset': df.iloc[i]['Offset'],
                'PID': int(df.iloc[i]['PID']),
                'StartAddress': df.iloc[i]['StartAddress'],
                'CreateTime': df.iloc[i]['CreateTime'],
                'ExitTime': df.iloc[i]['ExitTime']
            }
    return processes

def sort_key(change):
    if 'Changed' in change[1]:
        return 0
    elif 'New Thread' in change[1]:
        return 1
    elif 'Terminated Thread' in change[1]:
        return 2
    

def compare_process_lists(file1, file2):
    processes1 = read_file(file1, columns_thrdscan)
    processes2 = read_file(file2, columns_thrdscan)

    changes = []
    tids1 = set(processes1.keys())
    tids2 = set(processes2.keys())

    # Tracking distinct TIDs and key changes
    distinct_tids_changed = set()
    key_change_counts = {}

    # Processes that are new or changed
    for tid in tids2:
        if tid not in tids1:
            changes.append((tid, 'New Thread', processes2[tid]))
        else:
            process1 = processes1[tid]
            process2 = processes2[tid]
            for key in process1:
                if process1[key] != process2[key]:
                    changes.append((tid, f'Changed {key}', process1[key], process2[key]))
                    distinct_tids_changed.add(tid)
                    if key in key_change_counts:
                        key_change_counts[key] += 1
                    else:
                        key_change_counts[key] = 1

    # Processes that have terminated
    for tid in tids1 - tids2:
        changes.append((tid, 'Terminated Thread', processes1[tid]))

    sorted_changes = sorted(changes, key=sort_key)
    changed_count = 0
    new_count = 0
    terminated_count = 0
    for change in sorted_changes:
        if 'Changed' in change[1]:
            changed_count += 1
        elif 'New Thread' in change[1]:
            new_count += 1
        elif 'Terminated Thread' in change[1]:
            terminated_count += 1
    distinct_tids_changed_count = len(distinct_tids_changed)
    return sorted_changes,changed_count,new_count,terminated_count, distinct_tids_changed_count, key_change_counts


def main():
    directory ="C:/Users/victo/Desktop/2023-2024/Forensics/volatility_outputs" #MODIFY Path to folder resulted from the execution of analyze_snapshot.py
    output_file = 'thrdscan_comparison_results.txt'
    files = sorted([f for f in os.listdir(directory) if f.endswith('thrdscan.txt')])

    with open(output_file, 'w') as out_f:
        for i in range(len(files) - 1):
            file1 = os.path.join(directory, files[i])
            file2 = os.path.join(directory, files[i + 1])
            changes,changed,new,terminated, distinct_tids_changed,key_change_counts = compare_process_lists(file1, file2)
            out_f.write(f'Comparing {files[i]} and {files[i + 1]}:\n')
            out_f.write(f'\n')
            out_f.write(f'There are {changed} changes in the threads.\n')
            out_f.write(f'There are {new} New Threads.\n')
            out_f.write(f'There are {terminated} Terminated Threads.\n')
            out_f.write(f'There are {distinct_tids_changed} distinct TIDs that have changed.\n')
            out_f.write('Key change counts:\n')
            for key, count in key_change_counts.items():
                out_f.write(f'  {key}: {count}\n')
            out_f.write(f'\n')
            for change in changes:
                out_f.write(f'{change}\n')
            out_f.write('\n')

if __name__ == '__main__':
    main()