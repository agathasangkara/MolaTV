import requests as r
import json, random, string
import sys as s, os, threading
import subprocess
# from kivy.app import App
# from kivy.core.clipboard import Clipboard


client = r.Session()
base_url = "https://api2-mola.onwards.pro/v1"

# colours
green = "\033[0;32m"
white = "\033[0;37m"
red = "\033[0;31m"
yellow = "\033[0;33m"
cyan = "\033[0;36m"

def impor_config(red):
	if os.path.exists("config.json"):
		file = open("config.json", "r")
		data = json.load(file)
		return data
	else:
		os.system("touch config.json")
		print(f" {red}Write file config.json\n")
		exit

def sessionId():
    return '{:04x}{:04x}-{:04x}-{:04x}-{:04x}-{:04x}{:04x}{:04x}'.format(
        random.randint(0, 0xffff),
        random.randint(0, 0xffff),
        random.randint(0, 0xffff),
        random.randint(0, 0x0fff) | 0x4000,
        random.randint(0, 0x3fff) | 0x8000,
        random.randint(0, 0xffff),
        random.randint(0, 0xffff),
        random.randint(0, 0xffff)
    )

def create_tempmail():
	url = "https://mob2.temp-mail.org/mailbox"
	create = client.post(url, headers={'User-Agent': '3.13'})
	return create.json()
	
def send_otp(email, sandi, base_url, proxy):
	url = base_url + "/subscriber/send/otp"
	data = {"email":email,"lang":"en"}
	headers = {}
	headers['user-agent'] = 'Mola/2.2.6.10 (Android 10; UA43T6500AKXXD)'
	headers['x-mola-version'] = 'Mola/2.2.6.10 (Android 10; UA43T6500AKXXD)'
	headers['content-type'] = 'application/json; charset=UTF-8'
	return client.post(url, json=data, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=5)

def cek_otp(auth_email):
	url = "https://mob2.temp-mail.org/messages"
	headers = {}
	headers['User-Agent'] = '3.13'
	headers['Authorization'] = f'{auth_email}'
	return client.get(url, headers=headers)

def verifcation_otp(proxy, otp, email, sandi, base_url):
	url = base_url + "/subscriber/idToken/new"
	data = {"OTP":otp,"email":email,"password":sandi}
	headers = {}
	headers['user-agent'] = 'Mola/2.2.6.10 (Android 10; UA43T6500AKXXD)'
	headers['x-mola-version'] = 'Mola/2.2.6.10 (Android 10; UA43T6500AKXXD)'
	headers['content-type'] = 'application/json; charset=UTF-8'
	return client.post(url, json=data, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=5)

def signup_mola(proxy, idtoken, base_url):
	url = base_url + "/subscriber/register"
	data = {"idToken":idtoken,"isReceive":False}
	headers = {}
	headers['user-agent'] = 'Mola/2.2.6.10 (Android 10; UA43T6500AKXXD)'
	headers['x-mola-version'] = 'Mola/2.2.6.10 (Android 10; UA43T6500AKXXD)'
	headers['content-type'] = 'application/json; charset=UTF-8'
	return client.post(url, json=data, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=5)

def claim_bundling(idtoken_v2, adid, fid, serial, model, base_url):
	url = base_url + "/subscriber/login"
	data = {"advertisingId":adid,"appsflyerId":fid,"deviceId":serial,"deviceName":"samsung","deviceType":"Android","idToken":idtoken_v2,"modelNo":model,"serialNo":serial}
	headers = {}
	headers['user-agent'] = 'Mola/2.2.6.10 (Android 10; UA43T6500AKXXD)'
	headers['x-mola-version'] = 'Mola/2.2.6.10 (Android 10; UA43T6500AKXXD)'
	headers['content-type'] = 'application/json; charset=UTF-8'
	return client.post(url, json=data, headers=headers)

def cek_bundling(bearer, base_url):
	url = base_url + "/subscription/history"
	headers = {}
	headers['user-agent'] = 'Mola/2.2.6.10 (Android 10; UA43T6500AKXXD)'
	headers['x-mola-version'] = 'Mola/2.2.6.10 (Android 10; UA43T6500AKXXD)'
	headers['authorization'] = f'Bearer {bearer}'
	cek = client.get(url, headers=headers)
	return cek.json()

def change_profile(bearer, base_url):
	url = base_url + "/subscriber"
	data = {"birthday":"","displayImage":"","displayName":"Sangkara","gender":"m","location":"","mobileNumber":"","user_language":""}
	headers = {}
	headers['user-agent'] = 'Mola/2.2.6.10 (Android 10; UA43T6500AKXXD)'
	headers['x-mola-version'] = 'Mola/2.2.6.10 (Android 10; UA43T6500AKXXD)'
	headers['authorization'] = f'Bearer {bearer}'
	headers['content-type'] = 'application/json; charset=UTF-8'
	return client.patch(url, headers=headers, json=data)

def generate_code(serial, model):
    url = base_url + "/tv/activate/getcode"
    data = {"deviceId":serial,"deviceName":"samsung","deviceType":"AndroidTV","modelNo":model,"serialNo":serial}
    headers = {}
    headers['user-agent'] = 'Mola/2.0.2.13 (AndroidTV 10; xiaomi Redmi Note 8)'
    headers['x-mola-version'] = 'Mola/2.0.2.13 (AndroidTV 10; xiaomi Redmi Note 8)'
    headers['content-type'] = 'application/json; charset=UTF-8'
    rg = client.post(url, headers=headers, json=data, timeout=10)
    code = rg.json()
    return code['activationCode']

def checking_code(code):
    url = base_url + "/tv/activate/checkcode"
    data = {"activationCode":code}
    headers = {}
    headers['user-agent'] = 'Mola/2.0.2.13 (AndroidTV 10; xiaomi Redmi Note 8)'
    headers['x-mola-version'] = 'Mola/2.0.2.13 (AndroidTV 10; xiaomi Redmi Note 8)'
    headers['content-type'] = 'application/json; charset=UTF-8'
    return client.post(url, headers=headers, json=data, timeout=10)
    
    
def get_proxy(method):
	print(f'\n {yellow} Scrape Proxy {method} Diproccess ...\n')
	for i in range(2):
		subprocess.run(["python3", "scrap.py", "-p", method])

def run_task(proxy, red, green, white):
	try:
		load = impor_config(red)
		sandi = load['MolaTV']['Password']
		model = load['MolaTV']['Model']
		get_email = create_tempmail()
		auth_email = get_email['token']
		email = get_email['mailbox']
		
		send = send_otp(email, sandi, base_url, proxy)
		if send.status_code == 200:
			None
		elif send.status_code == 400:
			res = send.json()
			err = res['message']
			s.exit(f'\n {red}{err}')
		else:
			s.exit(f'\n Code : {send.status_code} Reason {send.json()}')
		
		while True:
			cek = cek_otp(auth_email)
			cek_text = cek.text
			if "MOLA" in cek_text:
				cek_json = cek.json()
				preview = cek_json['messages'][0]['subject']
				otp = preview[:6]
				break
			else:
				continue
			
		verif = verifcation_otp(proxy, otp, email, sandi, base_url)
		while True:
			if verif.status_code == 200:
				get_id = verif.json()
				idtoken = get_id['idToken']
				break
			elif verif.status_code == 429:
				s.exit(f' [{proxy}] : {red} Proxy 429 Too many request')
				break
			else:
				continue
		
		reg = signup_mola(proxy, idtoken, base_url)
		while True:
			if reg.status_code == 200:
				id_v2 = verif.json()
				idtoken_v2 = id_v2['idToken']
				break
			else:
				continue
		
		serial = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(16))
		fid = sessionId()
		adid = sessionId()
		login = claim_bundling(idtoken_v2, adid, fid, serial, model, base_url)
		while True:
			if login.status_code == 201:
				login_json = login.json()
				bearer = login_json['accessToken']['accessToken']
				# print(f' [{email}] : {white}Redeem Bundling Success{white}')
				break
			else:
				print(f' Code claim : {login.status_code}')
				continue
		
		cek_paket = cek_bundling(bearer, base_url)
		if cek_paket['total'] == 1:
			pkg = cek_paket['results'][0]['packageName']
			print(f'  {email} | {green}{pkg}{white}')
			with open('molatv.txt', 'a') as f:
				f.write(f'{email} || {sandi}\n')
		elif cek_paket['total'] == 0:
			s.exit(f'  {email} : {red}Promo failed applied{white}')
		else:
			s.exit(f'  {red} Something went wrong\n\n')
		
		change = change_profile(bearer, base_url)
		if change.status_code == 200:
			None

	except Exception as e:
		None

def mass_create(white, red, green):
    tanya = input(f'\n {white} Scrape Proxy [y/N] ? : ')
    if tanya == "y":
        print(f'\n {white} 1. HTTP\n  2. HTTPS')
        data_method = input(f'\n {white} Type Proxy : {yellow}')
        if data_method == "1":
            method = "http"
        elif data_method == "2":
            method = "https"
        else:
            s.exit(f'\n {red} Wrong type proxy\n\n')
    else:
        print(f'\n {red} Without scrape proxy\n')

    while True:
        if tanya == "y":
            get_prx = get_proxy(method)
            break
        else:
            get_prx = None
            break

    try:
        with open('proxy.txt', 'r') as file:
            proxies = file.read().splitlines()
            file.close()

            if not proxies:
                raise ValueError(" Proxies is empty. scrape first")

    except FileNotFoundError:
        os.system("touch proxy.txt")
        subprocess.call('python main.py', shell=True)

    except ValueError as e:
        s.exit(f' {white}{e}\n')

    amount = input(f' {white} Thread : ')
    if int(amount) > 20:
        s.exit(f'\n {red} Sebaiknya jangan gegabah terlalu banyak\n')

    print(f'\n {yellow} Threading {amount}x sedang diproses ... {white}\n')

    threads = []
    for _ in range(int(amount)):
        for proxy in proxies:
            thread = threading.Thread(target=run_task, args=(proxy, red, green, white,))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    print(f' {cyan} All proxies have been checked\n')
    subprocess.run(["rm", "-rf", "proxy.txt"])
    
def generate_aktivasi(white, red, green):
	load = impor_config(red)
	model = load['MolaTV']['Model']
	serial = sessionId()
	code = generate_code(serial, model)
	print(f'  {white}Redeemed this activation code : {green}{code} ')
	
	while True:
		cek = checking_code(code)
		cek_usr = cek.text
		if "accessToken" in cek_usr:
			cek_js = cek.json()
			email = cek_js['email']
			print(f'\n  {white}Code {yellow}{code}{white} redeem by {green}{email}{white}\n')
			break
		else:
			continue
			
def thread_code(i):
	try:
		generate_aktivasi(white, red, green)
		pass
	except Exception as e:
		None

def run_thread(red, yellow, white):
    amount = input(f'\n {white} Jumlah code : ')
    if int(amount) > 20:
        s.exit(f'\n {red} Sebaiknya jangan gegabah terlalu banyak\n')
    
    print(f'\n {yellow} Code {amount}x sedang diproses ... {white}\n')
    
    threads = []
    for i in range(int(amount)):
        t = threading.Thread(target=thread_code, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

os.system('cls' if os.name == "nt" else 'clear')
print(f"{cyan}\n  .-.            .;      .-.;;;;;;'          \n         .;|/:        .;'     (_)  .;.;.       .-. \n        .;   : .-.   .;  .-.       :  `;     .'    \n       .;    :;   ;'::  ;   :    .:'   ;;  .'      \n   .:'.;     :`;;'_;;_.-`:::'-'.-:._  ;;  ;        \n  (__.'      `.               (_/  `- `;.'\n")
print(f'\n {white} Mola TV Mass create (proxy) - Agathasangkara')
print(f'\n  1. {red}Create Unlimited Account Mola TV\n {white} 2. {red}Generate Code Activation{white}\n')

opsi = input(f'  Choose : {yellow}')
if opsi == "1":
	mass_create(white, red, green)
elif opsi == "2":
	run_thread(red, yellow, white)
else:
	s.exit(f'\n  {red}Your choice wrong, input again\n\n')
