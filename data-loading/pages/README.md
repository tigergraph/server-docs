# Data Loader User Guides

Data Loaders are interfaces built in to the TigerGraph system which enable users to use the same high-level GSQL protocol  for high-speed parallel data loading, whether the data reside directly on the network file system, or come from one of several other supported data sources. When the data are coming from another data source, some  initial configuration is needed. Then you can use the same type of loading jobs described in the [GSQL Language Reference: Part 1 - Data Definition and Loading](../gsql-ref/ddl-and-loading/).

To configure a data source, see the appropriate data loader user guide:

* [**AWS S3** Loader User Guide](s3-loader-user-guide.md)
* [**Kafka** Loader User Guide](kafka-loader-user-guide.md)
* [**Spark** Connection Via JDBC Driver](spark-connection-via-jdbc-driver.md)



