# Slurm worker exits before launching a batch script

## Verified recovery, October 7–8

The updated environment has `GetEnvTimeout=0` and a running worker. Five local
launch probes completed with exit 0:0: export ALL, ALL with an override plus
four CPUs/12 GiB and a dependency, NONE, selective export, and a subsequent
ALL submission. Fresh logs confirm that each batch script actually launched.
Evidence is retained in `notes/slurm-fix-review-20261007-V5xje1/`.
Environment repair and the subsequent HD-BET, LINDA, SynthStroke, manual
registration and DeepDisco jobs also launched successfully on October 8.
The adapter continues to request `--export=ALL`.

Old pending job IDs were reconciled after restart; those requests did not
survive, and IDs were reused. The account below is historical and must not
be used to identify or cancel current jobs. No upstream merge or image-version
claim is implied by these local checks.

## Root cause and upstream fix reported by the user

Subsequent investigation identified login-environment retrieval as the trigger
in Slurm 23.11.4, including submissions using `--export=NONE`. Slurm attempts
to create a PID namespace; Docker denies the operation, and the worker exits
before the batch script starts. The controller may still report RUNNING.
The larger resource request and dependency both worked with `--export=ALL`.
The earlier resource/dependency correlation below was not evidence of causality.

The reported upstream fix sets `GetEnvTimeout=0` for local Slurm, using an
existing environment cache or the submitted environment rather than creating
the namespace. The user reports regression coverage for the failing export
modes and subsequent jobs, with 1,296 unit tests passing. PR #1040 is awaiting
remaining image checks before merge. These are reported upstream results,
not tests executed in the CALMaR workspace.

Local verification before the image replacement showed `GetEnvTimeout = 2 sec`,
no running `slurmd`, and a DOWN node. The fix was not active at that checkpoint.
The user's newer acquisition job 4 was pending and had not been cancelled.
Worker restoration was required before dependency repair.
CALMaR's notebook adapter now requests `--export=ALL` explicitly; this does
not restore an already failed worker or replace the upstream fix.

## Reproduced after restart on October 7

The worker restarted at 01:40 UTC. A one-CPU/1-GiB control (fresh job 1)
completed at 01:47:12 with exit 0:0. The four-CPU/12-GiB probe submitted with
`afterok:1` was marked RUNNING, but created no batch logs. At 01:47:24 the
worker again logged `fatal: clone: Operation not permitted` and exited.
This reproduces the worker-launch failure without any neuroimaging tool.
That observation alone did not establish a cause; the later investigation
above identifies environment retrieval as the trigger.

An environment-repair job was submitted before the dead worker was confirmed;
it did not launch. Job 2 was cancelled; job 3 ended NODE_FAIL. Both briefly
remained COMPLETING, then cleared from the queue. Do not reuse those job IDs.
The existing `logs/calmar_environment_3.*` files are from October 6 and are
not evidence of today's installation. Scheduler adapter submissions now use
unique attempt directories for logs to prevent this ambiguity after restart.

Evidence: `notes/resume-20261007/slurmd.log` and `accounting.txt`.
The full repair still requires restoring the SLURM worker through the deployment
administrator; no server restart or security-policy change was attempted.
After restoration, repeat both launch probes with unique log paths before
running `src/analysis_20_restore_environment.sh`. Inspect actual terminal
accounting and fresh logs before submitting downstream work.

The remainder below preserves the original October 6 incident record.

Observed on 2026-10-06, UTC, Slurm 23.11.4 in Neurodesk.

The exact worker log `/var/log/slurm/slurmd.log` ends with:

```text
[2026-10-06T05:19:18.002] Launching batch job 4 for UID 1000
[2026-10-06T05:19:24.103] [4.batch] done with step
[2026-10-06T05:19:25.005] fatal: clone: Operation not permitted
```

Job 2 (workspace backup), job 3 (environment restoration) and job 4
(data acquisition) completed with exit code 0:0. Job 5 requested four CPUs,
12 GiB and 45 minutes on `neurodesktop`, within the node's configured capacity
(16 CPUs, 114184 MiB). Its submission from the CALMaR root was:

```bash
sbatch --parsable --dependency=afterok:4 --kill-on-invalid-dep=yes \
  --export=ALL,CALMAR_HDBET_MODE=fast \
  src/analysis_23_brain.sh workflow-acceptance/request.json \
  workflow-acceptance/brain workflow-acceptance/acquisition
```

The controller recorded job 5 as RUNNING, but neither its expected stdout/stderr
logs nor `/var/spool/slurmd/job00005` existed. No `slurmd`, `slurmstepd`, HD-BET
or CALMaR worker process was present. The script had not started. Jobs 5–8 were
cancelled; accounting now records cancellation for all four. No imaging output
was produced by these jobs. Job 1 had an unrelated Python dependency failure;
job 3 repaired that failure before acquisition ran.

Configuration: `TaskPlugin=task/none`, `ProctrackType=proctrack/linuxproc`,
`SelectType=select/cons_tres`, `SlurmdParameters=config_overrides`,
`SlurmdTimeout=300`. Earlier PMIx startup warnings preceded successful jobs,
so they do not by themselves explain the later crash. The exact failed clone
flags and the kernel policy rejecting them are not yet known. This is not
evidence of an HD-BET error, memory exhaustion or a bad MRI input.

## Minimal diagnostic reproduction

The following was the original October 6 probe plan; see the later execution
and diagnosis above. It is retained as historical evidence.
The worker must first be restored by an administrator. Submitting to the dead
worker would only demonstrate that the node is unavailable.

From the project root, create `logs/`, then submit the small control:

```bash
mkdir -p logs
sbatch --parsable --cpus-per-task=1 --mem=1G src/analysis_31_slurm_launch_probe.sh
```

Capture its job ID and check `squeue -j <id> -o '%i %T %R'`, then
`sacct -j <id> --format=JobID,State,ExitCode,Start,End` and its logs. If it
completes, use its ID to reproduce the original dependency/resources pattern:

```bash
sbatch --parsable --dependency=afterok:<control-job-id> \
  --kill-on-invalid-dep=yes --export=ALL,CALMAR_HDBET_MODE=fast \
  src/analysis_31_slurm_launch_probe.sh
```

This requests four CPUs and 12 GiB but only prints its identity and exits.
It loads no neuroimaging modules, downloads nothing and performs no analysis.
A failing probe would isolate the failure to launching the batch process.
A passing probe would mean the minimal case did not reproduce the incident.
The original acquisition-to-brain dependency sequence may then need testing
under an administrator's system-call trace of `slurmd`, recording clone/clone3
flags, errno, daemon credentials/capabilities and kernel security audit logs.

The installed `/opt/neurodesktop/setup_and_start_slurm.sh` explicitly requires
root. The current `jovyan` account has no passwordless sudo. Restore the worker
using the deployment's service-management procedure; do not change namespace
or security policy on the strength of this log line alone.
