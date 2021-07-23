---
description: GBAR - Graph Backup and Restore
---

# Backup and Restore

Graph Backup And Restore \(GBAR, is an integrated tool for backing up and restoring the data and data dictionary \(schema, loading jobs, and queries\) of a single TigerGraph node. 

The backup feature packs TigerGraph data and configuration information in a single file onto the disk or a remote AWS S3 bucket. Multiple backup files can be archived. Later, you can use the restore feature to roll back the system to any backup point. This tool can also be integrated easily with Linux cron to perform periodic backup jobs.

### Introduction and Syntax <a id="GBAR-GraphBackupandRestorev2.1-IntroductionandSyntax"></a>

{% hint style="info" %}
The current version of GBAR is intended for restoring the same machine that was backed up. For help with cloning a database \(i.e., backing up machine A and restoring the database to machine B\), please contact [support@tigergraph.com](mailto:support@tigergraph.com).
{% endhint %}

{% code title="Synopsis" %}
```text
Usage: gbar backup [options] -t <backup_tag>
       gbar restore [options] <backup_tag>
       gbar config
       gbar list

Options:
  -h, --help     Show this help message and exit
  -v             Run with debug info dumped
  -vv            Run with verbose debug info dumped
  -y             Run without prompt
  -t BACKUP_TAG  Tag for backup file, required on backup
```
{% endcode %}

  
The `-y` option forces GBAR to skip interactive prompt questions by selecting the default answer. There is currently one interactive question:

* At the start of restore, GBAR will always ask if it is okay to stop and reset the TigerGraph services: \(y/N\)? The default answer is yes.

### Configure GBAR  <a id="config"></a>

Before using the backup or the restore feature, GBAR must be configured.  

1. Run `gadmin config entry system.backup`, At each prompt, enter the appropriate values for each config parameter.

   ```bash
   $ gadmin config entry system.backup
 
   System.Backup.TimeoutSec [ 18000 ]: The backup timeout in seconds
   New: 18000
 
   System.Backup.CompressProcessNumber [ 8 ]: The number of concurrent process for compression during backup
   New: 8
 
   System.Backup.Local.Enable [ true ]: Backup data to local path
   New: true
 
   System.Backup.Local.Path [ /tmp/backup ]: The path to store the backup files
   New: /data/backup
 
   System.Backup.S3.Enable [ false ]: Backup data to S3 path
   New: false
 
   System.Backup.S3.AWSAccessKeyID [ <masked> ]: The path to store the backup files
   New:
 
   System.Backup.S3.AWSSecretAccessKey [ <masked> ]: The path to store the backup files
   New:
 
   System.Backup.S3.BucketName [  ]: The path to store the backup files
   New:

   ```

2. After entering the configuration values, run the following command to apply the new configurations

   ```text
   gadmin config apply -y
   ```

**Note**: 

* For S3 configuration, the AWS access key and secret are not provided, then GBAR will use the attached IAM role.
* You can specify the number of parallel processes for backup and restore.
* You must provide username and password using GSQL\_USERNAME and GSQL\_PASSWORD environment variables.

  ```
  $ GSQL_USERNAME=tigergraph GSQL_PASSWORD=tigergraph gbar backup -t daily
  ```

### Perform a backup <a id="backup"></a>

To perform a backup, run the following command as the TigerGraph Linux user:

```text
gbar backup -t <backup_tag>
```

Depending on your configuration settings, your backup archive will be output to your local backup path and/or your AWS S3 bucket. 

A backup archive is stored as several files in a folder, rather than as a single file. The backup tag acts like a filename prefix for the archive filename. The full name of the backup archive will be `<backup_tag>-<timestamp>`, which is a subfolder of the backup repository.

* If `System.Backup.Local.Enable` is set to `true`, the folder is a local folder on every node in a cluster, to avoid massive data moving across nodes in a cluster. 
* If `System.Backup.S3.Enable` is set to `true`, every node will upload data located on the node to the s3 repository. Therefore, every node in a cluster needs access to Amazon S3. If IAM policy is used for authentication, every node in the cluster needs to be given access under the IAM policy.

GBAR Backup performs a live backup, meaning that normal operations may continue while the backup is in progress. When GBAR backup starts, GBAR will check if there are running loading jobs. If there are, it will pause loading for 1 minute to generate a snapshot and then continue the backup process. You can specify the loading pausing interval by the environment variable `PAUSE_LOADING`. 

And then, it sends a request to the admin server, which then requests the GPE and GSE to create snapshots of their data. Per the request, the GPE and GSE store their data under GBAR’s own working directory. GBAR also directly contacts the Dictionary and obtains a dump of its system configuration information. In addition, GBAR gathers the TigerGraph system version and customized information including user-defined functions, token functions, schema layouts and user-uploaded icons. Then, GBAR compresses each of these data and configuration information files in tgz format and stores them in the `<backup_tag>-<timestamp>` subfolder on each node. As the last step, GBAR copies that file to local storage or AWS S3, according to the Config settings, and removes all temporary files generated during backup.

The current version of GBAR Backup takes snapshots quickly to make it very likely that all the components \(GPE, GSE, and Dictionary\) are in a consistent state, but it does not fully guarantee consistency. 

{% hint style="danger" %}
Backup does not save input message queues for REST++ or Kafka.
{% endhint %}

### List Backup Files <a id="list-backup-files"></a>

```text
gbar list
```

This command lists all generated backup files in the storage place configured by the user. For each file, it shows the file’s full tag, its size in human-readable format, and its creation time.

### Restore from a backup archive <a id="restore"></a>

1. Before restoring a backup, you should ensure that the backup you are restoring from is compatible with your current version of TigerGraph:
   * TigerGraph version numbers have the format X.Y\[.Z\], where X is the major version number and Y is the minor version number.
   * Restore is supported if the backup archive and the current system have the same major version number AND the current system has a minor version number that is greater than or equal to the backup archive minor version number.
2. To restore a backup, run the following command:

```text
gbar restore <archive_name>
```

If GBAR can verify that the backup archive exists and that the backup's system version is compatible with the current system version, GBAR will shut down the TigerGraph servers temporarily as it restores the backup. After completing the restore, GBAR will restart the TigerGraph servers. 

Restore is an offline operation, requiring the data services to be temporarily shut down. The user must specify the full archive name \( `<backup_tag>-<timestamp>` \) to be restored. When GBAR restore begins, it first searches for a backup archive exactly matching the archive name supplied in the command line. Then it decompresses the backup files to a working directory. Next, GBAR will compare the TigerGraph system version in the backup archive with the current system's version, to make sure that the backup archive is compatible with that current system. It will then shut down the TigerGraph servers \(GSE, RESTPP, etc.\) temporarily. Then, GBAR makes a copy of the current graph data, as a precaution. Next, GBAR copies the backup graph data into the GPE and GSE and notifies the Dictionary to load the configuration data. Also, GBAR will notify the GST to load backup user data and copy the backup user-defined token/functions to the right location. When these actions are all done, GBAR will restart the TigerGraph servers.

**Note**: GBAR restore does not estimate the uncompressed data size and check whether there is sufficient disk space.

{% hint style="info" %}
The primary purpose of GBAR is to save snapshots of the data configuration of a TigerGraph system, so that in the future the same system can be rolled back \(restored\) to one of the saved states. A key assumption is that Backup and Restore are performed on the same machine, and that the file structure of the TigerGraph software has not changed. 
{% endhint %}

{% hint style="danger" %}
Restore needs enough free space to accommodate both the old gstore and the gstore to be restored.
{% endhint %}

### GBAR Detailed Example <a id="gbar-detailed-example"></a>

The following example describes a real example, to show the actual commands, the expected output, and the amount of time and disk space used, for a given set of graph data. For this example, an Amazon EC2 instance was used, with the following specifications:

Single instance with 32 vCPU + 244GB memory + 2TB HDD.

Naturally, backup and restore time will vary depending on the hardware used.

#### GBAR Backup Operational Details <a id="gbar-backup-operational-details"></a>

 To run a daily backup, we tell GBAR to backup with the tag name _daily_.

```text
$ gbar backup -t daily
[23:21:46] Retrieve TigerGraph system configuration
[23:21:51] Start workgroup
[23:21:59] Snapshot GPE/GSE data
[23:33:50] Snapshot DICT data
[23:33:50] Calc checksum
[23:37:19] Compress backup data
[23:46:43] Pack backup data
[23:53:18] Put archive daily-20180607232159 to repo-local
[23:53:19] Terminate workgroup
Backup to daily-20180607232159 finished in 31m33s.
```

The total backup process took about 31 minutes, and the generated archive is about 49 GB. Dumping the GPE + GSE data to disk took 12 minutes. Compressing the files took another 20 minutes.

#### GBAR Restore Operational Details <a id="gbar-restore-operational-details"></a>

To restore from a backup archive, a full archive name needs to be provided, such as _daily-20180607232159_. By default, restore will ask the user to approve to continue. If you want to pre-approve these actions, use the "-y" option. GBAR will make the default choice for you.

```text
$ gbar restore daily-20180607232159
[23:57:06] Retrieve TigerGraph system configuration
GBAR restore needs to reset TigerGraph system.
Do you want to continue?(y/N):y
[23:57:13] Start workgroup
[23:57:22] Pull archive daily-20180607232159, round #1
[23:57:57] Pull archive daily-20180607232159, round #2
[00:01:00] Pull archive daily-20180607232159, round #3
[00:01:00] Unpack cluster data
[00:06:39] Decompress backup data
[00:17:32] Verify checksum
[00:18:30] gadmin stop gpe gse
[00:18:36] Snapshot DICT data
[00:18:36] Restore cluster data
[00:18:36] Restore DICT data
[00:18:36] gadmin reset
[00:19:16] gadmin start
[00:19:41] reinstall GSQL queries
[00:19:42] recompiling loading jobs
[00:20:01] Terminate workgroup
Restore from daily-20180607232159 finished in 22m55s.
Old gstore data saved under /home/tigergraph/tigergraph/gstore with suffix -20180608001836, you need to remove them manually.
```

For our test, GBAR restore took about 23 minutes. Most of the time \(20 minutes\) was spent decompressing the backup archive.

Note that after the restore is done, GBAR informs you were the pre-restore graph data \(gstore\) has been saved. After you have verified that the restore was successful, you may want to delete the old gstore files to free up disk space.

#### Performance Summary of Example <a id="perf-summary-of-example"></a>

| GStore size | Backup file size | Backup time | Restore time |
| :--- | :--- | :--- | :--- |
| 219GB | 49GB | 31 mins | 23 mins |

