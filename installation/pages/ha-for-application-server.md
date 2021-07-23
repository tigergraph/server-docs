# High Availability Support for Application Server

## Introduction

By Design, TigerGraph has built-in HA for all the internal critical components from the beginning. This includes GPE, GSE, REST API Servers, etc. However, the user-facing applications \(GSQL, GraphStudio and Admin Portal\) were designed to be set up by customers based on their High Availability \(HA\) needs. This included building solutions using non-TigerGraph components. With 3.1 release, TigerGraph will support native HA functionality for user-facing applications as well. This simplifies and streamlines HA deployment for users completely. For Operations personnel, this will reduce the operational overhead while enhancing the availability for end users.

## **Overview of the design**

Before we elaborate the design, we need to understand the topology of how TigerGraph services are deployed in a cluster. TigerGraph nodes in a cluster are organized as ‘m1’, ‘m2’, and so on. Application Server \(which serve the APIs for GraphStudio and Admin Portal\) follows the active-active architecture, in which the server is always on m1 and all replicas of m1. This system is a network of independent processing nodes, each having access to a replicated database such that all nodes can provide a similar set of functionalities. With this feature, users can connect to any of the nodes that runs Application Server to get access to GraphStudio and Admin Portal.

![](../../../.gitbook/assets/diagram-draft-1-.svg)

## **User Impacts**

### **When a server dies**

When a server dies, users can proceed to the next available server within the cluster to resume the operations. For example, assuming the TigerGraph cluster has Application Server on m1 and m2. If the server on m1 dies, users can access m2 to use GraphStudio and Admin Portal.

Keep in mind that any long running operation that is currently in process when the server dies will be lost.

### Load Balancing

#### NGINX

One possible choice for setting up load balancing is through the use of NGINX.

Here is an example NGINX configuration for the upstream and server directives:

```text
    upstream flask_pool {
        ip_hash;
        zone flask_pool 64k;
        server 172.31.86.19:14240;
        server 172.31.88.70:14240;
        server 172.31.94.90:14240;

        keepalive 32;
    }

    server {
        listen      8000;
        server_name localhost;

        location / {
                root html;
                index index.html index.htm;
                proxy_pass http://flask_pool;
                proxy_read_timeout 3600;
                proxy_set_header Connection "";
                proxy_http_version 1.1;
                chunked_transfer_encoding off;
                proxy_buffering off;
                proxy_cache off;
        }
        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
                root html;
        }
    }
```

The server directives should specify your nodes' addresses which you want to load balance. Since TigerGraph requires session persistence, the load balancing methods will be limited to _ip\_hash_ or _hash_, unless you have access to NGINX Plus, which then means any load balancing method may be used with session persistence setup: [https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/\#sticky](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/#sticky)

An active health check can be set on the following endpoint if using NGINX Plus:

`/api/ping`

Otherwise, only a passive health check is available. See NGINX documentation for more information: [https://docs.nginx.com/nginx/admin-guide/load-balancer/http-health-check/](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-health-check/)

### AWS Elastic Load Balancing

Another choice for load balancing is through the use of an Application Load Balancer with AWS: [https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-application-load-balancer.html)

In addition to the outlined AWS step 1 to step 6 on the following page: [https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-application-load-balancer.html](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-application-load-balancer.html)

You should also use the following details in step 3, 4, 5:

Step 3: When creating or using an existing security group, make sure it allows requests from the load balancer to port 14240 of the instances in the target group. You can see AWS's recommended rules here: [https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-update-security-groups.html](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-update-security-groups.html)

Step 4: Set the health check URL to `/api/ping`

Step 5: Enter 14240 for the port of your instances.

After following the steps and creating your load balancer, we need to enable sticky sessions in your target group: [https://docs.aws.amazon.com/elasticloadbalancing/latest/application/sticky-sessions.html](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/sticky-sessions.html)

After successfully creating your load balancer, you should now be able to access GraphStudio through the load balancer's DNS name. The DNS name can be found under the "Description" tab of your load balancer in the Amazon EC2 console.







