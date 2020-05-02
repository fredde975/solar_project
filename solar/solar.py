"""Basic usage example and testing of pyfronius."""
import asyncio
import json
import logging
import os
from time import sleep
import requests
import aiohttp
import pyfronius
import boto3
import socket

# os.environ["AWS_REGION"] = "eu-west-1"
# os.environ["AWS_ACCESS_KEY_ID"] = ""
# os.environ["AWS_SECRET_ACCESS_KEY"] = ""
# os.environ["AWS_SESSION_TOKEN"] = ""

# http://192.168.1.68/solar_api/v1/GetPowerFlowRealtimeData.fcgi
IP = "192.168.1.68"
URL_POWER_FLOW = "http://{}/solar_api/v1/GetPowerFlowRealtimeData.fcgi".format(IP)
VERSION = "1.1"
CHANGE_LOG = "1.1 - Added source IP and Hostname to the json"

logger = logging.getLogger()


def find_my_ip() -> tuple:
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + ip_addr)
    return ip_addr, hostname


def list_environment():
    for k, v in os.environ.items():
        item = f'{k}={v}'
        print(item)
        logger.info(item)


def main():
    # list_environment()
    firehose = boto3.client('firehose', region_name='eu-west-1')
    source_ip, source_host = find_my_ip()

    while (True):
        print("\n\n\n ****************************")
        res = requests.request('GET', URL_POWER_FLOW)
        power_result = json.loads(res.content)
        solar_dict = {
            "timestamp": power_result['Head']['Timestamp'],
            "energy_day_wh": power_result['Body']['Data']['Site']['E_Day'],
            "energy_total_wh": power_result['Body']['Data']['Site']['E_Total'],
            "energy_year_wh": power_result['Body']['Data']['Site']['E_Year'],
            "current_power_wh": power_result['Body']['Data']['Site']['P_PV'],
            "source_ip": source_ip,
            "source_host": source_host
        }

        logger.info("Solar info: {}".format(solar_dict))
        print(solar_dict)
        fh_response = firehose.put_record(
            DeliveryStreamName='solceller',
            Record={
                "Data": json.dumps(solar_dict) + "\n"
            }
        )
        logger.info("Firehose Response: {}".format(fh_response))
        print("Firehose Response: {}".format(fh_response))
        sleep(60)


# async def main_old(loop, host):
#     async with aiohttp.ClientSession(loop=loop) as session:
#         fronius = pyfronius.Fronius(session, host)
#         session = boto3.session.Session(profile_name='fredrik_dev2')
#
#         # client = session.resource(service_name='firehose', region_name='eu-west-1')
#         firehose = boto3.client('firehose', region_name='eu-west-1')
#         kinesis = boto3.client('kinesis')
#         s3 = boto3.client('s3', region_name='eu-west-1')
#         print(s3.list_buckets())
#
#         while(True):
#             print("\n\n\n ****************************")
#             power_result = await fronius.current_power_flow()
#             print(power_result)
#             print("type of power_result: {} ".format(type(power_result)))
#
#             response = firehose.list_delivery_streams()
#             print("firehose: {}".format(response))
#
#
#             simlpe_dict = {
#                 "timestamp" : power_result['timestamp']['value'],
#                 "energy_day_wh" : power_result['energy_day']['value'],
#                 "energy_total_wh" : power_result['energy_total']['value'],
#                 "energy_year_wh" : power_result['energy_year']['value'],
#                 "current_power_w" : power_result['power_photovoltaics']['value']
#             }
#
#             response = firehose.put_record(
#                 DeliveryStreamName='solceller',
#                 Record={
#                     "Data": json.dumps(simlpe_dict) + "\n"
#                 }
#             )
#             print("put response: {}".format(response))
#             sleep(60)
#
#         # res = await fronius.current_system_meter_data()
#         # print(res)
#         # res = await fronius.current_meter_data()
#         # print(res)
#         # res = await fronius.current_storage_data()  // problem with json
#         # print(res)
#         # res = await fronius.current_inverter_data()
#         # print(res)
#         # res = await fronius.current_system_inverter_data()
#         # print(res)


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.DEBUG)
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main(loop, "http://192.168.1.68"))

main()
