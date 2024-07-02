import os
import json
from collections import defaultdict

def load_processes_from_folder(folder_path):
    processes = {}
    for filename in os.listdir(folder_path):
        if filename.startswith("process_") and filename.endswith(".json"):
            pid = filename.split('_')[1].split('.')[0]
            with open(os.path.join(folder_path, filename), 'r') as file:
                processes[pid] = json.load(file)
    return processes

def compare_processes(prev_processes, current_processes):
    added = set(current_processes.keys()) - set(prev_processes.keys())
    removed = set(prev_processes.keys()) - set(current_processes.keys())
    common = set(prev_processes.keys()) & set(current_processes.keys())

    changed = defaultdict(list)
    field_changes_count = defaultdict(int)
    for pid in common:
        prev_fields = prev_processes[pid]
        curr_fields = current_processes[pid]
        for key in curr_fields.keys():
            if key in prev_fields and prev_fields[key] != curr_fields[key]:
                changed[pid].append((key, prev_fields[key], curr_fields[key]))
                field_changes_count[key] += 1
    
    return added, removed, changed, field_changes_count

def get_process_name(process):
    return process.get('ImageFileName', 'Unknown')

def main():
    base_path = "D:/Pilar" # MODIFY Path to memory dumps
    result_file_complete = "comparison_results_complete.txt"
    result_file_brief = "comparison_results_brief.txt"

    time_points = sorted([d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))])
    previous_processes = {}

    with open(result_file_complete, 'w') as result:
        for i in range(1, len(time_points)):
            prev_folder = os.path.join(base_path, time_points[i-1])
            curr_folder = os.path.join(base_path, time_points[i])

            prev_processes = load_processes_from_folder(prev_folder)
            curr_processes = load_processes_from_folder(curr_folder)

            added, removed, changed, field_changes_count = compare_processes(prev_processes, curr_processes)

            result.write(f"Comparison between {time_points[i-1]} and {time_points[i]}:\n")
            result.write(f"Number of processes added: {len(added)}\n")
            result.write(f"Number of processes terminated: {len(removed)}\n")
            result.write(f"Number of processes changed: {len(changed)}\n")
            result.write(f"Number of changes per field:\n")
            for field, count in field_changes_count.items():
                result.write(f"  Field {field}: {count} changes\n")
            if added:
                result.write("Added PIDs: ")
                result.write(", ".join([f"{pid} ({get_process_name(curr_processes[pid])})" for pid in added]) + "\n")
            if removed:
                result.write("Removed PIDs: ")
                result.write(", ".join([f"{pid} ({get_process_name(prev_processes[pid])})" for pid in removed]) + "\n")
            if changed:
                result.write("Changed PIDs:\n")
                for pid, changes in changed.items():
                    result.write(f"  PID {pid} ({get_process_name(curr_processes[pid])}):\n")
                    for change in changes:
                        result.write(f"    Field {change[0]} changed from {change[1]} to {change[2]}\n")
            result.write("\n")

    with open(result_file_brief, 'w') as result:
        for i in range(1, len(time_points)):
            prev_folder = os.path.join(base_path, time_points[i-1])
            curr_folder = os.path.join(base_path, time_points[i])

            prev_processes = load_processes_from_folder(prev_folder)
            curr_processes = load_processes_from_folder(curr_folder)

            added, removed, changed, field_changes_count = compare_processes(prev_processes, curr_processes)

            result.write(f"Comparison between {time_points[i-1]} and {time_points[i]}:\n")
            result.write(f"Number of processes added: {len(added)}\n")
            result.write(f"Number of processes terminated: {len(removed)}\n")
            result.write(f"Number of processes changed: {len(changed)}\n")
            result.write(f"Number of changes per field:\n")
            for field, count in field_changes_count.items():
                result.write(f"  Field {field}: {count} changes\n")
            if added:
                result.write("Added PIDs: ")
                result.write(", ".join([f"{pid} ({get_process_name(curr_processes[pid])})" for pid in added]) + "\n")
            if removed:
                result.write("Removed PIDs: ")
                result.write(", ".join([f"{pid} ({get_process_name(prev_processes[pid])})" for pid in removed]) + "\n")
            if changed:
                result.write("Changed PIDs: ")
                result.write(", ".join([f"{pid} ({get_process_name(curr_processes[pid])})" for pid in changed.keys()]) + "\n")
            result.write("\n")

if __name__ == "__main__":
    main()
