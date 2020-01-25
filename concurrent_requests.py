#!/usr/bin/python3

import sys
import time
import requests
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning

session = requests.Session()
session.verify = False

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def print_header():
    print('| url'.ljust(len(sys.argv[1])), '|\t','method', '|\t', 'status', '\t', 'response_time')
    print('-----------------------------------------------------------------------')

def print_footer():
    print('-----------------------------------------------------------------------')

def print_response(response):
    url = response.url
    status = response.status_code
    elapsed_time = response.elapsed.total_seconds()
    print('|', url, '|\t|','GET', '|\t\t|',  status, '|\t\t|', elapsed_time, '|')

def print_responses(responses):
    print_header()
    for response in responses:
       print_response(response) 
    print_footer()

def make_requests(number_of_threads):
    with Pool(number_of_threads) as pool:
        start_time = time.perf_counter()
        
        responses = pool.imap_unordered(session.get, urls)
        print_responses(responses)

        end_time = time.perf_counter() - start_time

    print('Total time elapsed: ', end_time)


if __name__ == '__main__':
    number_of_requests_to_make_per_thread = int(sys.argv[2])
    number_of_threads = int(sys.argv[3])
    
    urls = [sys.argv[1]] * number_of_requests_to_make_per_thread * number_of_threads
    print(len(urls))

    make_requests(number_of_threads)

