import requests
import os
import subprocess
import threading
import json
import time
import argparse


proxies = {"http": "socks5://127.0.0.1:10808", "https": "socks5://127.0.0.1:10808"}


def run_xray(config_file):
    global process
    try:
        command = ['./xray' , '-c' , config_file]
        process = subprocess.Popen(command , shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()
        print('X-ray ran successfully')
    except subprocess.CalledProcessError as e:
        print(e)
    except FileNotFoundError:
        print('X-ray binary not found')
    event.set()
    return process


def replace_fragment_in_config(config_file, fragment_value):
    with open(config_file, 'r') as f:
        config_data = json.load(f)

    
    config_data['outbounds'][1]['settings']['fragment']["interval"] = fragment_value

    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)

def replace_length_in_config(config_file, length_value):
    with open(config_file, 'r') as f:
        config_data = json.load(f)

    
    config_data['outbounds'][1]['settings']['fragment']["length"] = length_value

    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)

def expand_ip_range(ip_range):
    ip_network = ipaddress.ip_network(ip_range)
    return [str(ip) for ip in ip_network.hosts()]
def print_red(text):
    print("\033[91m" + text + "\033[0m")  


def get_speed():
    
    s = speedtest.Speedtest(secure=True)
    s.get_best_server()
    s.upload()
    results_dict = s.results.dict()
    return results_dict['upload']

def convert_speed():
    n = get_speed()
    bytes_ps = n / 8
    mb_ps = bytes_ps / (1024 * 1024)
    round_mb_ps = round(mb_ps, 2)
    return round_mb_ps

def upload_speed_test(file_size_kb=1024):
    
    file_size_bytes = file_size_kb * 1024
    
    
    data = b'0' * file_size_bytes
    
    
    start_time = time.time()
    
    
    try:
        response = requests.post('https://speed.cloudflare.com/__up', data=data)
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        return None
    
    
    elapsed_time = time.time() - start_time
    
    
    upload_speed_mbps = (file_size_bytes * 8) / (elapsed_time * 1000000) / 8
    
    return upload_speed_mbps

def download_speed_test(file_size_kb=1024):
    
    file_size_bytes = file_size_kb * 1024
    
    
    data = b'0' * file_size_bytes
    
    
    start_time = time.time()
    
    
    try:
        response = requests.get('https://speed.cloudflare.com/__down', data=data)
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        return None
    
    
    elapsed_time = time.time() - start_time
    
    
    download_speed_mbps = (file_size_bytes * 8) / (elapsed_time * 1000000) / 8
    
    return download_speed_mbps

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fragment Checker with Speed Tests')
    parser.add_argument('--speedtest', action='store_true', help='Run Speedtest speed test')
    parser.add_argument('--download', action='store_true', help='Run cloudflare download test')
    parser.add_argument('--filesize', type=int, help='Specify the file size in MB for speed tests')
    parser.add_argument('--grpc', action='store_true', help='Run grpc config for test')
    parser.add_argument('--length', action='store_true', help='Change the length while testing')



    args = parser.parse_args()


    if args.grpc:
        config_file = "config.json"
    else:
        config_file = "configws.json"
    fragment_file="fragment.txt"
    event = threading.Event()

    
    with open(fragment_file, 'r') as f:
        fragment_values = f.read().splitlines()


    if args.length:
        length_file = "length.txt"
        with open(length_file, 'r') as f:
            length_values = f.read().splitlines()
        for fragment_value in fragment_values:
            replace_fragment_in_config(config_file, fragment_value)

            for length_value in length_values:
                replace_length_in_config(config_file , length_value)
                print_red(fragment_value)
                print_red(length_value)

                
                xray_thread = threading.Thread(target=run_xray, args=(config_file,))
                xray_thread.start()
                event.wait(1)
                
                file_size_kb = args.filesize *1024 if args.filesize is not None else 5120        
                
                
                print("Performing Cloudflare upload speed test...")
                upload_speed = upload_speed_test(file_size_kb)
                
                if upload_speed is not None:
                    print(f"Cloudflare Upload Speed: {upload_speed:.2f} Mbps")
                else:
                    print("Cloudflare Upload speed test failed.")
                
                if args.download:
                    print("Performing Cloudflare download speed test...")
                    download_speed = download_speed_test(file_size_kb)
                    
                    if download_speed is not None:
                        print(f"Cloudflare Download Speed: {download_speed:.2f} Mbps")
                    else:
                        print("Cloudflare Download speed test failed.")
                
                if args.speedtest:
                    print("Performing Speedtest speed test...")
                    print(f"Speedtest Result: {convert_speed()}")

                xray_thread.join(timeout=1)

    else:
        for fragment_value in fragment_values:
            replace_fragment_in_config(config_file, fragment_value)
            print_red(fragment_value)

            
            xray_thread = threading.Thread(target=run_xray, args=(config_file,))
            xray_thread.start()
            event.wait(1)
            
            file_size_kb = args.filesize *1024 if args.filesize is not None else 5120        
            
            
            print("Performing Cloudflare upload speed test...")
            upload_speed = upload_speed_test(file_size_kb)
            
            if upload_speed is not None:
                print(f"Cloudflare Upload Speed: {upload_speed:.2f} Mbps")
            else:
                print("Cloudflare Upload speed test failed.")
            
            if args.download:
                print("Performing Cloudflare download speed test...")
                download_speed = download_speed_test(file_size_kb)
                
                if download_speed is not None:
                    print(f"Cloudflare Download Speed: {download_speed:.2f} Mbps")
                else:
                    print("Cloudflare Download speed test failed.")
            
            if args.speedtest:
                print("Performing Speedtest speed test...")
                print(f"Speedtest Result: {convert_speed()}")

            xray_thread.join(timeout=1)
