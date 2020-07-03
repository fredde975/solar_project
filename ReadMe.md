# Things to fix
Seems like I have to load the new s3 partitions into athena before I can query the data
Do I need to run this in the script  "MSCK REPAIR TABLE fhbase;" ?!

# setup
```
sudo pip3 install virtualenv 
virtualenv venv
source /venv/bin/activate
pip install -r requirements.txt
```

# Running the program

```
python solar/solar.py 
```

# Set up credentials

```
export AWS_ACCESS_KEY_ID=XXX
export AWS_SECRET_ACCESS_KEY=YYY
```

# Description
The program publishes json solar data on a Kinesis Firehose that writes to an s3 bucket. 

The data is partitioned with Year=2020/Month=04/Day=30/hour=13

Uploaded data looks like this: 
```
{"timestamp": "2020-04-29T16:03:18+02:00", "energy_day_wh": 30098, "energy_total_wh": 2859539.75, "energy_year_wh": 2842461.25, "current_power_wh": 1674}
```

# Athena
```
MSCK REPAIR TABLE fhbase; # import new partitions

SELECT * FROM "solceller"."fhbase" where day = '01' order by timestamp desc
```

example of select:

```
SELECT * FROM "solceller"."fhbase" 
where year = '2020'
and month = '07'
and day = '01'
and hour = '00';
```

Output
```
timestamp	energy_day_wh	energy_total_wh	energy_year_wh	current_power_wh	source_ip	source_host	year	month	day	hour
2020-07-01T02:31:56+02:00	0	6473950.0	6456864.5		127.0.1.1	raspberrypi	2020	7	1	0
2020-07-01T02:32:57+02:00	0	6473950.0	6456864.5		127.0.1.1	raspberrypi	2020	7	1	0
2020-07-01T02:33:57+02:00	0	6473950.0	6456864.5		127.0.1.1	raspberrypi	2020	7	1	0
2020-07-01T02:34:58+02:00	0	6473950.0	6456864.5		127.0.1.1	raspberrypi	2020	7	1	0
2020-07-01T02:35:58+02:00	0	6473950.0	6456864.5		127.0.1.1	raspberrypi	2020	7	1	0
2020-07-01T02:57:08+02:00	0	6473950.0	6456864.5		127.0.1.1	raspberrypi	2020	7	1	0
2020-07-01T02:58:08+02:00	0	6473950.0	6456864.5		127.0.1.1	raspberrypi	2020	7	1	0
2020-07-01T02:59:09+02:00	0	6473950.0	6456864.5		127.0.1.1	raspberrypi	2020	7	1	0
2020-07-01T03:00:09+02:00	0	6473950.0	6456864.5		127.0.1.1	raspberrypi	2020	7	1	0
2020-07-01T03:01:09+02:00	0	6473950.0	6456864.5		127.0.1.1	raspberrypi	2020	7	1	0
2020-07-01T02:06:43+02:00	0	6473950.0	6456864.5		127.0.1.1	raspberrypi	2020	7	1	0
2020-07-01T02:07:44+02:00	0	6473950.0	6456864.5		127.0.1.1	raspberrypi	2020	7	1	0
```


BUG!!!
```
Your query has the following error(s):

HIVE_BAD_DATA: Error parsing field value '0.5' for field 1: For input string: "0.5"

This query ran against the "solceller" database, unless qualified by the query. Please post the error message on our forum or contact customer support with Query Id: 284c4bc0-2413-4bed-aa00-540ae86a1978.
```

From file in s3:
```
{"timestamp": "2020-07-01T03:47:31+02:00", "energy_day_wh": 0.5, "energy_total_wh": 6473950, "energy_year_wh": 6456864.5, "current_power_wh": null, "source_ip": "127.0.1.1", "source_host": "raspberrypi"}
{"timestamp": "2020-07-01T03:48:31+02:00", "energy_day_wh": 0.5, "energy_total_wh": 6473950, "energy_year_wh": 6456864.5, "current_power_wh": null, "source_ip": "127.0.1.1", "source_host": "raspberrypi"}
{"timestamp": "2020-07-01T03:49:31+02:00", "energy_day_wh": 0.5, "energy_total_wh": 6473950, "energy_year_wh": 6456864.5, "current_power_wh": null, "source_ip": "127.0.1.1", "source_host": "raspberrypi"}
{"timestamp": "2020-07-01T03:50:32+02:00", "energy_day_wh": 0.6000000238418579, "energy_total_wh": 6473950, "energy_year_wh": 6456864.5, "current_power_wh": null, "source_ip": "127.0.1.1", "source_host": "raspberrypi"}
{"timestamp": "2020-07-01T03:51:32+02:00", "energy_day_wh": 0.6000000238418579, "energy_total_wh": 6473950, "energy_year_wh": 6456864.5, "current_power_wh": null, "source_ip": "127.0.1.1", "source_host": "raspberrypi"}

```


# Packaging
```
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel

```

This command should output a lot of text and once completed should generate two files in the dist directory:
```

dist/
    solar-pkg-fredrik-0.0.1.tar.gz           
    solar_pkg_fredrik-0.0.1-py3-none-any.whl
```

The tar.gz file is a source archive whereas the .whl file is a built distribution. Newer pip versions preferentially install built distributions, but will fall back to source archives if needed. You should always upload a source archive and provide built archives for the platforms your project is compatible with. In this case, our example package is compatible with Python on any platform so only one built distribution is needed.

# Copy to RaspberryPi
```
cd dist
scp solar-pkg-fredrik-0.0.1.tar.gz pi@192.168.1.238:
```

# Edit crontab on RaspberryPi

Start every hour at minute 0 every day 
```
0 * * * * /bin/bash -c "./solar/solar-pkg-fredrik-0.0.1/solar/start_solar_service.sh   >> /tmp/solar.log  2>&1"
```

# Enable crontab logging
You can enable logging for cron jobs in order to track problems. You need to edit the /etc/rsyslog.conf file and make 
sure you have the following line uncommented:

```
cron.*                          /var/log/cron.log

```
 
Then restart rsyslog and cron:
    
```
sudo service rsyslog restart
sudo service cron restart
```

# script on raspberry pi to start program
```
#!/bin/bash

unalias -a
trap onexit SIGINT SIGSEGV SIGQUIT SIGTERM

prog="solar"
lock="/tmp/${prog}.lock"

onexit () {
        rm -f "${lock}"
        exit
}

# check if the lock file is in place.
if [ -f $lock ]; then
        # silent exit is better from cron jobs,
        echo "$0 Error: Lock file $lock is in place."
        echo "Make sure an old instance of this program is not running, remove it and try again."
        exit
fi
date > $lock

#
# your script goes here
#
cd /home/pi/solar/solar-pkg-fredrik-0.0.1/solar

source ./credentials.sh
source venv/bin/activate
python solar.py
 
# 
# exit your program calling onexit
#

onexit

```

# read stout on raspberrypi

```
ps -ef                              # look for the process pid
sudo tail -f /proc/21913/fd/1       # tail stout from process
```



# Other material
CREATE EXTERNAL TABLE IF NOT EXISTS solceller2.solceller_table (
  `timestamp` string,
  `energy_day_wh` int,
  `energy_total_wh` float,
  `energy_year_wh` float,
  `current_power_wh` int 
) PARTITIONED BY (
  year int,
  month int,
  day int,
  hour int 
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = '1'
) LOCATION 's3://stellavagen-solceller/'
TBLPROPERTIES ('has_encrypted_data'='false');


{"timestamp": "2020-04-29T16:03:18+02:00", "energy_day_wh": 30098, "energy_total_wh": 2859539.75, "energy_year_wh": 2842461.25, "current_power_wh": 1674}
{"timestamp": "2020-04-29T16:04:18+02:00", "energy_day_wh": 30127, "energy_total_wh": 2859569.75, "energy_year_wh": 2842490, "current_power_wh": 1656}
{"timestamp": "2020-04-29T16:05:19+02:00", "energy_day_wh": 30155, "energy_total_wh": 2859600, "energy_year_wh": 2842516.75, "current_power_wh": 1645}
{"timestamp": "2020-04-29T16:06:19+02:00", "energy_day_wh": 30183, "energy_total_wh": 2859630, "energy_year_wh": 2842545.25, "current_power_wh": 1643}
{"timestamp": "2020-04-29T16:07:19+02:00", "energy_day_wh": 30210, "energy_total_wh": 2859649.75, "energy_year_wh": 2842572, "current_power_wh": 1675}

HIVE_PARTITION_SCHEMA_MISMATCH: There is a mismatch between the table and partition schemas. The types are incompatible and cannot be coerced. The column 'energy_day_wh' in table 'solceller2.stellavagen_solceller' is declared as type 'double', but partition 'partition_0=2020/partition_1=04/partition_2=29/partition_3=06' declared column 'energy_day_wh' as type 'int'.

This query ran against the "solceller2" database, unless qualified by the query. Please post the error message on our forum or contact customer support with Query Id: 8069c7e2-e454-4cdd-a7bd-a08cd1998f8b.

http://192.168.1.68/solar_api/v1/GetPowerFlowRealtimeData.fcgi
{
   "Body" : {
      "Data" : {
         "Inverters" : {
            "1" : {
               "DT" : 232,
               "E_Day" : 4349,
               "E_Total" : 2867440,
               "E_Year" : 2850357.75,
               "P" : 3088
            }
         },
         "Site" : {
            "E_Day" : 4349,
            "E_Total" : 2867440,
            "E_Year" : 2850357.75,
            "Meter_Location" : "unknown",
            "Mode" : "produce-only",
            "P_Akku" : null,
            "P_Grid" : null,
            "P_Load" : null,
            "P_PV" : 3088,
            "rel_Autonomy" : null,
            "rel_SelfConsumption" : null
         },
         "Version" : "12"
      }
   },
   "Head" : {
      "RequestArguments" : {},
      "Status" : {
         "Code" : 0,
         "Reason" : "",
         "UserMessage" : ""
      },
      "Timestamp" : "2020-04-30T08:38:29+02:00"
   }
}


{
  "timestamp": {
    "value": "2020-04-27T17:29:23+02:00"
  },
  "status": {
    "Code": 0,
    "Reason": "",
    "UserMessage": ""
  },
  "energy_day": {
    "value": 44730,
    "unit": "Wh"
  },
  "energy_total": {
    "value": 2807249.75,
    "unit": "Wh"
  },
  "energy_year": {
    "value": 2790167.25,
    "unit": "Wh"
  },
  "meter_location": {
    "value": "unknown"
  },
  "meter_mode": {
    "value": "produce-only"
  },
  "power_battery": {
    "value": null,
    "unit": "W"
  },
  "power_grid": {
    "value": null,
    "unit": "W"
  },
  "power_load": {
    "value": null,
    "unit": "W"
  },
  "power_photovoltaics": {
    "value": 552,
    "unit": "W"
  },
  "relative_autonomy": {
    "value": null,
    "unit": "%"
  },
  "relative_self_consumption": {
    "value": null,
    "unit": "%"
  }
}


Prefix - optional
"fhbase/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/"

Error prefix - optional
Customizable through the CLI
"fherroroutputbase/!{firehose:random-string}/!{firehose:error-output-type}/!{timestamp:yyyy/MM/dd}/"