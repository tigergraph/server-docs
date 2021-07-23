# Built-in Endpoints

## System Utilities

### Echo

`GET /echo` and `POST /echo`

These endpoints are simple diagnostic utilities, which respond with the following message if the RESTPP server is up and running.

#### Sample request:

{% tabs %}
{% tab title="GET echo/ Request and Response" %}
```bash
curl -X GET "http://localhost:9000/echo"
{
    "error": false, 
    "message": "Hello GSQL"
}
```
{% endtab %}
{% endtabs %}

`POST /echo` has the same response as `GET /echo`.

#### Parameters

| Name | Required | Description |
| :--- | :--- | :--- |
| `sleep` | No | Integer that indicates the number of seconds for which the response will be delayed.   |

### Health check \(public\)

This endpoint performs a simple server health check. It listens on port 14240 and does not require authentication. If you ping it and the server is running, it will respond with the message "pong".

#### Endpoint:

`GET /api/ping`

#### Sample request:

```text
$ curl 'http://localhost:14240/api/ping'
​
{
  "error": "false",
  "message": "pong",
  "results": {}
}
```

#### Parameters:

No parameters.

### List all endpoints 

`GET /endpoints/{graph_name}`

This endpoint returns a list of the installed endpoints and their parameters. There are three types of endpoints:

* _Built-in endpoints_ which are preinstalled in the TigerGraph system
* _Dynamic endpoints_ which are generated when compiling GSQL queries
* _Static endpoints_ which are user-installed endpoints

To include one or more of the endpoint types in the output, include the endpoint type in the parameter query string and set its value to `true`. If no type parameters are provided, all endpoints are returned.

{% tabs %}
{% tab title="Example: Report on all built-in endpoints" %}
```bash
curl -X GET "http://localhost:9000/endpoints?builtin=true" | jq .
```
{% endtab %}
{% endtabs %}

#### Response

There are over a dozen built-in endpoints, and some have several parameters, so the formatted JSON output of all built-in endpoints is over 300 lines long. It is listed in full in Appendix A. Below is a small excerpt of the output:

{% tabs %}
{% tab title="Subset of GET /endpoints output" %}
```bash
    "GET /echo": null,
    "GET /endpoints": {
        "parameters": {
            "builtin": {
                "default": "false", 
                "max_count": 1, 
                "min_count": 0, 
                "type": "BOOL"
            }, 
            "dynamic": {
                "default": "false", 
                "max_count": 1, 
                "min_count": 0, 
                "type": "BOOL"
            }, 
            "static": {
                "default": "false", 
                "max_count": 1, 
                "min_count": 0, 
                "type": "BOOL"
            }
        }
    }
```
{% endtab %}
{% endtabs %}

#### Parameters

| Name | Required | Description |
| :--- | :--- | :--- |
| `builtin` | No | Takes a boolean value. Returns built-in endpoints if true. |
| `dynamic` | No | Takes a boolean value. Returns dynamic endpoints if true. |
| `static` | No | Takes a boolean value. Returns user-installed endpoints if true. |

### Show component versions

`GET /version`

This endpoint returns the GIT versions of all components of the system. 

#### Sample request:

```bash
curl -X GET "http://localhost:9000/version"
{"error":"false", "message":"TigerGraph RESTPP: 
 --- Version --- 
product              release_2.6.0_05-09-2020 ab1e3d0da6237c27468d6cabb90900119d63759d  2020-04-15 15:46:29 -0700
olgp                 release_2.6.0_05-09-2020 046c745088106b69920b9bdb3bd15969de409e92  2020-05-01 19:10:27 -0700
topology             release_2.6.0_05-09-2020 c028af100117f2051b619436c3aa4febc810bf36  2020-04-22 08:44:07 -0700
gpe                  release_2.6.0_05-09-2020 34b9e86ef7b5fdaa106637e7db1d8a9e080a0aa2  2020-04-19 09:42:59 -0700
gse                  release_2.6.0_05-09-2020 ed2c2351357aa9077fa4dee7ea7a01f8ad2f7585  2020-05-11 01:18:54 -0700
third_party          release_2.6.0_05-09-2020 4bce6990bae5be2b91e9201693ceb66341d3f204  2020-04-19 09:42:56 -0700
utility              release_2.6.0_05-09-2020 2ce197d3edb3557bdd66ed1a4194309908d6197e  2020-04-20 21:19:34 -0700
realtime             release_2.6.0_05-09-2020 52a82b454437c73b47d846acd5803ab0d9f54a45  2020-04-22 08:44:11 -0700
er                   release_2.6.0_05-09-2020 a3e6cb7606fb74984c75cae9bbd4d2112fdbf73a  2020-05-01 19:10:33 -0700
gle                  release_2.6.0_05-09-2020 d8bdbd1cf346e181aa9a317c704dd7b3b11b4658  2020-05-06 00:51:04 -0700
bigtest              release_2.6.0_05-09-2020 2f64c47b7a5ac1834ead9a22eef8d42241117853  2019-12-12 01:31:35 -0800
document             release_2.6.0_05-09-2020 6327094bd76b2dbc8f4625108d547827344b5091  2019-12-13 16:30:13 -0800
glive                release_2.6.0_05-09-2020 93f61ea06fe42759c808fc58ff6245c9954d5447  2020-02-05 22:40:24 -0800
gap                  release_2.6.0_05-09-2020 e798efb595545bf91c449034566857c41f52449a  2020-04-29 22:47:26 -0700
gst                  release_2.6.0_05-09-2020 1b695c02f277efad0ddfb2deab710ae0158409da  2020-04-29 22:47:32 -0700
gus                  release_2.6.0_05-09-2020 eee784502b5387844e462305bae419954784da6f  2020-04-29 22:47:20 -0700
blue_features        release_2.6.0_05-09-2020 5d7a4e8d806519f529274b331496d3bc78f01990  2020-04-15 15:46:38 -0700
blue_commons         release_2.6.0_05-09-2020 432763afc49bf986aed4731e50254243d3665bc3  2019-07-30 03:34:46 -0700
"}
```

#### Parameters

This endpoint does not take any parameters.

### Monitor system metrics

`POST /ts3/api/datapoints`

TigerGraph System State Service \(TS3\) is TigerGraph's managed monitoring service that collects system metrics and events. Many TigerGraph components will report metrics such as CPU usage, memory usage, disk usage, and network traffic to TS3 at regular intervals. You can use this endpoint to read from TS3,  filtering for the data points you need by time \(`when`, `from`, and `to`\), component\(`who`\), metric\(`what`\) and location\(`where`\). Visualization of such metrics are available in Admin Portal - Dashboard - [Cluster Monitoring](../../ui/admin-portal/dashboard.md#TigerGraphAdminPortalUIGuide-Charts). 

On a TigerGraph cluster, this endpoint is only present on the `m1` node. 

#### Parameters

<table>
  <thead>
    <tr>
      <th style="text-align:left">Name</th>
      <th style="text-align:left">Required</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left"><code>from</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">Epoch timestamp that indicates the start of the time filter. Only data
        points reported after the timestamp will be included in the return results.</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>to</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">Epoch timestamp that indicates the end of the time filter. Only data points
        reported before the timestamp will be included in the return results.</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>latest</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">Number of latest data points to return. If provided, the endpoint will
        return the latest data points that satisfy the <code>what</code>, <code>who</code> and <code>where</code> filters
        and ignore other time-related filters.</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>what</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">
        <p>Name of the metric to filter for. Possible values are:</p>
        <ul>
          <li><code>cpu</code>: Percentage of CPU usage by component</li>
          <li><code>mem</code>: Memory usage in megabytes by component</li>
          <li><code>diskspace</code>: Disk usage in megabytes by directory</li>
          <li><code>network</code>: Network traffic in bytes since the service started</li>
          <li><code>qps</code>: Number of requests per second by endpoint</li>
          <li><code>servicestate</code>: Whether or not the service is online. A value
            of <code>0</code> indicates that the service is offline while a value of <code>1</code> means
            the service is online</li>
          <li><code>connection</code>: Number of open TCP connections</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>who</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">Name of the component that reported the datapoint</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>where</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">Name of the node that the datapoint is reported for</td>
    </tr>
  </tbody>
</table>

#### Sample requests

In the sample request below, the filters in the query string include a timeframe starting at `1618957536` and ending at `1619023346`, and specifying that the response should only include CPU information:  

```bash
$ curl -X GET 
"https://crunch.i.tgcloud.io:14240/ts3/api/datapoints?from=1618957536&to=1619023346&what=cpu"

# Three data points returned
[
  {
    "detail": 0,  # GPE is using 0 percent CPU 
    "when": 1619023346, 
    "where": "m1", 
    "who": "GPE_1#1",
    "what": "cpu"
  },
  {
    "detail": 0,
    "when": 1619023346,
    "where": "m1",
    "who": "GSE_1#1",
    "what": "cpu"
  },
  {
    "detail": 0,
    "when": 1619023346,
    "where": "m1",
    "who": "RESTPP#1",
    "what": "cpu"
  }
]

```

In the below example, the request asks for the 10 latest data points regarding memory usage:

```bash
$ curl -X GET
"https://crunch.i.tgcloud.io:14240/ts3/api/datapoints?what=mem&latest=10"

[
  {
    "detail": 159,
    "when": 1620076473,
    "where": "m1",
    "who": "RESTPP#1",
    "what": "mem"
  },
  {
    "detail": 211,
    "when": 1620076533,
    "where": "m1",
    "who": "GPE_1#1",
    "what": "mem"
  },
  {
    "detail": 436,
    "when": 1620076533,
    "where": "m1",
    "who": "GSE_1#1",
    "what": "mem"
  },
  {
    "detail": 159,
    "when": 1620076533,
    "where": "m1",
    "who": "RESTPP#1",
    "what": "mem"
  },
  {
    "detail": 211,
    "when": 1620076593,
    "where": "m1",
    "who": "GPE_1#1",
    "what": "mem"
  },
  {
    "detail": 436,
    "when": 1620076593,
    "where": "m1",
    "who": "GSE_1#1",
    "what": "mem"
  },
  {
    "detail": 159,
    "when": 1620076593,
    "where": "m1",
    "who": "RESTPP#1",
    "what": "mem"
  },
  {
    "detail": 210,
    "when": 1620076653,
    "where": "m1",
    "who": "GPE_1#1",
    "what": "mem"
  },
  {
    "detail": 436,
    "when": 1620076653,
    "where": "m1",
    "who": "GSE_1#1",
    "what": "mem"
  },
  {
    "detail": 159,
    "when": 1620076653,
    "where": "m1",
    "who": "RESTPP#1",
    "what": "mem"
  }
]
```

### Show query performance

`GET /statistics/{graph_name}`

This endpoint returns real-time query performance statistics over the given time period, as specified by the `seconds` ****parameter. The `seconds` parameter must be a positive integer less than or equal to 60. 

#### Sample request:

The return object is a hash of the endpoints and their performance data:

```bash
# The example shows two endpoints (/graph/vertex and
# /statistics) called during the past 60 seconds.
curl -X GET "http://localhost:9000/statistics/poc_graph?seconds=60" | jq '.'

{
  "GET /graph/vertices/{vertex_type}/{vertex_id}": {
    "CompletedRequests": 8,
    "QPS": 0.08,
    "TimeoutRequests": 0,
    "AverageLatency": 130,
    "MaxLatency": 133,
    "MinLatency": 128,
    "LatencyPercentile": [
      200,
      200,
      200,
      200,
      200,
      200,
      200,
      200,
      200,
      200
    ]
  },
  "GET /statistics": {
    "CompletedRequests": 4226,
    "QPS": 42.26,
    "TimeoutRequests": 0,
    "AverageLatency": 2,
    "MaxLatency": 125,
    "MinLatency": 0,
    "LatencyPercentile": [
      10,
      10,
      10,
      10,
      10,
      10,
      10,
      10,
      10,
      200
    ]
  }
}
```

Each endpoint has the following attributes:

* `CompletedRequests` - the number of completed requests.
* `QPS` - query per second.
* `TimeoutRequests` - the number of requests not returning before the system-configured timeout limit. Timeout requests are not included in the calculation of QPS.
* `AverageLatency` - the average latency of completed requests.
* `MaxLatency` - the maximum latency of completed requests.
* `MinLatency` - the minimum latency of completed requests.
* `LatencyPercentile` - The latency distribution. The number of elements in this array depends on the `segments` ****parameter of this endpoint whose default value is 10, meaning the percentile range 0-100% will be divided into ten equal segments: 0%-10%, 11%-20%, etc.`Segments` ****must be \[1, 100\].

If there is no query sent in the past given seconds, an empty json will be returned.

#### Parameters

| Name | Required | Description |
| :--- | :--- | :--- |
| `seconds` | Yes | Positive integer less than 60 that indicates how many seconds back from the current time the statistics report will cover.  |
| `segments` | No | Integer that indicates the number of segments that `LatencyPercentile` array in the response will be split into. The value for this endpoint must be between 1 and 100 and has a default value of 10.  |

### Rebuild graph engine 

`GET /rebuildnow/{graph_name}` or `POST /rebuildnow/{graph_name}`

In TigerGraph, when new data is being loaded into the graph \(such as new vertices or edges\), data is first stored in memory before it is saved to disk permanently. TigerGraph runs a rebuild of the Graph Processing Engine \(GPE\) to commit the data in memory to disk every 30 seconds, but you can also call this endpoint to trigger a rebuild immediately. 

#### Parameters:

<table>
  <thead>
    <tr>
      <th style="text-align:left">Name</th>
      <th style="text-align:left">Required</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left"><code>threadnum</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">
        <p>Number of threads used to execute the rebuild. If not specified, the number
          specified in line 185 of the <code>.tg.cfg</code> file (<code>&quot;RebuildThreadNumber&quot;</code>)
          in the home directory of the server on which TigerGraph is running will
          be used; it is set to 3 by default.</p>
        <p></p>
        <p>The maximum value for this parameter is the number of vCPUs per node in
          your distributed system. If you are running a single-node server, the maximum
          is the number of vCPUs on that node. You can run <code>lscpu</code> in the
          command line of your Linux server and look in the <code>CPU(s)</code> column
          to view the number of vCPUs.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>vertextype</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">Vertex type to perform the rebuild for. If not provided, the rebuild will
        be run for all the vertex types.</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>segid</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">Segment ID of the segments to rebuild. If not provided, all segments will
        be rebuilt. In general, it is recommended not to provide this parameter
        and rebuild all segments.</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>path</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">Path to save the summary of the rebuild to. If not provided, the default
        path is <code>/tmp/rebuildnow</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>force</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">Boolean value that indicates whether to perform rebuilds for segments
        for which there are no records of new data. Normally, a rebuild would skip
        such segments, but if <code>force</code> is set true, the segments will not
        be skipped.</td>
    </tr>
  </tbody>
</table>

#### Example:

```bash
$ curl -X GET 'http://localhost:9000/rebuildnow/social' 

# JSON response
{
  "version": {
    "edition": "enterprise",
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "RebuildNow finished, please check details in the folder: /tmp/rebuildnow",
  "results": [],
  "code": "REST-0000"
}

# Example summary file
$ cat finished.summary.txt

[SELECTED]	Segment id: 106, vertextype: 0, vertexsubtypeid: 0, vertexcount: 187732, edgecount: 563196, deletevertexcount: 0, postqueue_pos: 16344, transaction id: 16344, rebuild ts: 1573106412990
[SKIPPED]	Segment id: 6, vertextype: 0, vertexsubtypeid: 0, vertexcount: 85732, edgecount: 3106, deletevertexcount: 0, postqueue_pos: 16344, transaction id: 16344, rebuild ts: 1573106412900

```

### Check deleted vertices

~~`GET /deleted_vertex_check`~~

In certain rare cases, TigerGraph's Graph Processing Engine \(GPE\) and Graph Storage Engine \(GSE\) might be out of sync on vertex deletion information. When this happens, some vertices might exist on one of the components, but not the other. Even though these errors are exceedingly rare, TigerGraph provides an endpoint that allows you to check the deleted vertices on GSE and GPE and see if they out of sync. 

The check passes if there are no discrepancies between the GSE and GPE in terms of deleted vertices. If there is a discrepancy, the check fails and the return result will contain the IDs of the deleted vertices that are not synced properly. If you are running TigerGraph on a distributed cluster, the check will be performed on each node of the cluster, and the endpoint will return a list containing the results of the check for every node. 

#### Parameters:

<table>
  <thead>
    <tr>
      <th style="text-align:left">Name</th>
      <th style="text-align:left">Required</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left"><code>threadnum</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">Integer that indicates the number of threads used to execute the deleted
        vertex check jobs. This parameter is optional and the default value is
        6 if none is provided</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>segid</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">IDs of segments to perform the deleted vertex check for. If none is provided,
        the check will be performed on all segments.</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>vertextype</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">Vertex types to perform the deleted vertex check for. If none is provided,
        the check will be performed on all vertex types.</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>verbose</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">
        <p>Integer that indicates the level of detail in the return results. Here
          is a list of accepted values and their corresponding level of detail:</p>
        <ul>
          <li><code>0</code> (default) : Only return whether the check passed and the
            list of unsynced vertex IDs</li>
          <li><code>1</code>: In addition to the previous level, also return vertex
            count information</li>
          <li><code>2</code>: In addition to the previous level, return vertex count
            information for every segment</li>
          <li><code>4</code>: In addition to the previous level, also return the IDs
            of deleted vertices for every segment</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>log</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">
        <p>Integer that indicates the log level of the deleted vertex check. This
          log is not returned in the endpoint&apos;s HTTP response, but is printed
          to the logs of the GPE component at <code>/tigergraph/log/gpe/log.INFO</code>:</p>
        <ul>
          <li><code>0</code> (default): Report brief log for the check as a whole</li>
          <li><code>1</code>: Report logs for each segment</li>
          <li><code>2</code>: Report additional logs on the obtained deleted ID list</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

#### Example:

```bash
# Passing check performed on a single-node database
$ curl -X GET "http://localhost:9000/deleted_vertex_check?threadnum=10&verbose=0" |jq .
 
{
  "version": {
    "edition": "enterprise",
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "check passed",
  "results": [
    {
      "GPE": "GPE_1_1",
      "PassCheck": true,
      "UnSyncList": []
    }
  ],
  "code": "REST-0000"
}

# Failed check performed on a distributed cluster

$ curl -X GET 'http://localhost:9000/deleted_vertex_check?threadnum=10&verbose=0&vertextype=region' |jq .
{                                                                                                   
  "version": {                                                                                      
    "edition": "enterprise",                                                                        
    "api": "v2",                                                                                    
    "schema": 0                                                                                     
  },                                                                                                
  "error": false,                                                                                   
  "message": "check failed",                                                                        
  "results": [                                                                                      
    {                                                                                               
      "GPE": "GPE_2_1",                                                                             
      "PassCheck": false,                                                                           
      "UnSyncList": [                                                                               
        {                                                                                           
          "Segid": 193,                                                                             
          "IsRemote": false,                                                                        
          "VertexType": "region",                                                                   
          "GPEDelHash": 7013042118817697000,                                                        
          "IDSDelHash": 202375168                                                                   
        }                                                                                           
      ]                                                                                             
    },                                                                                              
    {                                                                                               
      "GPE": "GPE_3_1",                                                                             
      "PassCheck": false,                                                                           
      "UnSyncList": [                                                                               
        {                                                                                           
          "Segid": 193,                                                                             
          "IsRemote": true,                                                                         
          "VertexType": "region",                                                                   
          "GPEDelHash": 7013042118817697000,                                                        
          "IDSDelHash": 202375168                                                                   
        }                                                                                           
      ]                                                                                             
    },                                                                                              
    {                                                                                               
      "GPE": "GPE_1_1",                                                                             
      "PassCheck": false,                                                                           
      "UnSyncList": [                                                                               
        {                                                                                           
          "Segid": 193,                                                                             
          "IsRemote": true,           
          "VertexType": "region",                                                                   
          "GPEDelHash": 7013042118817697000,                                                        
          "IDSDelHash": 202375168                                                                   
        }                                                                                           
      ]                                                                                             
    }                                                                                               
  ],                                                                                                
  "code": "REST-0000"                                                                               
}      
```

## Authentication

The endpoints in this subsection allow users to create, refresh and delete authentication tokens for requests made to the REST++ server. **These endpoints only exist when** [**user authentication is enabled**](../../admin/admin-guide/user-access/user-privileges-and-authentication.md#rest-authentication) **on RESTPP endpoints.** 

### Request a token \(`GET`\)

`GET /requesttoken`

If authentication is enabled on RESTPP endpoints, a token needs to be included in the request header for all requests sent to the RESTPP server. A user can generate a token using either

*  A secret, which is a random string generated in GSQL \(see[ Managing User Privileges and Authentication](../../admin/admin-guide/user-access/user-privileges-and-authentication.md)\)
* Their username and password in their request header as well as specifying the graph \(Available only in V3.1.4 and later. 

#### Sample request:

```bash
curl -X GET "http://localhost:9000/requesttoken?secret=jiokmfqqfu2f95qs6ug85o89rpkneib3&lifetime=1000000"
{
  "code": "REST-0000",
  "expiration": 1616042814,
  "error": false,
  "message": "Generate new token successfully.",
  "token": "tohvf6khjqju8jf0r0l1cohhlm8gi5fq"
}

curl --user tigergraph:tigergraph -X GET "localhost:9000/requesttoken?graph=<GRAPH_NAME>"
```

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `secret` | Yes \(No for 3.1.4 and later\) | User's secret used to generate the token. |
| `lifetime` | No | Period of time for which the token is valid measured in seconds. The default value is about 2.6 million \(about a month\). |
| `graph` | No | Name of the graph that the token wil be valid for. |

### Request a token \(`POST`\)

`POST /requesttoken`

You may also use a `POST` request to generate your token. This allows you to avoid exposing your secret in the query string. 

#### Sample request:

```bash
curl -d <path_to_secret> -X POST \
"http://localhost:9000/requesttoken?lifetime=1000000"
{
  "code": "REST-0000",
  "expiration": 0,
  "error": false,
  "message": "Refresh token successfully.",
  "token": "tohvf6khjqju8jf0r0l1cohhlm8gi5fq"
}
```

Replace `path_to_secret` with the path to the file containing your secret. The file should only include a single line, which is your secret. 

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `lifetime` | No | Period of time for which the token is valid measured in seconds. The default value is about 2.6 million \(about a month\). |

### Refresh a token

`PUT /requesttoken`

This endpoint takes a token and its associated secret and refreshes the lifetime of the token. The token itself remains unchanged.

**Parameters:**

| **Name** | Required | Description |
| :--- | :--- | :--- |
| `token` | Yes | Token to refresh. |
| `secret` | Yes | User's secret used to generate the token. |
| `lifetime` | Yes | Period of time for which the token is valid measured in seconds. |

#### Sample request

```bash
curl -X PUT "http://localhost:9000/requesttoken?lifetime=15&secret=ksdoilrvpl0r0tef3d4abbpgu0t2u5la&token=0mq98l9pderkaivndf820gudg923p3l0"|jq .
{
  "code": "REST-0000",
  "expiration": 15,
  "error": false,
  "message": "Refresh token successfully.",
  "token": "0mq98l9pderkaivndf820gudg923p3l0"
}
```

{% hint style="warning" %}
**Known bug**: The output shows the lifetime instead of the expiration time.
{% endhint %}

### Delete a token

`DELETE /requesttoken`

This endpoint takes a token and its associated secret, and deletes the token.

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `token` | Yes | Token to delete. |
| `secret` | Yes | User's secret used to generate the token. |

## Loading jobs

### Run a Loading Job

`POST /ddl/{graph_name}`

This endpoint is for loading data into a graph. It submits data as an HTTP request payload, to be loaded into the graph by the DDL Loader. The data payload can be formatted as generic CSV or JSON. For more details, please see[ GSQL Language Reference Part 1 - Defining Graphs and Loading Data](../gsql-ref/ddl-and-loading/). 

If the loading job references multiple files, multiple HTTP requests are needed to complete the loading job since you can only provide data for one filename varibale at a time. The loading job will skip the `LOAD` statements referencing filename variables that the request didn't provide data for.  To provide data for a filename variable, put the data in the request body and use the `filename` parameter \(explained in the parameter table below\) to match the variable name defined in the loading job. 

If a `LOAD` statement is written using a filepath string instead of a file variable, even though the filepath is already provided in the loading job, you still need to provide data in the request body for the `LOAD` statement to run. Since there isn't a file variable in this case, use a [position-based file identifier](../gsql-ref/ddl-and-loading/creating-a-loading-job.md#position-based-file-identifier) to identify the filepath string you are providing data for in the `filename` parameter. 

#### Request body:

The request body is the data to be loaded \(either in CSV or JSON format\).

Curl allows you to read the data from an input file by using the @ symbol:

`curl -X POST --data-binary @./company.csv "http://…"`

#### Sample request:

In this example, the loading job is dependent on three filename variables \(`f1` and `f3`\) and one filepath string. Therefore, three HTTP requests are needed to complete the loading job. 

```bash
# Loading job
CREATE LOADING JOB load_data for GRAPH poc_graph {

    DEFINE FILENAME f1;
    DEFINE FILENAME f3;
    
    LOAD f1 to VERTEX person VALUES ($0, $0);
    LOAD "/home/data/company.csv" to VERTEX company VALUES ($0, $0);

    LOAD f3 to EDGE work_at VALUES ($0, $1, $3, $4, $5);
}

# Provide data for for the second LOAD statement 
curl -X POST --data-binary @./another_company.csv \
"http://localhost:9000/ddl/poc_graph?tag=load_data&filename=__GSQL_FILENAME_0__" | jq 

{
  "version": {
    "edition": "enterprise",
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "sourceFileName": "Online_POST",
      "statistics": {
        "validLine": 7927,
        "rejectLine": 0,
        "failedConditionLine": 0,
        "notEnoughToken": 0,
        "invalidJson": 0,
        "oversizeToken": 0,
        "vertex": [
          {
            "typeName": "company",
            "validObject": 7,
            "noIdFound": 0,
            "invalidAttribute": 0,
            "invalidPrimaryId": 0,
            "invalidSecondaryId": 0,
            "incorrectFixedBinaryLength": 0
          }
        ],
        "edge": [],
        "deleteVertex": [],
        "deleteEdge": []
      }
    }
  ],
  "code": "REST-0000"
}

# Provide data for filename f1 for the first LOAD statement
curl -X POST --data-binary @./person.csv \
"http://localhost:9000/ddl/poc_graph?tag=load_data&filename=f1"

# Provide data for filename f3 for the third LOAD statement
curl -X POST --data-binary @./work_at.csv \
"http://localhost:9000/ddl/poc_graph?tag=load_data&filename=f3"
```

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `tag` | Yes | Loading job name defined in your DDL loading job |
| `filename` | Yes | File variable name or file path for the file containing the data  |
| `sep` | No | Separator of CSV data. If your data is JSON, you do not need to specify this parameter. The default separator is a comma`","` |
| `eol` | No | End-of-line character. Only one or two characters are allowed, except for the special case "\r\n". The default value is `"\n"` |
| `ack` | No | `"all"`: request will return after all GPE instances have acknowledged the `POST` request. `"none"`: request will return immediately after RESTPP processed the `POST` request. |
| `timeout` | No | Timeout in seconds. If set to 0, use system-wide endpoint timeout setting. |
| `concise` | No | Boolean value that indicates whether to return concise results of the data loading request. Concise results will only include the number of vertices and edges added or deleted, and will omit information such as the number of valid and invalid lines in the default response.  |

If there are special characters in your parameter values, the special characters should use [URL encoding](https://www.w3schools.com/tags/ref_urlencode.asp). To avoid confusion about whether you should you one or two backslashes, we do not support backslash escapes for the `eol` or `sep` parameter.

The maximum size of data you can upload via this endpoint is controlled by the [`Nginx.ClientMaxBodySize`](intro.md#request-body-size) configuration parameter \(default is 128 MB\).

## Graphs

### Run built-in functions on graph

`POST /builtins/{graph_name}`

This endpoint runs a set of built-in functions and returns relevant statistics about a graph. 

#### Request body:

This endpoint expects a data payload in the request body that specifies which function to run on the graph. Depending on the function being run, different fields may also be expected in the request body.

Here is a list of functions supported by this endpoint and their corresponding data payload format.

* `stat_vertex_attr`
  * Returns the minimum, maximum, and average values of the given vertex type's `int`, `uint`, `float` and `double` attributes, and the count of `true` and `false` of a boolean attribute.
  * Data payload fields:
    * `"function": "stat_vertex_attr"` - specifies that the function to run is`stat_vertex_attr`
    * `"type"` - the vertex type whose attribute values to report on. Required field. It also accepts the value `"*"` \(wild card\), in which case, all vertex types are included
* `stat_edge_attr`
  * Returns the minimum, maximum, and average values of the given edge type's `int`, `uint`, `float` and `double` attributes, and the count of `true` and `false` of a boolean attribute.
  * Data payload fields:
    * `"function": stat_edge_attr`
    * `"type"`
    * `"from_type"` - the source vertex type of the edges to report on
    * `"to_type"` - the target vertex type of the edges to report on
* `stat_vertex_number`
  * Returns the number of vertices of the given vertex type. 
  * Data payload fields:
    * `"function":  "stat_vertex_number"`
    * `"type"` - the vertex type of the vertices to count
* `state_edge_number`
  * Returns the number of edges of the given edge type
  * Data payload fields:
    * `"function": "stat_edge_number"`
    * `"type"` - the edge type of the edges to count
    * `"from_type"` - the source vertex type of the edges to report on
    * `"to_type"` - the target vertex type of the edges to report on

#### Sample requests:

Below is an example request running `stat_vertex_attr` on `socialNet` and its output. The vertex type `"Person"` has a `uint` attribute `"age"`.

```bash
curl -X POST "http://localhost:9000/builtins/socialNet" \
-d  '{"function":"stat_vertex_attr","type":"Person"}' | jq .

{
  "version": {
      "api": "v2",
      "schema": 0
   },
  "error": false,
  "message": "",
  "results": [
    {
      "vertexName": "Person",
      "attributeStat": [
        {
          "vattrName": "age",
          "MAX": 64,
          "MIN": 15,
          "AVG": 36.5
        }
      ]
    }
  ]
}
```

Here is an example request running `stat_edge_attr` on `socialNet` and its output. The edge type `"Liked"` has a float attribute `"strength"`.

```bash
curl -X POST "http://localhost:9000/builtins/socialNet" \
-d  '{"function":"stat_edge_attr","type":"Liked", "from_type":"*", "to_type":"*"}' | jq .

{
  "version": {
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "e_type": "Liked",
      "attributes": {
        "weight": {
          "MAX": 2.5,
          "MIN": 1,
          "AVG": 1.375
        }
      }
    }
  ]
}
```

Here is an example request running `stat_vertex_number` and its output.

```bash
curl -X POST "http://localhost:9000/builtins/socialNet" \
-d  '{"function":"stat_vertex_number","type":"*"}' | jq .

{
  "version": {
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "v_type": "User",
      "count": 4
    },
    {
      "v_type": "Page",
      "count": 4
    },
    {
      "v_type": "Product",
      "count": 7
    },
    {
      "v_type": "DescWord",
      "count": 7
    },
    {
      "v_type": "NameUser",
      "count": 9
    },
    {
      "v_type": "VidUser",
      "count": 4
    },
    {
      "v_type": "Video",
      "count": 5
    },
    {
      "v_type": "AttributeTag",
      "count": 4
    }
  ]
}
```

#### Parameters:

No parameters.

### Show graph schema metadata 

`GET /gsqlserver/gsql/schema` 

Returns schema details about a vertex type, an edge type, or the entire graph schema. This is a GSQL Server request sent to port 14240, and authentication credentials need to be provided.  

#### Sample request:

```bash
$ curl -u tigergraph:tigergraph \
"localhost:14240/gsqlserver/gsql/schema?graph=workNet&type=company"

{
  "error": false,
  "message": "",
  "results": {
    "Config": {
      "STATS": "OUTDEGREE_BY_EDGETYPE",
      "PRIMARY_ID_AS_ATTRIBUTE": false
    },
    "Attributes": [
      {
        "AttributeType": {
          "Name": "STRING"
        },
        "IsPartOfCompositeKey": false,
        "PrimaryIdAsAttribute": false,
        "AttributeName": "id",
        "HasIndex": false,
        "IsPrimaryKey": false
      },
      {
        "AttributeType": {
          "Name": "STRING"
        },
        "IsPartOfCompositeKey": false,
        "PrimaryIdAsAttribute": false,
        "AttributeName": "country",
        "HasIndex": false,
        "IsPrimaryKey": false
      }
    ],
    "PrimaryId": {
      "AttributeType": {
        "Name": "STRING"
      },
      "IsPartOfCompositeKey": false,
      "PrimaryIdAsAttribute": false,
      "AttributeName": "clientId",
      "HasIndex": false,
      "IsPrimaryKey": false
    },
    "Name": "company"
  }
}
```

_**Vertex schema object**_ **fields:**

* **`Name`**: the vertex type name, same as the input parameter "type"
* **`PrimaryId`**: details about the primary id
* **`Attributes`**: details about each attribute, listed in order
* **`Config`**: details about global properties of the vertex type

_**Edge schema object**_ **fields:**

* **`Name`**: the edge type name, same as the input parameter "type"
* **`FromVertexTypeName`**: source vertex type name
* **`ToVertexTypeName`**: target vertex type name
* **`Attributes`**: details about each attribute, listed in order
* **`IsDirected`**: whether the edge is directed 
* **`Config`**: additional details about global properties of the edge type

_**Graph schema object**_ **fields:**

* **`GraphName`**: the graph name, same as the input parameter "graph"
* **`VertexTypes`**: an array of _vertex schema objects_. Each vertex schema object is exactly the JSON output if that specific vertex type had been specified.
* **`EdgeTypes`**: an array of _edge schema objects_. Each edge schema object is exactly the JSON output if that specific edge type had been specified.

```bash
{
  "error": false,
  "message": "",
  "results": {
    "GraphName": "workNet",
    "VertexTypes": [
      {
        "Config": {...},
        "Attributes": [...],
        "PrimaryId": {...},
        "Name": "person"},
      {
        "Config": {...},
        "Attributes": [...],
        "PrimaryId": {...},
        "Name": "company"}
    ],
    "EdgeTypes": [
      {
        "IsDirected": false,
        "ToVertexTypeName": "company",
        "Config": {},
        "Attributes": [...],
        "FromVertexTypeName": "person",
        "Name": "worksFor"
      }
    ]
  }
}
```

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `graph` | Yes | The name of the graph whose schema to retrieve. |
| `type` | No | The vertex or edge type whose details to retrieve. If not provided, the endpoint will provide a _graph schema object_ containing the schema details of the entire graph. |

### Upsert data to graph

`POST /graph/{graph_name}` 

This endpoint upserts vertices and/or edges into a graph. To upsert means that if a vertex or edge does not exist, it is inserted, and if it does exist, it is updated. 

#### Parameters:

<table>
  <thead>
    <tr>
      <th style="text-align:left">Name</th>
      <th style="text-align:left">Required</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left"><code>ack</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">
        <p>The value of this parameter can either be <code>&quot;all&quot;</code> or <code>&quot;none&quot;</code>.</p>
        <p><code>&quot;all&quot;</code>: request will return after all GPE instances
          have acknowledged the POST
          <br /><code>&quot;none&quot;</code>: request will return immediately after RESTPP
          processed the POST.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><code>new_vertex_only</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">Boolean value that indicates whether or not to update existing vertices.
        If the value is true, it will only insert new vertices and not update existing
        ones.</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>vertex_must_exist</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">Boolean value that indicates whether or not to insert new vertices. If
        the value is true, the operation will only update existing vertices</td>
    </tr>
  </tbody>
</table>

The response is the number of vertices and edges that were accepted. The API uses JSON format to describe the vertices and edges to be upserted. The JSON code can be stored in a text file or specified directly in a command line. There is a maximum size for a `POST` data payload \(see the [**Size Limits**](intro.md#size-and-time-limits) ****section\). The JSON format for describing a vertex set or edge set is summarized below. 

#### Request body:

The payload data should be in JSON according to the schema shown below:

{% tabs %}
{% tab title="Request body schema" %}
```text
"vertices": {
   "<vertex_type>": {
      "<vertex_id>": {
         "<attribute>": {
            "value": <value>,
            "op": <opcode>
         }
      }
   }
},
"edges": {
   "<source_vertex_type>": {
      "<source_vertex_id>": {
         "<edge_type>": {
            "<target_vertex_type>": {
               "<target_vertex_id>": {
                  "<attribute>": {
                     "value": <value>,
                     "op": <opcode>
                  }
               }
            }
         }
      }
   }
}
```
{% endtab %}
{% endtabs %}

The fields in angle brackets \(`<>`\) are placeholder names or values, to be replaced with actual values. The keys in angle brackets, such as `<vertex_type>`, can be repeated to form a list of items. The keys which are not in angle brackets are exact texts that must be used as they are. The nested hierarchy means that vertices are grouped by type.  Edges, on the other hand, are first grouped by source vertex type, then vertex ID, then edge type. 

The first example below shows two `User` vertices having an attribute called `age`:

{% tabs %}
{% tab title="Upsert Example Data 1: Two User vertices" %}
```bash
{
 "vertices": {
    "User": {
      "id6": {
        "age": {
           "value": 30
         }
      },
      "id1": {
        "age": {
           "value": 22
         }
      }
    }
  }
}
```
{% endtab %}
{% endtabs %}

The second example starts with one `User` vertex. If `id6` already exists, it is not changed. If it doesn't yet exist, it is created with default attribute values. Then two edges are created: a `Liked` edge from `id1` to `id6`, and then a `Liked_By` edge from `id6` to `id1`.

{% tabs %}
{% tab title="Upsert Example Data 2: add\_id6.json" %}
```bash
{
 "vertices": {
    "User": {
      "id6": {
      }
    }
  },
  "edges": {
    "User":{
      "id1": {
        "Liked": {
          "User": {
            "id6" : {
              "weight" : {
                "value": 5.0
              }
            }
          }
        }
      },
      "id6": {
        "Liked_By": {
          "User": {
            "id1" : {
              "weight" : {
                "value": 1.0
              }
            }
          }
        }
      }
    }
  }
}
```
{% endtab %}
{% endtabs %}

Follow the instructions in the Introduction section to [format advanced data types](intro.md#formatting-data-in-json). For example, the following payload is used to upsert two `User` vertices with an attribute `coordinates` of type `LIST` and an attribute `measurements` of type `MAP`:

```bash
{
 "vertices": {
    "User": {
      "id4": {
        "coordinates": {
           "value": [51.3345, -7.2233]
         },
        "measurements": {
           "value": {
             "keyList": ["chest", "waist", "hip"]
             "valueList": [35, 30, 35]
           } 
         }
      },
      "id5": {
        "coordinates": {
           "value": [31.3245, -17.3292]
         },
        "measurements": {
           "value": {
             "keyList": ["chest", "waist", "hip"]
             "valueList": [39, 35, 41]
           } 
         }
      }
    }
  }
}
```

#### Operation codes

Each attribute value may be accompanied by an operation \(op\) code, which provides very sophisticated schemes for data update or insertion:

| Type | op | Meaning |
| :--- | :--- | :--- |
| 1 | `"ignore_if_exists"` or `"~"` | If the vertex/edge does not exist, use the payload value to initialize the attribute; but if the vertex/edge already exists, do not change this attribute. |
| 2 | `"add"` or `"+"` | Add the payload value to the existing value. |
| 3 | `"and"` or `"&"` | Update to the logical AND of the payload value and the existing value. |
| 4 | `"or"` or `"|"` | Update to the logical OR of the payload value and the existing value.   |
| 5 | `"max"` or `">"` | Update to the higher value between the payload value and the existing value.  |
| 6 | `"min"` or `"<"` | Update to the lower value between the payload value and the existing value. |

If an attribute is not given in the payload, the attribute stays unchanged if the vertex/edge already exists, or if the vertex/edge does not exist, a new vertex/edge is created and assigned the default value for that data type. The default value is 0 for `int/uint`, 0.0 for `float/double`, and `""`\(empty string\) for string.

#### Invalid data types cause the request to be rejected

The RESTPP server validates the request before updating the values. The following schema violations will cause the entire request to fail and no change will be made to a graph:

* For vertex upsert:

1. Invalid vertex type.
2. Invalid attribute data type.

* For edge upsert:

1. Invalid source vertex type.
2. Invalid edge type.
3. Invalid target vertex type.
4. Invalid attribute data type.

If an invalid attribute name is given, it is ignored.

#### Output response

The response is the number of vertices and edges that were accepted. Additionally, if `new_vertex_only` is true, the response will include two more fields:

* `skipped_vertices`: the number of vertices in the input data which already existed in the graph
* `vertices_already_exist`: the id and type of the input vertices which were skipped

If `vertex_must_exist` is true, the response will include two more fields:

* `skipped_edges`: the number of edges in the input data rejected because of missing endpoint vertices
* `miss_vertices`: the id and type of the endpoint vertices which were missing

The example file `add_id6.json` \(shown in the **Request Body** section\) upserts one `User` __vertex with `id = "id6"`, one `Liked` __edge, and one `Liked_By` __edge. The `Liked` __edge is from `"id1` " to `"id6"`; the `Liked_By` __edge is from `"id6"` to _`"id1"`_.

The following example submits an upsert request by using the payload data stored in `add_id6.json`.

```java
$ curl -X POST --data-binary @add_id6.json \
"http://localhost:9000/graph"
  
{"accepted_vertices":1,"accepted_edges":2}
```

## Vertices

{% hint style="info" %}
To support multiple graphs within one system, the graph data REST endpoint URLs include an optional graph name.
{% endhint %}

### List vertices

`GET /graph/{graph_name}/vertices/{vertex_type}`

This endpoint returns all vertices having the type _`vertex_type`_ in a graph. __

#### Sample request:

```javascript
curl -X GET "http://localhost:9000/graph/socialNet/vertices/User"

{
  "version": {
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "v_id": "id1",
      "v_type": "User",
      "attributes": {}
    },
    {
      "v_id": "id2",
      "v_type": "User",
      "attributes": {}
    }
    // ... all vertices in graph socialNet of type User
  ]
}
```

#### Parameters

| Name | Required | Description |
| :--- | :--- | :--- |
| `count_only` | No | Takes a boolean value. If the value is true, the `results` field will only contain the count of how many vertices were selected. Default is `false`. |
| `select` | No | Attributes of the selected vertices to return. The parameter takes a list, which is a string of comma-separated values, and will only return the attributes that are provided.  |
| `filter` | No | Conditions used to filter the returned vertices. The parameter takes a list of conditions, which is a string of comma-separated values. If any filter conditions are provided, the endpoint will only return the vertices that satisfy the conditions. Six comparison operators are supported for this parameter: `=`, `!=`, `>`, `>=`, `<` and `<=`. If the value on the right side of an operator is a string literal, it should be enclosed in double-quotes. |
| `limit` | No | Integer value that specifies the total number of vertices to return |
| `sort` | No | Attributes to sort the results by. The parameter takes a list, which is a string of comma-separated values, and will sort the returned vertices based on the attributes provided in the list in order. Add "-" in front of the attribute to sort in descending order. |
| `timeout` | No | Integer that specifies the number of seconds after which the query will time out. If the parameter is set to 0 or isn't provided, the system-wide endpoint timeout setting is applied.  |

### Retrieve a vertex

`GET /graph/{graph_name}/vertices/{vertex_type}/{vertex_id}`

This endpoint will return a single vertice by its vertex ID.

#### Sample request:

```javascript
curl -X GET "http://localhost:9000/graph/socialNet/vertices/User/id1"

{
  "version": {
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "v_id": "id1",
      "v_type": "User",
      "attributes": {}
    }
  ]
}
```

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `select` | No | Attributes of the selected vertices to return. The parameter takes a list, which is a string of comma-separated values, and will only return the attributes that are provided.  |
| `timeout` | No | Integer that specifies the number of seconds after which the query will time out. If the parameter is set to 0 or isn't provided, the system-wide endpoint timeout setting is applied.  |

### Delete vertices

`DELETE /graph/{graph_name}/vertices/{vertex_type}`

This endpoint deletes vertices by their vertex type. The delete operation is a cascading deletion. If a vertex is deleted, then all of the edges connected to it are automatically deleted as well.

#### Sample request:

The response object will contain a `"deleted_vertices"` field that indicates the number of vertices that were deleted

```bash
curl -X DELETE "http://localhost:9000/graph/socialNet/vertices/User"

{
  "version": {
    "edition": "enterprise",
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": {
    "v_type": "person",
    "deleted_vertices": 3
  }
}
```

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `permanent` | No | Takes a boolean value. If the value is true, the deleted vertex IDs can never be inserted back, unless the graph is dropped or the graph store is cleared. |
| `filter` | No | Conditions used to filter the vertices to delete. The parameter takes a list of conditions, which is a string of comma-separated values. If any filter conditions are provided, the endpoint will only delete the vertices that satisfy the conditions. Six comparison operators are supported for this parameter: `=`, `!=`, `>`, `>=`, `<` and `<=`. If the value on the right side of an operator is a string literal, it should be enclosed in double-quotes. |
| `limit` | No | Integer value that specifies the total number of vertices to delete. |
| `sort` | No | Attributes to sort the vertices by. In delete operations,`sort` should always be used together with `limit`. The endpoint will delete the number of vertices under the limit specified in the order specified. The parameter takes a list of attributes, and the endpoint will sort all vertices based on the attributes provided in the list in order. Add `"-"` in front of the attribute to sort by that attribute in descending order. |
| `timeout` | No | Integer that specifies the number of seconds after which the query will time out. If the parameter is set to 0 or isn't provided, the system-wide endpoint timeout setting is applied.  |

### Delete vertices by type

`DELETE /graph/{graph_name}/delete_by_type/vertices/{vertex_type}`

This endpoint deletes all vertices of the given vertex type in a graph. 

#### Sample request:

```bash
curl -X DELETE "http://localhost:9000/graph/poc_graph/delete_by_type/vertices/person"
```

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `permanent` | No | Takes a boolean value. If the value is true, the deleted vertex IDs can never be inserted back, unless the graph is dropped or the graph store is cleared. |
| `ack` | No | If the parameter is set to "none", the delete operation doesn't need to get acknowledgment from any GPE. If it is set to "all" \(default\), the operation needs to get acknowledgment from all GPEs. |

### Delete a vertex

`DELETE /graph/{graph_name}/vertices/{vertex_type}/{vertex_id}`

#### Sample request:

```bash
curl -X DELETE "http://localhost:9000/graph/socialNet/vertices/User/id1"

{
  "version": {
    "edition": "enterprise",
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": {
    "v_type": "User",
    "deleted_vertices": 1
  }
}
```

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `timeout` | no | Integer that specifies the number of seconds after which the query will time out. If the parameter is set to 0 or isn't provided, the system-wide endpoint timeout setting is applied.  |

## Edges

### List edges of a vertex

`GET /graph/{graph_name}/edges/{source_vertex_type}/{source_vertex_id}`

This endpoint returns all edges which are connected to a given vertex ID in the graph

#### Sample request:

```bash
curl -X GET "http://localhost:9000/graph/socialNet/edges/VidUser/0?limit=2

{
  "version": {
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "e_type": "User_Video",
      "directed": false,
      "from_id": "0",
      "from_type": "VidUser",
      "to_id": "2",
      "to_type": "Video",
      "attributes": {
        "rating": 5.2,
        "date_time": 0
      }
    },
    {
      "e_type": "User_Video",
      "directed": false,
      "from_id": "0",
      "from_type": "VidUser",
      "to_id": "0",
      "to_type": "Video",
      "attributes": {
        "rating": 6.8,
        "date_time": 0
      }
    }
  ]
}
```

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `count_only` | No | Takes a boolean value. If the value is true, the `results` field will only contain the count of how many edges were selected. Default is `false`. |
| `select` | No | Attributes of the selected edges to return. The parameter takes a list, which is a string of comma-separated values. If `select` is provided, the edges returned will only show the attributes provided.  |
| `filter` | No | Conditions used to filter the edges to return. The parameter takes a list of conditions, which is a string of comma-separated values. If any filter conditions are provided, the endpoint will only return the edges that satisfy the conditions. Six comparison operators are supported for this parameter: `=`, `!=`, `>`, `>=`, `<` and `<=`. If the value on the right side of an operator is a string literal, it should be enclosed in double-quotes. |
| `limit` | No | Integer value that specifies the maximum limit of the total number of edges to return. |
| `sort` | No | Attributes to sort the results by. The parameter takes a list, which is a string of comma-separated values, and will sort all the edges based on the attributes provided in the list in order. Add `"-"` in front of the attribute to sort in descending order. |
| `timeout` | No | Integer that specifies the number of seconds after which the query will time out. If the parameter is set to `0` or isn't provided, system-wide endpoint timeout setting is applied.  |

### List edges of a vertex by edge type

`GET /graph/{graph_name}/edges/{source_vertex_type}/{source_vertex_id}/{edge_type}`

This endpoint lists all the edges of a specified type connected to a given vertex ID in the graph

#### Sample request:

```bash
curl -X GET "http://localhost:9000/graph/socialNet/edges/VidUser/0/User_Video?limit=2

{
  "version": {
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "e_type": "User_Video",
      "directed": false,
      "from_id": "0",
      "from_type": "VidUser",
      "to_id": "2",
      "to_type": "Video",
      "attributes": {
        "rating": 5.2,
        "date_time": 0
      }
    },
    {
      "e_type": "User_Video",
      "directed": false,
      "from_id": "0",
      "from_type": "VidUser",
      "to_id": "0",
      "to_type": "Video",
      "attributes": {
        "rating": 6.8,
        "date_time": 0
      }
    }
  ]
}
```

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `count_only` | No | Takes a boolean value. If the value is true, the `results` field will only contain the count of how many edges were selected. Default is `false`. |
| `select` | No | Attributes of the selected edges to return. The parameter takes a list, which is a string of comma-separated values. If `select` is provided, the edges returned will only show the attributes provided.  |
| `filter` | No | Conditions used to filter the edges to return. The parameter takes a list of conditions, which is a string of comma-separated values. If any filter conditions are provided, the endpoint will only return the edges that satisfy the conditions. Six comparison operators are supported for this parameter: `=`, `!=`, `>`, `>=`, `<` and `<=`. If the value on the right side of an operator is a string literal, it should be enclosed in double quotes. |
| `limit` | No | Integer value that specifies the maximum limit of the total number of edges to return. |
| `sort` | No | Attributes to sort the results by. The parameter takes a list, which is a string of comma-separated values, and will sort all the edges based on the attributes provided in the list in order. Add `"-"` in front of the attribute to sort in descending order. |
| `timeout` | No | Integer that specifies the number of seconds after which the query will time out. If the parameter is set to `0` or isn't provided, system-wide endpoint timeout setting is applied.  |

### List edges of a vertex by edge type and target type

```bash
GET /graph/{graph_name}/edges/{source_vertex_type}/{source_vertex_id}/{edge_type}/{target_vertex_type}
```

This endpoint lists edges connected to a given vertex by edge type and target vertex type

{% hint style="info" %}
Use `"_"` for `edge_type` in the URL to permit any edge type.
{% endhint %}

#### Sample request:

```php
curl -X GET "http://localhost:9000/graph/socialNet/edges/VidUser/0/User_Video/Video?limit=2

{
  "version": {
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "e_type": "User_Video",
      "directed": false,
      "from_id": "0",
      "from_type": "VidUser",
      "to_id": "2",
      "to_type": "Video",
      "attributes": {
        "rating": 5.2,
        "date_time": 0
      }
    },
    {
      "e_type": "User_Video",
      "directed": false,
      "from_id": "0",
      "from_type": "VidUser",
      "to_id": "0",
      "to_type": "Video",
      "attributes": {
        "rating": 6.8,
        "date_time": 0
      }
    }
  ]
}
```

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `count_only` | No | Takes a boolean value. If the value is true, the `results` field will only contain the count of how many edges were selected. Default is `false`. |
| `not_wildcard` | No | Boolean value that indicates whether or not `"_"` supplied in the endpoint URL is a wildcard. If the parameter is true, `"_"` is interpreted literally to select only edges with edge type name equal to underscore. |
| `select` | No | Attributes of the selected edges to return. The parameter takes a list, which is a string of comma-separated values. If `select` is provided, the edges returned will only show the attributes provided.  |
| `filter` | No | Conditions used to filter the edges to return. The parameter takes a list of conditions, which is a string of comma-separated values. If any filter conditions are provided, the endpoint will only return the edges that satisfy the conditions. Six comparison operators are supported for this parameter: `=`, `!=`, `>`, `>=`, `<` and `<=`. If the value on the right side of an operator is a string literal, it should be enclosed in double-quotes. |
| `limit` | No | Integer value that specifies the maximum limit of the total number of edges to return. |
| `sort` | No | Attributes to sort the results by. The parameter takes a list, which is a string of comma-separated values, and will sort all the edges based on the attributes provided in the list in order. Add `"-"` in front of the attribute to sort in descending order. |
| `timeout` | No | Integer that specifies the number of seconds after which the query will time out. If the parameter is set to `0` or isn't provided, the system-wide endpoint timeout setting is applied.  |

### Retrieve edge by source, target, and edge type

```bash
GET /graph/{graph_name}/edges/{source_vertex_type}/{source_vertex_id}/{edge_type}/{target_vertex_type}/{target_vertex_id}
```

This endpoint returns the edge of a specified type between a source vertex and a target vertex.

#### Sample request:

```bash
curl -X GET "http://localhost:9000/graph/socialNet/edges/VidUser/0/User_Video/Video/2"

{
  "version": {
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "e_type": "User_Video",
      "directed": false,
      "from_id": "0",
      "from_type": "VidUser",
      "to_id": "2",
      "to_type": "Video",
      "attributes": {
        "rating": 5.2,
        "date_time": 0
      }
    }
   ]
 } 
```

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `select` | No | Attributes of the selected edges to return. The parameter takes a list, which is a string of comma-separated values. If `select` is provided, the edges returned will only show the attributes provided.  |
| `timeout` | No | Integer that specifies the number of seconds after which the query will time out. If the parameter is set to `0` or isn't provided, the system-wide endpoint timeout setting is applied.  |

### Delete an edge

```bash
DELETE /graph/{graph_name}/edges/{source_vertex_type}/{source_vertex_id}/{edge_type}/{target_vertex_type}/{target_vertex_id}
```

Deletes an edge by its source vertex type and ID, target vertex type and ID, as well as edge type. 

#### Sample request

```bash
$ curl -X DELETE "https://crunch.i.tgcloud.io:9000/graph/CrunchBasePre_2013/edges/person/p:23601/work_for_company/company/c:14478"

# Response
{
  "version": {
    "edition": "enterprise",
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "e_type": "work_for_company",
      "deleted_edges": 1
    }
  ]
}
```

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `timeout` | no | Integer that specifies the number of seconds after which the query will time out. If the parameter is set to 0 or isn't provided, the system-wide endpoint timeout setting is applied. |

## Queries

### Get query metadata

`GET /gsqlserver/gsql/queryinfo`

Returns metadata details about a query. In particular, it lists the input parameters and output `PRINT` statement syntax. **This endpoint exists on port 14240 and requests are sent to the GSQL server.** Therefore, you should provide authentication credentials in the request. 

#### Sample request:

```sql
$ curl -u tigergraph:tigergraph -X GET \
"http://localhost:14240/gsqlserver/gsql/queryinfo?graph=workNet&query=to_vertex_setTest"

{
  "output": [
    {
      "v": "vertex"
    },
    {
      "@@v2": "SetAccum<vertex>"
    },
    {
      "S2": [
        {
          "v_id": "int",
          "attributes": {
            "interestList": "INT_LIST",
            "skillSet": "INT_SET",
            "skillList": "INT_LIST",
            "locationId": "STRING",
            "interestSet": "INT_SET",
            "id": "STRING"
          },
          "v_type": "person"
        },
        {
          "v_id": "int",
          "attributes": {
            "country": "STRING",
            "id": "STRING"
          },
          "v_type": "company"
        }
      ]
    },
    {
      "SDIFF.size()": "int"
    }
  ],
  "input": {
    "uid": "string",
    "uids": "set<string>",
    "vtype": "string"
  },
  "queryname": "to_vertex_setTest",
  "error": false,
  "message": "",
  "version": {
    "schema": 0,
    "edition": "DEVELOPER_EDITION",
    "api": "V2"
  }
}
```

The JSON response object contains three fields:

* **`queryname`**: name of the query, same as the query input parameter.
* **`input`**: unordered list of the input parameter names and data types. 
* **`output`**: JSON object that follows the same structure of the query's output. For each key-value pair, the key is the name that appears in the query output, while the values are the data types of the output.

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `graph` | Yes | Name of the graph |
| `query` | Yes | Name of the query |

### Run an installed query \(`GET`\)

`GET /query/{graph_name}/{query_name}` 

Each time a new TigerGraph query is installed, a dynamic endpoint is generated. This new endpoint enables the user to run the new TigerGraph query through HTTP requests and giving the parameters in URL or in a data payload. In the case of a `GET` request, parameters should be passed in through the query string.

#### Parameter passing:

When using a `GET` request to run an installed query, the query parameters are [passed in through the query string of the URL](intro.md#query-string-parameter-passing). 

#### Sample request:

To run query `hello` on a graph named `social`, and the query parameter is of type `VERTEX<person>` whose ID is `"Tom"`

{% code title="Running a query via HTTP request" %}
```bash
curl -X GET "http://localhost:9000/query/social/hello?p=Tom"
```
{% endcode %}

### Run an installed query \(`POST`\)

`POST /query/{graph_name}/{query_name}`

Users can also run queries through a `POST` request, which allows them to pass query parameters in JSON. This is especially helpful when the query takes complex parameters. 

#### Parameter Passing:

When using a `POST` request to run an installed query, the query parameters are passed in through the request body and [encoded in JSON format](intro.md#formatting-data-in-json). 

#### Sample request:

The query in this request takes a parameter of type `VERTEX<person>`:

```bash
curl -X POST -d '{"p":{"id":"Tom","type":"person"}}' \
"http://localhost:9000/query/social/hello"
```

{% hint style="info" %}
Installed queries can run in [Detached Mode](../gsql-ref/querying/query-operations.md#detached-mode-async-option). To do this, use the `GSQL-ASYNC`header and set its value to `true`. The [results](built-in-endpoints.md#check-query-status-detached-mode) and [status](built-in-endpoints.md#check-query-status-detached-mode) of the queries run in Detached Mode can be retrieved with a query ID, which is returned immediately when queries are executed in Detached Mode.
{% endhint %}

### Run an interpreted query

`POST /gsqlserver/interpreted_query`

This endpoint runs a GSQL query in Interpreted Mode. The query body should be supplied at the data payload, and the query's parameters are supplied as the URL's query string. **This endpoint exists on the GSQL server on port 14240.**

This request goes directly to the GSQL server \(port 14240\) instead of the RESTPP server \(port 9000\), so the username and password must be specified in the header. If you are using curl, you can use the `-u` option as shown below. 

#### Request body:

The request body for this endpoint should be the entire `INTERPRET QUERY` statement.

#### Parameter passing:

When running an interpreted query through this endpoint, the query parameters should be [passed in through the URL query string](intro.md#query-string-parameter-passing).

#### Sample request:

```javascript
curl --fail -u <my_username>:<my_password> -X POST \
"http://localhost:14240/gsqlserver/interpreted_query?a=10" \
-d 'INTERPRET QUERY (INT a) FOR GRAPH gsql_demo {
    PRINT a;
 }'
```

### List running queries

`GET /showprocesslist/{graph_name}`

This endpoint reports statistics of running queries of a graph: the query's request ID, start time, expiration time, and the REST endpoint's URL.

#### Sample request:

```bash
curl -X GET "http://localhost:9000/showprocesslist/poc_graph" | jq .

{
  "version": {
    "edition": "enterprise",
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "requestid": "65538.RESTPP_1_1.1558386411523.N",
      "startTime": "2019-05-20 14:06:51.523",
      "expirationTime": "2019-05-20 14:15:11.523",
      "url": "/sleepgpe?milliseconds=100001"
    },
    {
      "requestid": "196609.RESTPP_1_1.1558386401478.N",
      "startTime": "2019-05-20 14:06:41.478",
      "expirationTime": "2019-05-20 14:15:01.478",
      "url": "/sleepgpe?milliseconds=100000"
    }
  ],
  "code": "REST-0000"
}
```

#### Parameters:

No Parameters.

### Abort a query

`GET /abortquery/{graph_name}`

This endpoint safely aborts a selected query by ID or all queries of an endpoint by endpoint URL of a graph. 

#### Sample request:

```graphql
curl -X GET "localhost:9000/abortquery/poc_graph?requestid=16842763.RESTPP_1_1.1561401340785.N&requestid=16973833.RESTPP_1_1.1561401288421.N"

{
  "version": {
    "edition": "enterprise",
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [
    {
      "aborted_queries": [
        {
          "requestid": "16842763.RESTPP_1_1.1561401340785.N",
          "url": "/sleepgpe?milliseconds=110000"
        },
        {
          "requestid": "16973833.RESTPP_1_1.1561401288421.N",
          "url": "/sleepgpe?milliseconds=100000"
        }
      ]
    }
  ],
  "code": "REST-0000"
}
```

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `requestid` | No | The ID of the query to abort. It can take a single query ID or the string `"all"`. If `requestid` is set to all. It will abort all running queries. |
| `url` | No | The endpoint whose running queries to abort. You must specify the base of the endpoint's URL, but then use a wildcard to allow for different parameters. For example, to abort all running queries for the endpoint `/sleepgpe`, use `url=/sleepgpe.*`  |

### Check query status \(Detached Mode\)

`GET /query_status`

This endpoint allows you to check the status of a query run in [detached mode](../gsql-ref/querying/query-operations.md#detached-mode-async-option).

#### Sample request:

```bash
$ curl -s -X GET "http://localhost:9000/query_status?graph_name=poc_graph&requestid=4.RESTPP_1_1.1599672031541.N"

{
  "version": {
    "edition": "enterprise",
    "api": "v2",
    "schema": 0
  },
  "error": false,
  "message": "",
  "results": [{
    "requestid": "4.RESTPP_1_1.1599672031541.N",
    "startTime": "2020-09-09 10:20:31.541",
    "expirationTime": "2020-09-09 10:20:47.541",
    "url": "/query/ldbc_snb/countIndirectFriends?pid=21990232555889",
    "elapsedTime": 19,
    "status": "success"
  }]
}
```

| **Field** | **Description** |
| :--- | :--- |
| `url` | URL of the given query. |
| `status` | The status of the given query. Possible values are `“success”`, `“timeout”`, `“aborted”`, or `“running”`. |
| `startTime` | The timestamp for the start time of the given query. |
| `requestid` | The query ID associated with the given query status JSON object. |
| `expirationTime` | The timestamp for when the given query times out. The default timeout limit is 16 seconds and can be set using the[`GSQL-TIMEOUT`](intro.md#gsql-query-timeout) header. |
| `elapsedTime` | Elapsed real time of the given query measured in milliseconds. For completed queries, the value shows the total runtime of the request. For ongoing queries, it shows the amount of time taken so far. |

If one or more of the provided query IDs \(`requestid`\) are invalid, the return JSON will include an`unknown_requestid`field containing all the invalid query IDs. If a query ID is marked as unknown, it means either the query does not exist or that it was not run in Detached Mode. 

#### Parameters:

<table>
  <thead>
    <tr>
      <th style="text-align:left"><b>Name</b>
      </th>
      <th style="text-align:left"><b>Required</b>
      </th>
      <th style="text-align:left"><b>Description</b>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left"><code>graph_name</code>
      </td>
      <td style="text-align:left">Yes</td>
      <td style="text-align:left">Name of the graph the query belongs to. Required parameter.</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>requestid</code>
      </td>
      <td style="text-align:left">No</td>
      <td style="text-align:left">
        <p>String ID of the query. It also accepts the value <code>&quot;all&quot;</code>,
          in which case it will return a status report for every running query. When
          multiple <code>requestid</code> are provided, it will return the status of
          all corresponding queries. If no <code>requestid</code> is provided, or if
          the value of <code>requestid</code> is <code>&quot;all&quot;</code>, it will
          return the status of all queries that are currently running.</p>
        <p>The output will contain one JSON object for each query.</p>
      </td>
    </tr>
  </tbody>
</table>

### Check query results \(Detached Mode\)

`GET /query_result`

This endpoint allows you to check the results of queries run in Detached Mode if they have finished running. If the query is still running, the endpoint will respond with an error and a message saying `"Unable to retrieve result for query <requestid>"`.  Ensure that the query is finished before checking its result.

#### Sample request:

```sql
$ curl -s -X GET "http://localhost:9000/query_result?request_id=4.RESTPP_1_1.1599672031541.N"

{
  "error": false,
  "message": "",
  "version": {
    "edition": "enterprise",
    "api": "v2",
    "schema": 0
  },
  "results": [{"vSet": [{
    "v_id": "21990232555889",
    "attributes": {"vSet.@friendCount": 13677},
    "v_type": "Person"
  }]}]
}
```

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `requestid` | Yes | String ID of the query.  |

## Path-Finding Algorithms

The TigerGraph platform comes with two built-in endpoints, `/shortestpath` and `/allpaths`, which return either the shortest or all unweighted paths connecting a set of source vertices to a set of target vertices. The table below summarizes the two path-finding endpoints.

### Input Parameters and Output Format for Path-Finding

Each REST endpoint reads a JSON-formatted payload that describes the input parameters. These parameters specify which vertices and edges may be on the paths, additional conditions on the attributes of the vertices and edges, and the maximum length of a path.

#### Source and target vertices

Each endpoint must have either a **source** or **sources** key and either a **target** or **targets** parameter. The source and target parameters describe a single vertex. The format for a vertex object is as follows: `{"type" : "<vertex_type_name>", "id" : "<vertex_id>"}.`  The sources and targets parameters are JSON arrays containing a list of vertex objects.

**Filters**  
The payload may also have an array of filter conditions, to restrict the vertices or edges in the paths. Each individual filter is a JSON object which describes a condition on one vertex type or edge type.  A filter object has one or two key-value pairs: `{"type": "<vertex_or_edge_type>", "condition": "<attribute_condition>"}`

* `"type":` the vertex type or edge type to be filtered
* `"condition"` \(optional\): a boolean expression on one attribute of the given vertex type or edge type. "AND" and "OR" may be used to make compound expressions.

Example of a filter array:

```markup
[{"type": "bought", "condition": "price < \"100\" and quality == \"good\""},
 {"type": "sold",   "condition": "price > \"100\"  or quality != \"good\""}]
```

Note that all filtering conditions in **`vertexFilters`** and **`edgeFilters`** are combined with the `"OR"`  relationship, i.e., if a vertex \(or edge\) fulfills any one of the filter conditions, then this vertex \(or edge\) will be included in the resulting paths.

#### Output

The JSON output is a list of vertices and a list of edges. Each vertex and each edge is listed in full, with all attributes.  The collections of vertices and edges are not in path order.  

### Find shortest path

`POST /shortestpath/{graph_name}`

This endpoint takes a source vertex or a set of source vertices, a target vertex or a set of target vertices, and returns the shortest path between the source and the target. If the source is a set of vertices, the resulting path will begin with one of the vertices in the set. If the target is a set of vertices, the resulting path will end with one of the vertices in the set. 

#### Request body:

This endpoint expects a request body that describes the source and target vertex or vertex set. Below is a table of all the fields in the request body. 

| Key | Type | Description |
| :--- | :--- | :--- |
| `source` | vertex object | Each path must start from this vertex. Mutually exclusive with `sources`. |
| `sources` | vertex array | Each path must start from one of these vertices. Mutually exclusive with `source`. |
| `target` | vertex object | Each path must end at this vertex. Mutually exclusive with `targets`. |
| `targets` | vertex array | Each path must end at one of these vertices. Mutually exclusive with `target`. |
| `vertexFilters` | filter array | \(OPTIONAL\) Restrict the paths to those whose vertices satisfy any of the given filters.  |
| `edgeFilters` | filter array | \(OPTIONAL\) Restrict the paths to those whose edges satisfy any of the given filters. See details of filters above. |

#### Sample request:

```bash
curl -s -X POST "http://localhost:9000/shortestpath/movieNet" \
-d '{
  "sources":[{"type":"VidUser","id":"2"}],
  "targets":[{"type":"VidUser","id":"0"}, {"type":"VidUser","id":"3"}],
  "edgeFilters":[{"type":"User_Video","condition":"rating > 5 and date_time > 1000"}],
  "maxLength":4
}'

# Result is an array of vertex json objects and edge json objects,
# describing the subgraph for all found vertices and edges.
{
  "version": { "edition": "developer", "api": "v2", "schema": 0 },
  "error": false,
  "message": "Cannot get 'vertex_filters' filters, use empty filter.",
  "results": [
    {
      "vertices": [
        { "v_id": "3","v_type": "VidUser","attributes": { "name": "Dale" }},
        { "v_id": "0","v_type": "Video","attributes": { "name": "Solo", "year", 2018 }},
        { "v_id": "0","v_type": "VidUser","attributes": { "name": "Angel" }},
      ],
      "edges": [
        {
          "e_type": "User_Video", "from_id": "0", "from_type": "Video",
          "to_id": "0", "to_type": "VidUser", "directed": false,
          "attributes": { "rating": 6.8, "date_time": 15000 }
        },
        {
          "e_type": "User_Video", "from_id": "0", "from_type": "Video",
          "to_id": "3", "to_type": "VidUser",  "directed": false,
          "attributes": { "rating": 6.6, "date_time": 16000 }
        }
      ]
    }
  ]
}
```

#### Parameters:

| Key | Required | Description |
| :--- | :--- | :--- |
| `maxLength` | No | Integer that specified the maximum length of a shortest path. The default value is 6. |
| `allShortestPaths` | No | If **true**, the endpoint will return all shortest paths between the source and target. Default is **false**, meaning that the endpoint will return only one path. |

### Find all paths

`POST /allpaths/{graph_name}`

This endpoint finds all paths between a source vertex \(or vertex set\) and target vertex \(or vertex set\).

#### Request body:

This endpoint expects a request body that describes the source and target vertex or vertex set. Below is a table of all the fields in the request body. 

| Key | Type | Description |
| :--- | :--- | :--- |
| `source` | vertex object | Each path must start from this vertex. Mutually exclusive with `sources`. |
| `sources` | vertex array | Each path must start from one of these vertices. Mutually exclusive with `source`. |
| `target` | vertex object | Each path must end at this vertex. Mutually exclusive with `targets`. |
| `targets` | vertex array | Each path must end at one of these vertices. Mutually exclusive with `target`. |
| `vertexFilters` | filter array | \(OPTIONAL\) Restrict the paths to those whose vertices satisfy any of the given filters.  |
| `edgeFilters` | filter array | \(OPTIONAL\) Restrict the paths to those whose edges satisfy any of the given filters. See details of filters above. |

#### Parameters:

| Name | Required | Description |
| :--- | :--- | :--- |
| `maxLength` | Yes | Maximum path length. |

{% hint style="danger" %}
The current implementation of this endpoint will include paths with loops. Since it is possible to go around a loop an infinite number of times, it is important that you select the smallest value of maxLength which you consider appropriate.  Even if there are no loops in your graph, a smaller maxLength will allow your query to run faster.
{% endhint %}

#### Sample request:

The example below requests all paths between the source vertex set {Video 0} and the target vertex set {AttributeTag "action"}, up to maximum length 3. The path may only contain Video vertices where `year >= 1984`. The result includes 3 paths:  
AttrributeTag "action"  --  Video 0  
AttrributeTag "action"  --  Video 3 -- VidUser 4 -- Video 0  
AttrributeTag "action"  --  Video 2 -- VidUser 0 -- Video 0

```bash
curl -s -X POST "http://localhost:9000/allpaths/movieNet" \
-d '{
  "sources":[{"type":"Video","id":"0"}],
  "targets":[{"type": "AttributeTag", "id":"action"}],
  "vertexFilters":[{"type":"Video", "condition":"year >= 1984"}],
  "maxLength": 3
}'

# Result is an array of vertex json objects and edge json objects,
# indicating the subgraph for all found vertices and edges.
{
  "version": { "edition": "developer", "api": "v2", "schema": 0 },
  "error": false,
  "message": "Cannot get 'edge_filters' filters, use empty filter.",
  "results": [
    {
      "vertices": [
        { "v_id": "action","v_type": "AttributeTag","attributes": {}},
        { "v_id": "3","v_type": "VidUser","attributes": { "name": "Dale" }},
        { "v_id": "0","v_type": "VidUser","attributes": { "name": "Angel" }},
        { "v_id": "0","v_type": "Video","attributes": { "name": "Solo", "year", 2018 }},
        { "v_id": "2","v_type": "Video","attributes": { "name": "Thor", "year", 2011 }},
        { "v_id": "4","v_type": "Video","attributes": { "name": "Ran", "year", 1985 }}
      ],
      "edges": [
        {
          "e_type": "Video_AttributeTag", "from_id": "0", "from_type": "Video",
          "to_id": "action", "to_type": "AttributeTag", "directed": false,
          "attributes": { "weight": 1, "date_time": 0 }
        },
        {
          "e_type": "Video_AttributeTag", "from_id": "4", "from_type": "Video",
          "to_id": "action", "to_type": "AttributeTag", "directed": false,
          "attributes": { "weight": 1, "date_time": 11000 }
        },
        {
          "e_type": "User_Video", "from_id": "3", "from_type": "VidUser",
          "to_id": "4", "to_type": "Video", "directed": false,
          "attributes": { "rating": 8.4, "date_time": 12000 }
        },
        {
          "e_type": "User_Video", "from_id": "3", "from_type": "VidUser",
          "to_id": "0", "to_type": "Video", "directed": false,
          "attributes": { "rating": 6.6, "date_time": 16000 }
        },   
        {
          "e_type": "Video_AttributeTag", "from_id": "2", "from_type": "Video",
          "to_id": "action", "to_type": "AttributeTag", "directed": false,
          "attributes": { "weight": 1, "date_time": 0 }
        },
        {
          "e_type": "User_Video", "from_id": "2", "from_type": "VidUser",
          "to_id": "0", "to_type": "Video", "directed": false,
          "attributes": { "rating": 7.4, "date_time": 17000 }
        },
        {
          "e_type": "User_Video", "from_id": "0", "from_type": "Video",
          "to_id": "0", "to_type": "VidUser", "directed": false,
          "attributes": { "rating": 6.8, "date_time": 15000 }
        }
      ]
    }
  ]
}
```

Other versions of pathfinding algorithms are available in the [GSQL Graph Algorithm Library](../../tigergraph-platform-overview/graph-algorithm-library.md#path-algorithms).  


