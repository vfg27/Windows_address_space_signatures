# Windows_address_space_signatures
The objective of this project, titled "Windows Address Space Signatures," was to analyse the stability of various fields within critical kernel data structures in a Windows 10 64-bit environment. Over the course of the project, multiple snapshots were taken at different times from the same machine to determine which fields in structures such as _PEB, _TEB, _ETHREAD, _EPROCESS, and _MMVAD remained constant and which ones changed over time.
## How to run it?
### Volatility 3
To make it run you should:

1. Execute **analyze_snapshots.py** modifying in the script the path to the memory dumps to analyse and the path to volatility3 at the beginning and at the end of the script. This script will produce a folder called "volatility_outputs" in its same directory.
2. Execute **pslist_compare.py** modifying in the script the path to the “volatility_outputs” folder that the previous script “analyze_snapshots.py” generated. This script will produce a text file called "pslist_comparison_results.txt" containig the results of comparing the pslist plugin outputs.
3. Execute **thrdscan_compare.py** modifying in the script the path to the “volatility_outputs” folder that the previous script “analyze_snapshots.py” generated. This script will produce a text file called "thrdscan_comparison_results.txt" containig the results of comparing the thrdscan plugin outputs.


### Volshell
There are three scripts:
  *	**automate_volshell.py**: To make it run you should modify: the path where the memory dumps are store, the path to the volatility3 folder (in the executed command) and the path to the script you want to execute.
  *	**EPROCESS_script.py**: To make it run you should modify the path to store the JSONs. This script is executed from **automate_volshell.py**.
  *	**EPROCESS_compare.py**: This script must be executed after running **automate_volshell.py**. To make it run you must modify the path where the memory dumps are stored.

The execution order is: first run **automate_volshell.py** with **EPROCESS_script.py**. When you have the outputs, you must run **EPROCESS_compare.py** to obtain the comparison.
