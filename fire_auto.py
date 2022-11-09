import sys
import fire

for x in sys.stdin:
	url = x.strip()
	args, help_text = fire.parse_arguments()
	if args.command == "create":
		args.url = url
		fp = fire.FireProx(args, help_text)
		result = fp.create_api(fp.url)
		print(result)
	if args.command == "delete":
		args.url = url
		fp = fire.FireProx(args, help_text)
		results = fp.list_api()
		for result in results:
			api_url_generated = fp.get_integration(result['id']).replace('{proxy}','')
			if args.url == api_url_generated:
				fp.delete_api(result['id'])
	