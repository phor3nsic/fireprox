#!/usr/bin/env python3

import sys
import os
import random
import string
import subprocess
import json
import fire
from time import sleep
from itertools import islice
from concurrent.futures import ThreadPoolExecutor

def get_random_string():
	length = 6
	letters = string.ascii_lowercase
	result_str = ''.join(random.choice(letters) for i in range(length))
	return result_str

def run(func, targets):
	with ThreadPoolExecutor() as executor:
			executor.map(func, targets, timeout=10)

def save(text, output):
	with open(output, 'a+') as f:
		f.write(text)

def delete_used_apis():
	with open(args.output) as f:
		lines = f.readlines()
		for line in lines:
			data = json.loads(line.strip())
			fp.delete_api(data['id'])

def parser_output(api_id, url):
	with open(f"/tmp/{index_file}fireproxy.outputtemp.txt") as f:
		lines = f.readlines()
		proxy_url = f"https://{api_id}.execute-api.{args.region}.amazonaws.com/fireprox/"
		for line in lines:
			line = line.replace(proxy_url,url)
			print(line.replace('\n',''))
			save(line, args.output)

def shell(url):
	fp.url = url
	cmd = args.shell
	result = fp.create_api(url)
	cmd = cmd.replace("URL",result['proxy_url'])
	cmd = cmd.replace("OUTPUT",f"/tmp/{index_file}fireproxy.outputtemp.txt")
	try:
		proc = subprocess.Popen(cmd, shell=True)
		stdout, stderr = proc.communicate()
		fp.delete_api(result['id'])
		if "outputtemp" in cmd:
			parser_output(result['id'],fp.url)
	except KeyboardInterrupt:
		proc.kill()
		fp.delete_api(result['id'])
		sys.exit()

def generate(url):
	fp.url = url
	result = fp.create_api(fp.url)
	os.system(f'echo {result["proxy_url"]}') # more fast stdout (independent)
	save(f'{json.dumps(result)}\n',args.output)

def chunck(it, size):
	it = iter(it)
	return iter(lambda: tuple(islice(it, size)), ())

def main():
	all_list = []
	bulk_size = []

	if args.command == 'delete':
		delete_used_apis()
	
	if args.command == 'shell':
		print("SHELL MODE")
		print(f"[i] Running: {args.shell}")
		shell(args.url)
		
"""		
		for x in sys.stdin:
			url = x.strip()
			all_list.append(url)
		
		#if len(all_list) > 25:
		for bulk in list(chunck(all_list,3)):
			bulk_size = bulk
			run(shell, bulk_size)
			sleep(1)
		#else:
		#	for x in all_list:
		#		generate(x)
"""
if __name__ == '__main__':
	args, help_text = fire.parse_arguments()
	args.access_key = os.environ['AWS_ACCESS_KEY']
	args.secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
	args.region = os.environ['AWS_REGION']
	if args.output == None:
		args.output = 'log.json' 
	fp = fire.FireProx(args, help_text)
	index_file = get_random_string()
	main()
