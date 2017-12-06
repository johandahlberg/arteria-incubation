Arteria pack
============

This is the new and improved version of the Arteria StackStorm pack, it has been
considerably slimmed down compared to previous version.

The aim of this pack is to provide re-usable units for automating tasks at a
sequencing core. However, the type of things presented here can be of use to any
group which does enough sequencing that a high degree of automation is necessary.

This pack is indented as a starting point, not a turn-key solution. Most sequencing cores
will have a sufficiently unique environment that a specialized solution has to be developed,
however, the components provided here can make that work easier.

For more information on Arteria in general, look at our pre-print here:
https://www.biorxiv.org/content/early/2017/11/06/214858

Acknowledgements
================
The docker environment provided here has been heavily inspired by the one provided by
[StackStorm](https://github.com/StackStorm/st2-docker) and [UMCCR](https://github.com/umccr/st2-arteria-docker).

What does Arteria pack do?
==========================
TODO

General outline of system
=========================
TODO

Usage
=====

Getting started / Installation
------------------------------
In order to have an development environment in which to get started quickly, we provide a
Docker based environment with the repository.

To get started with it follow the installation guides for you platform for [Docker](https://docs.docker.com/engine/installation/)
 and [Docker Compose](https://docs.docker.com/compose/install/).

Once you have that installed, ensure that you have Make installed (should be available from
your favorite package manager). Then you can get the sytem up and running by executing the
following command:

```
make up
```

Congratulations, you're now ready to get started trying out the Arteria pack.

To get into the StackStorm master node, run:

```
make interact
```

Running a workflow
------------------
Once you are inside the StackStorm container, it's time to install and configure the
Arteria pack. You only need to do this the first time you bring up the environment
(or if you re-build it later).

```
# Copy the default config into the StackStorm config directory
cp /opt/stackstorm/packs/arteria/default.config.yaml /opt/stackstorm/configs/arteria.yaml

# Register packs and configuration values
st2ctl reload --register-all

# Ensure that the Arteria virtual env is installed
st2 run packs.setup_virtualenv packs=arteria
```

Now the environment should be ready to run a workflow.

All you need to do is place a runfolder under `docker-mountpoints/monitored-directory`,
then give its path as a parameter when initiating the workflow:

```
st2 run arteria.workflow_bcl2fastq_and_checkqc runfolder_path="/opt/monitored-folder/<runfolder name>"
```

Eventually you should see something like this:

```
id: 5a2516ea10895200eb467b63
action.ref: arteria.workflow_bcl2fastq_and_checkqc
parameters:
  runfolder_path: /opt/monitored-folder/my_runfolder
status: succeeded (286s elapsed)
result_task: mark_as_done
result:
  exit_code: 0
  result: true
  stderr: ''
  stdout: ''
start_timestamp: 2017-12-04T09:35:38.361039Z
end_timestamp: 2017-12-04T09:40:24.743737Z
+--------------------------+--------------------------+--------------------+---------------------------+-------------------------------+
| id                       | status                   | task               | action                    | start_timestamp               |
+--------------------------+--------------------------+--------------------+---------------------------+-------------------------------+
| 5a2516eb10895200eb467b66 | succeeded (1s elapsed)   | get_runfolder_name | core.local                | Mon, 04 Dec 2017 09:35:38 UTC |
| 5a2516eb10895200eb467b68 | succeeded (1s elapsed)   | mark_as_started    | arteria.runfolder-service | Mon, 04 Dec 2017 09:35:39 UTC |
| 5a2516ed10895200eb467b6a | succeeded (1s elapsed)   | start_bcl2fastq    | arteria.bcl2fastq-service | Mon, 04 Dec 2017 09:35:41 UTC |
| 5a2516ef10895200eb467b6c | succeeded (267s elapsed) | poll_bcl2fastq     | arteria.bcl2fastq-service | Mon, 04 Dec 2017 09:35:42 UTC |
| 5a2517fd10895200eb467b6e | succeeded (1s elapsed)   | checkqc            | core.http                 | Mon, 04 Dec 2017 09:40:13 UTC |
| 5a2517fe10895200eb467b70 | succeeded (1s elapsed)   | mark_as_done       | arteria.runfolder-service | Mon, 04 Dec 2017 09:40:14 UTC |
+--------------------------+--------------------------+--------------------+---------------------------+-------------------------------+
```

Indicating that you have successfully executed a workflow which has demultiplexed the runfolder
 using bcl2fastq and and checked its quality control statistics using [CheckQC](https://github.com/Molmed/checkQC).

Starting a workflow through a sensor
------------------------------------
The way that Stackstorm will detect changes in the surrounding environment is through sensors.
In this pack there is a sensor called the `RunfolderSensor`, which will query the the runfolder
service for information about the state of runfolders.

To activate the rule, i.e. the part that glues the sensor and a workflow/action together,
run:

```
st2 rule enable arteria.when_runfolder_is_ready_start_bcl2fastq
```

Then to start processing the runfolder, set its state to `ready` using:

```
st2 run arteria.runfolder_service cmd="set_state" state="ready" runfolder="/opt/monitored-folder/<name of your runfolder>" url="http://runfolder-service"
```

Withing 15s you should if you execute `st2 execution list` see that a workflow processing that runfolder
has started. This is the way that Arteria can be used to automatically start processes as needed.

Running tests
-------------

To run the pack tests, run the following command in the StackStorm container:

```
st2-run-pack-tests -c -v -p /opt/stackstorm/packs/arteria
```
