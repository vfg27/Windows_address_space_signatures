# Windows_address_space_signatures
The objective of this project, titled "Windows Address Space Signatures," was to analyse the stability of various fields within critical kernel data structures in a Windows 10 64-bit environment. Over the course of the project, multiple snapshots were taken at different times from the same machine to determine which fields in structures such as _PEB, _TEB, _ETHREAD, _EPROCESS, and _MMVAD remained constant and which ones changed over time.
## How to run it?
### Volatility 3
To make it run you should:

1. Execute **analyze_snapshots.py** modifying in the script the path to the memory dumps to analyse and the path to volatility3 at the beginning and at the end of the script. This script will produce a folder called "volatility_outputs" in its same directory.
2. Execute **pslist_compare.py** modifying in the script the path to the “volatility_outputs” folder that the previous script “analyze_snapshots.py” generated. This script will produce a text file called "pslist_comparison_results.txt" containig the results of comparing the pslist plugin outputs.
3. Execute **thrdscan_compare.py** modifying in the script the path to the “volatility_outputs” folder that the previous script “analyze_snapshots.py” generated. This script will produce a text file called "thrdscan_comparison_results.txt" containig the results of comparing the thrdscan plugin outputs.


### Volshell
To make it run you should:

1. Execute **automate_volshell.py** modifying the path where the memory dumps are store, the path to the volatility3 folder (in the executed command) and the path to the script you want to execute. The script we want to execute in this case is **EPROCESS_script.py**, so add in **automate_volshell.py** its path. Also, modify inside **EPROCESS_script.py** the path to store the JSONs with the results. 
2. Execute  **EPROCESS_compare.py** modifying the path where the memory dumps are.

