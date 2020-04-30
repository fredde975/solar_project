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

# os.environ["AWS_REGION"] = "eu-west-1"
os.environ["AWS_ACCESS_KEY_ID"] = ""
os.environ["AWS_SECRET_ACCESS_KEY"] = ""
# os.environ["AWS_SESSION_TOKEN"] = ""

IP = "192.168.1.68"
URL_POWER_FLOW = "http://{}/solar_api/v1/GetPowerFlowRealtimeData.fcgi".format(IP)

# http://192.168.1.68/solar_api/v1/GetPowerFlowRealtimeData.fcgi

def main2(host:str):
    firehose = boto3.client('firehose', region_name='eu-west-1')

    while(True):
        print("\n\n\n ****************************")
        res = requests.request('GET', URL_POWER_FLOW)
        power_result = json.loads(res.content)
        simlpe_dict = {
            "timestamp" : power_result['Head']['Timestamp'],
            "energy_day_wh" : power_result['Body']['Data']['Site']['E_Day'],
            "energy_total_wh" : power_result['Body']['Data']['Site']['E_Total'],
            "energy_year_wh" : power_result['Body']['Data']['Site']['E_Year'],
            "current_power_wh" : power_result['Body']['Data']['Site']['P_PV'],
        }

        print(simlpe_dict)
        fh_response = firehose.put_record(
            DeliveryStreamName='solceller',
            Record={
                "Data": json.dumps(simlpe_dict) + "\n"
            }
        )
        print("Firehose Response: {}".format(fh_response))
        sleep(60)


async def main(loop, host):
    async with aiohttp.ClientSession(loop=loop) as session:
        fronius = pyfronius.Fronius(session, host)
        session = boto3.session.Session(profile_name='fredrik_dev2')

        # client = session.resource(service_name='firehose', region_name='eu-west-1')
        firehose = boto3.client('firehose', region_name='eu-west-1')
        kinesis = boto3.client('kinesis')
        s3 = boto3.client('s3', region_name='eu-west-1')
        print(s3.list_buckets())

        while(True):
            print("\n\n\n ****************************")
            power_result = await fronius.current_power_flow()
            print(power_result)
            print("type of power_result: {} ".format(type(power_result)))

            response = firehose.list_delivery_streams()
            print("firehose: {}".format(response))
            simlpe_dict = {
                "timestamp" : power_result['timestamp']['value'],
                "energy_day_wh" : power_result['energy_day']['value'],
                "energy_total_wh" : power_result['energy_total']['value'],
                "energy_year_wh" : power_result['energy_year']['value'],
                "current_power_wh" : power_result['power_photovoltaics']['value']
            }

            response = firehose.put_record(
                DeliveryStreamName='solceller',
                Record={
                    "Data": json.dumps(simlpe_dict) + "\n"
                }
            )
            print("put response: {}".format(response))
            sleep(60)

        # res = await fronius.current_system_meter_data()
        # print(res)
        # res = await fronius.current_meter_data()
        # print(res)
        # res = await fronius.current_storage_data()  // problem with json
        # print(res)
        # res = await fronius.current_inverter_data()
        # print(res)
        # res = await fronius.current_system_inverter_data()
        # print(res)


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.DEBUG)
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main(loop, "http://192.168.1.68"))

main2(host="192.168.1.68")