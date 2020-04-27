"""Basic usage example and testing of pyfronius."""
import asyncio
import json
import logging
import os

import aiohttp

import pyfronius
import boto3

# os.environ["AWS_REGION"] = "eu-west-1"
# os.environ["AWS_ACCESS_KEY_ID"] = ""
# os.environ["AWS_SECRET_ACCESS_KEY"] = ""
# os.environ["AWS_SESSION_TOKEN"] = ""



async def main(loop, host):
    async with aiohttp.ClientSession(loop=loop) as session:
        fronius = pyfronius.Fronius(session, host)
        session = boto3.session.Session(profile_name='')

        # client = session.resource(service_name='firehose', region_name='eu-west-1')
        firehose = boto3.client('firehose', region_name='eu-west-1')
        kinesis = boto3.client('kinesis')
        s3 = boto3.client('s3', region_name='eu-west-1')
        print(s3.list_buckets())

        # while(True):
        print("\n\n\n ****************************")
        power_result = await fronius.current_power_flow()
        print(power_result)
        print("type of power_result: {} ".format(type(power_result)))


        response = firehose.list_delivery_streams()
        print("firehose: {}".format(response))

        response = firehose.put_record(
            DeliveryStreamName='solceller',
            Record={
                "Data": json.dumps(power_result)
            }
        )
        print("put response: {}".format(response))

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


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, "http://192.168.1.68"))