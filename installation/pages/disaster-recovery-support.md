# Disaster Recovery Support

## **Overview**

TigerGraph architecture is built with no Single Point of Failure \(SPOF\). This provides fault tolerance built at each component level. Any component or server failure is handled seamlessly by TigerGraph's Continuous Availability. 

However, there are situations where the failures span the entire cluster due to loss of data center or any other catastrophic event, Continuous Availability will not be sufficient. Typically, such an event would be defined as a Disaster. Customers would need a disaster recovery \(DR\) plan to get services back up in the event of a disaster. 

Cross-Region Replication \(CRR\) is a new feature that will allow users to keep two or more TigerGraph clusters in different data centers or regions in sync. 

For customers, cross-region replication will help deliver on the following business goals:

* **Disaster Recovery**: Support Disaster Recovery functionality with the use of a dedicated remote cluster 
* **Enhanced Availability**: Enhance Inter-cluster data availability by synchronizing data using Read Replicas across two clusters
* **Enhanced Performance**: If the customer application is spread over different regions, CRR can take advantage of data locality to avoid network latency.
* **Improved System Load-balancing**: CRR allows you to distribute computation load evenly across two clusters if the same data sets are accessed in both clusters.
* **Data Residency Compliance**: Cross-Region replication allows you to replicate data between different data centers or Regions to satisfy compliance requirements. Additionally, this feature can be used to set up clusters in the same region to satisfy more stringent Data sovereignty or localization business requirements.

Besides Disaster recovery and enhanced business continuity, this will enable forward-thinking customers to set up the clusters as part of Blue/Green deployment purposes for agile upgrades.

## **Design**

Disaster Recovery support will include complete native support for all Data and Metadata replication including Automated schema changes, User management, and Query management.

Cross-region replication will be delivered in two phases:

* **Phase1**: Cross-region replication support for data from Primary to DR cluster. Metadata operations will not be supported. Phase 1 will be delivered in TigerGraph 3.1.
* **Phase2**: Complete native support for all Data and Metadata replication including Automated schema changes, User and Query management. Phase 2 will be delivered in TigerGraph 3.2.

![](https://lh5.googleusercontent.com/rfYwJYgfd2jHPJoBSgGy_ZoPc7DGnbE5VxHlBTaRFuAz2yFxPTzCF1kmha9VCuq2ZQQw5PZcFF6l07hJ-Oc1Nb2RN0j3ZtOjcGVwaCB07U63VAMCqWROG98iJE0KovUg5-_PTx2L)

## **User Impact and Changes**

To support cross-region replication, primary and standby clusters need to have the same number of partitions. However, the clusters can have different numbers of replicas. Also, the clusters can be in the same region or data center.

The following setup is needed in order to perform a failover in the event of a disaster:

### **Primary cluster setup**

There are no configuration changes required for the primary cluster. This feature is designed not to impact the primary cluster operations in any way. However, the primary cluster should be running on TigerGraph Version 3.1.

### **DR cluster setup**

The remote cluster needs to be set up to be used as a Disaster Recovery cluster. The following configurations should be set up by the operations team to enable the synchronization of data between primary and remote clusters. 

```text
gadmin config set System.CrossRegionReplication.Enabled true
gadmin config set System.CrossRegionReplication.PrimaryKafkaIPs <primary_ips> // IP lists, comma separated
gadmin config set System.CrossRegionReplication.PrimaryKafkaPort <kafka_port>
gadmin config set System.CrossRegionReplication.GpeTopicPrefix Primary
gadmin config apply -y
gadmin init kafka -y
gadmin restart -y
```

### **Metadata Operations**

All the data loaded in the Primary cluster will be copied and loaded into the DR cluster automatically. In TigerGraph 3.1, users will also have to manually perform all the metadata operations. The Metadata operations include Schema change, Installation of new queries, and User Management operations.

With respect to Schema change, users will have to perform all the Schema change operations on the DR cluster in the same order after successfully applying schema change in the primary cluster. Without applying the corresponding schema change in the DR clusters, data updates will pause in the DR clusters. Or if wrong schema change \(or wrong order\) is performed in the DR cluster, there will be data inconsistency issues resulting in loss of cluster services.

### **Failover**

In the event of catastrophic failure that has impacted the full cluster due to Data Center or Region failure, the customer can initiate the failover to the DR cluster. This is a manual process. Users will have to make the following configuration changes to upgrade the DR cluster to become the primary cluster.

```text
gadmin config set System.CrossRegionReplication.Enabled false
gadmin config set System.CrossRegionReplication.PrimaryKafkaIPs 
gadmin config set System.CrossRegionReplication.PrimaryKafkaPort
gadmin config set System.CrossRegionReplication.GpeTopicPrefix Primary 
gadmin config apply -y
gadmin restart -y
```

If we want to set up a new DR cluster over the upgraded primary cluster:

```text
gadmin config set System.CrossRegionReplication.Enabled true
gadmin config set System.CrossRegionReplication.PrimaryKafkaIPs <primary_ips> // IP lists, comma separated
gadmin config set System.CrossRegionReplication.PrimaryKafkaPort <kafka_port>
gadmin config set System.CrossRegionReplication.GpeTopicPrefix Primary.Primary // Yes P.P
gadmin config apply -y
gadmin init kafka -y
gadmin restart -y
```

There is no limit on the number of times a cluster can failover to another cluster. When designating a new DR cluster, make sure that you set the `System.CrossRegionReplication.GpeTopicPrefix` parameter correctly by adding an additional `.Primary` . For example, if your original cluster fails over once, and the current cluster's `GpeTopicPrefix` is `Primary`, then the new DR cluster needs to have its `GpeTopicPrefix` be `Primary.Primary`. If it needs to fail over again, the new DR cluster needs to have its `GpeTopicPrefix` be set to `Primary.Primary.Primary`. 



