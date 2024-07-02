import json
import datetime

fields = ['ImageFileName', 'AccountingFolded', 'ActiveProcessLinks', 'ActiveThreads', 'ActiveThreadsHighWatermark', 'AddressPolicyFrozen', 'AddressSpaceInitialized', 'AffinityPermanent', 'AffinityUpdateEnable', 'AllowedCpuSets', 'AllowedCpuSetsIndirect', 'AltSyscall', 'AuxiliaryProcess', 'Background', 'BreakOnTermination', 'CommitCharge', 'CommitChargeJob', 'CommitChargeLimit', 'CommitChargePeak', 'CommitFailLogged', 'Cookie', 'CoverageSamplerContext', 'Crashed', 'CreateInterruptTime', 'CreateReported', 'CreateTime', 'CreateUnbiasedInterruptTime', 'CrossSessionCreate', 'DebugPort', 'DefaultCpuSets', 'DefaultCpuSetsIndirect', 'DefaultHardErrorProcessing', 'DefaultIoPriority', 'DefaultPagePriority', 'DeprioritizeViews', 'DeviceAsid', 'DeviceMap', 'DisableSystemAllowedCpuSet', 'DisabledComponentFlags', 'DisallowUserTerminate', 'DiskCounters', 'DiskIoAttribution', 'DxgProcess', 'EmptyJobEvaluated', 'EnableProcessSuspendResumeLogging', 'EnableReadVmLogging', 'EnableThreadSuspendResumeLogging', 'EnableWriteVmLogging', 'EnclaveNumber', 'EnclaveTable', 'EnergyContext', 'EtwDataSource', 'ExceptionPortData', 'ExceptionPortState', 'ExceptionPortValue', 'ExitProcessReported', 'ExitStatus', 'ExitTime', 'ExplicitAffinity', 'FailFastOnCommitFail', 'FatalAccessTerminationRequested', 'Flags', 'Flags2', 'Flags3', 'ForceWakeCharge', 'ForegroundExternal', 'ForegroundSystem', 'ForkInProgress', 'GhostCount', 'HangCount', 'HasAddressSpace', 'HideImageBaseAddresses', 'HighGraphicsPriority', 'HighMemoryPriority', 'HighPriorityFaultsAllowed', 'HighestUserAddress', 'ImageFilePointer', 'ImageNotifyDone', 'ImagePathHash', 'InPrivate', 'IndirectCpuSets', 'InheritedFromUniqueProcessId', 'InvertedFunctionTable', 'Job', 'JobLinks', 'JobNotReallyActive', 'JobVadsAreTracked', 'KTimer2Sets', 'KTimerSets', 'LargePrivateVadCount', 'LastAppState', 'LastAppStateUpdateTime', 'LastAppStateUptime', 'LastFreezeInterruptTime', 'LastReportMemory', 'LastThreadExitStatus', 'LaunchPrefetched', 'LockedPagesList', 'ManageExecutableMemoryWrites', 'Minimal', 'MitigationFlags', 'MitigationFlags2', 'MitigationFlags3', 'MmHotPatchContext', 'MmProcessLinks', 'MmReserved', 'ModifiedPageCount', 'NeedsHandleRundown', 'NewProcessReported', 'NoDebugInherit', 'NumberOfLockedPages', 'NumberOfPrivatePages', 'ObjectTable', 'OtherOperationCount', 'OtherTransferCount', 'OutswapEnabled', 'Outswapped', 'OverrideAddressSpace', 'OwnerProcessId', 'PageDirectoryPte', 'ParentSecurityDomain', 'PartitionObject', 'PathRedirectionHashes', 'PdeUpdateNeeded', 'PeakVirtualSize', 'Peb', 'PicoContext', 'PicoCreated', 'PrefetchTrace', 'PrefilterException', 'PrimaryTokenFrozen', 'PriorityClass', 'ProcessDelete', 'ProcessExecutionState', 'ProcessExiting', 'ProcessFirstResume', 'ProcessInSession', 'ProcessInserted', 'ProcessQuotaPeak', 'ProcessQuotaUsage', 'ProcessRundown', 'ProcessSelfDelete', 'ProcessStateChangeInProgress', 'ProcessStateChangeRequest', 'ProcessTimerDelay', 'ProcessVerifierTarget', 'PropagateNode', 'QuotaBlock', 'ReadOperationCount', 'ReadTransferCount', 'RefTraceEnabled', 'RelinquishedCommit', 'ReplacingPageRoot', 'ReportCommitChanges', 'RequestedTimerResolution', 'ReserveFailLogged', 'RestrictSetThreadContext', 'RotateInProgress', 'SectionBaseAddress', 'SectionObject', 'SectionSignatureLevel', 'SecurityDomain', 'SecurityDomainChanged', 'SecurityFreezeComplete', 'SecurityPort', 'SequenceNumber', 'ServerSilo', 'Session', 'SessionProcessLinks', 'SetTimerResolution', 'SetTimerResolutionLink', 'SharedCommitCharge', 'SharedCommitLinks', 'SignatureLevel', 'SmallestTimerResolution', 'Spare1', 'SubsystemProcess', 'SvmData', 'SvmLock', 'SvmProcessDeviceListHead', 'SystemProcess', 'ThreadListHead', 'ThreadTimerSets', 'TimerResolutionIgnore', 'TimerResolutionLink', 'TimerResolutionStackRecord', 'Token', 'TotalUnbiasedFrozenTime', 'UniqueProcessId', 'VadCount', 'VadHint', 'VadPhysicalPages', 'VadPhysicalPagesLimit', 'VadTrackingDisabled', 'VdmAllowed', 'VirtualSize', 'VirtualTimerListHead', 'VirtualTimerListLock', 'VmContext', 'VmDeleted', 'VmProcessorHost', 'VmProcessorHostTransition', 'VmTopDown', 'Win32KFilterSet', 'Win32Process', 'Win32WindowStation', 'WnfContext', 'WoW64Process', 'WorkingSetWatch', 'Wow64VaSpace4Gb', 'WriteOperationCount', 'WriteTransferCount', 'WriteWatch']
def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4, default=str)  # Use default=str to handle non-serializable values

def get_process_attributes():
    # Retrieve the attribute dictionary for EPROCESS
    processes = lp()
    for i in range(len(processes)):
        actualPS = processes[i]
        pid = actualPS.UniqueProcessId
        res = {}
        for field in fields:
            data = getattr(actualPS, field)
            # UnionType
            if field in ('CreateTime', 'ExitTime'):
                time=data.QuadPart
                windows_epoch = datetime.datetime(1601, 1, 1)
                res_datetime = windows_epoch + datetime.timedelta(microseconds=time / 10)
                if time != 0:
                    res[field] = res_datetime
                else:
                    res[field] = 'N/A'
            # UnionType
            elif field in ('OtherOperationCount', 'OtherTransferCount', 'ReadOperationCount', 'ReadTransferCount', 'WriteOperationCount', 'WriteTransferCount'):
                value = data.QuadPart
                res[field] = value
            # UnionType
            elif field == 'ProcessTimerDelay':
                value = data.All
                res[field] = value
            # LIST_ENTRY
            elif field in ('ActiveProcessLinks', 'JobLinks', 'MmProcessLinks', 'SessionProcessLinks', 'SharedCommitLinks', 'ThreadListHead', 'VirtualTimerListHead'):
                value = {}
                value['Blink'] = data.Blink
                value['Flink'] = data.Flink
                res[field] = value
            # EX_FAST_REF
            elif field in ('Token', 'PrefetchTrace'):
                value = {}
                value['Object'] = data.Object
                value['RefCnt'] = data.RefCnt
                value['Value'] = data.Value
                res[field] = value
            # ARRAY
            elif field in ('ImageFileName'):
                res[field] = data.cast("string", max_length= 24)
            # ARRAY
            elif field in ('ProcessQuotaPeak', 'ProcessQuotaUsage'):
                res[field] = data.cast("int")
            else:
                try:
                    part = {}
                    for key in data:
                        part[key] = data[key]
                    res[field] = part
                except Exception as e:
                    res[field] = data
        filename = f"D:/Pilar/volshell_outs/process_{pid}.json" # MODIFY PATH. It should be: <Path to the folder with the memory dumps>/volshell_outs/process_{pid}.json
        save_to_json(res, filename)     

get_process_attributes()
