#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Explanation: An importer of Crowdstrike information using the SQS queue
Usage:
    $ python  csimport [ options ]
Style:
    Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html
    @name           csimport
    @version        1.0.0
    @author-name    Wayne Schmidt
    @author-email   wschmidt@sumologic.com
    @license-name   GNU GPL
    @license-url    http://www.gnu.org/licenses/gpl.html
"""

__version__ = 1.0
__author__ = "Wayne Schmidt (wschmidt@sumologic.com)"

import argparse
import json
import time
import os
import sys
import configparser
import boto3

sys.dont_write_bytecode = 1

PARSER = argparse.ArgumentParser(description="""
This is a launcher for an AWS SQS queue consumer
""")

PARSER.add_argument('-q', metavar='<awsqueue>', dest='awsqueue', help='specify AWS SQS queue')
PARSER.add_argument('-k', metavar='<awskey>', dest='awskey', help='specify AWS key')
PARSER.add_argument('-s', metavar='<awssecret>', dest='awssecret', help='specify AWS secret')
PARSER.add_argument('-r', metavar='<awsregion>', dest='awsregion', help='specify AWS region')
PARSER.add_argument('-o', metavar='<outputpath>', dest='outputpath', help='specify output')
PARSER.add_argument('-t', metavar='<timeout>', dest='timeout', help='specify timeout')
PARSER.add_argument('-c', metavar='<cfgfile>', dest='cfgfile', help='specify config file')

ARGS = PARSER.parse_args()

BINDIR = os.path.dirname(os.path.abspath(__file__))
CFGDIR = os.path.abspath(BINDIR.replace('bin', 'etc'))

if ARGS.awskey:
    os.environ["AWSKEY"] = ARGS.awskey
if ARGS.awssecret:
    os.environ["AWSSECRET"] = ARGS.awssecret
if ARGS.awsqueue:
    os.environ["AWSQUEUE"] = ARGS.awsqueue
if ARGS.outputpath:
    os.environ["OUTPUTPATH"] = ARGS.outputpath
if ARGS.timeout:
    os.environ["TIMEOUT"] = ARGS.timeout
if ARGS.awsregion:
    os.environ["AWSREGION"] = ARGS.awsregion

if ARGS.cfgfile:
    CONFIG = configparser.ConfigParser()
    CFGFILE = os.path.abspath(ARGS.cfgfile)
    if os.path.exists(CFGFILE):
        CONFIG.read(CFGFILE)
        if CONFIG['DEFAULT']['AWSKEY']:
            os.environ["AWSKEY"] = CONFIG['DEFAULT']['AWSKEY']
        if CONFIG['DEFAULT']['AWSSECRET']:
            os.environ["AWSSECRET"] = CONFIG['DEFAULT']['AWSSECRET']
        if CONFIG['DEFAULT']['AWSQUEUE']:
            os.environ["AWSQUEUE"] = CONFIG['DEFAULT']['AWSQUEUE']
        if CONFIG['DEFAULT']['OUTPUTPATH']:
            os.environ["OUTPUTPATH"] = CONFIG['DEFAULT']['OUTPUTPATH']
        if CONFIG['DEFAULT']['TIMEOUT']:
            os.environ["TIMEOUT"] = CONFIG['DEFAULT']['TIMEOUT']
        if CONFIG['DEFAULT']['AWSREGION']:
            os.environ["AWSREGION"] = CONFIG['DEFAULT']['AWSREGION']
try:
    AWSKEY = os.environ["AWSKEY"]
    AWSSECRET = os.environ["AWSSECRET"]
    AWSQUEUE = os.environ["AWSQUEUE"]
    AWSREGION = os.environ["AWSREGION"]
    OUTPUTPATH = os.environ["OUTPUTPATH"]
    TIMEOUT = os.environ["TIMEOUT"]
except KeyError as myerror:
    print('Environment Variable Not Set :: {} '.format(myerror.args[0]))

S3_ARN = boto3.client('s3', region_name=AWSREGION, aws_access_key_id=AWSKEY, \
    aws_secret_access_key=AWSSECRET)

SQS_ARN = boto3.resource('sqs', region_name=AWSREGION, aws_access_key_id=AWSKEY, \
    aws_secret_access_key=AWSSECRET)

def handle_file(path):
    """
    Custom logic for handling files
    """
    print("Handling File" % path)

def download_message_files(msg):
    """
    Downloads the files from s3 referenced in msg and places them in OUTPUT_PATH.
    download_message_files function will iterate through every file listed at msg['filePaths'],
    move it to a local path with name "{OUTPUT_PATH}/{s3_path}",
    and then call handle_file(path).
    """
    msg_output_path = os.path.join(os.path.abspath(OUTPUTPATH, msg['pathPrefix']))
    if not os.path.exists(msg_output_path):
        os.makedirs(msg_output_path)
    for s3_file in msg['files']:
        s3_path = s3_file['path']
        local_path = os.path.join(OUTPUTPATH, s3_path)
        print("Your AWS Bucket: " + msg['bucket'])
        print("Your AWS Path: " + s3_path)
        S3_ARN.download_file(msg['bucket'], s3_path, local_path)
        handle_file(local_path)

def consume_data_replicator():
    """
    Consume from data replicator and track number of messages/files/bytes downloaded.
    """

    sleep_time = 1
    msg_cnt = 0
    file_cnt = 0
    byte_cnt = 0

    queue = SQS_ARN.Queue(url=AWSQUEUE)

    while True:
        # We want to continuously poll the queue for new messages.
        # Receive messages from queue if any exist
        # (NOTE: receive_messages() only receives a few messages
        #        at a time, it does NOT exhaust the queue)
        for msg in queue.receive_messages(VisibilityTimeout=TIMEOUT):
            msg_cnt += 1
            # grab the actual message body
            body = json.loads(msg.body)
            download_message_files(body)
            file_cnt += body['fileCount']
            byte_cnt += body['totalSize']
            # msg.delete() must be called or the message will be
            # returned to the SQS queue after TIMEOUT seconds
            msg.delete()
            time.sleep(sleep_time)
        print("Messages: %i\tFiles: %i\tBytes: %i" % (msg_cnt, file_cnt, byte_cnt))

def main():
    """
    This is a wrapper function for the main logic in the program
    """
    consume_data_replicator()

if __name__ == '__main__':
    main()
