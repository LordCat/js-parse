from tqdm import tqdm
import time, asyncio
from .fetch_and_extract_files import extract_files
from .utils import parse_domain
from .store_files import store_urls
from .args import argparser


args = argparser()
target_url = args.url

def process_files_with_tqdm():
    custom_bar_format = "[[\033[94m  {desc}\033[0m: [{n}/{total} {percentage:.0f}%] \033[31mCurrent:\033[0m [{elapsed}] \033[31mRemaining:\033[0m [{remaining}]  ]]"
    total_items = len(list(extract_files(target_url)))
    start_time = time.time()
    scope_list = args.scope
    for js_file in tqdm(extract_files(target_url), desc="Extracting", unit='URL', bar_format=custom_bar_format, total=total_items, position=4, dynamic_ncols=True, leave=False):
        # handles absolute urls that belong to target's domain
        if 'http' in js_file or 'https' in js_file:
            if (parse_domain(target_url) == parse_domain(js_file)):
                store_urls(js_file)
                tqdm.write("\033[32m[Extracted]\033[0m " + js_file)
            else:
                try:
                    True if [True if parse_domain(js_file) in scope else False for scope in scope_list].index(True) else False
                    store_urls(js_file)
                    tqdm.write("\033[32m[Extracted]\033[0m " + js_file)
                except:
                    tqdm.write("\033[33m[Skipped]\033[0m " + js_file)
        else:
            # handles both relative files and relative urls
            if (js_file[0] != "/"): 
                js_file = "/" + js_file
                tqdm.write("\033[32m[Extracted]\033[0m " + js_file)
                store_urls(target_url + js_file)
            else:
                tqdm.write("\033[32m[Extracted]\033[0m " + js_file)
                store_urls(target_url + js_file)
    print("")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("  \033[94m" + f"[COMPLETED]\033[0m {total_items} files in {elapsed_time:.2f} seconds")
 

def process_files_without_tqdm():
    scope_list = args.scope
    for js_file in extract_files(target_url):
        # handles absolute urls that belong to target's domain
        if 'http' in js_file or 'https' in js_file:
            if (parse_domain(target_url) == parse_domain(js_file)):
                store_urls(js_file)
            else:
                try:
                    True if [True if parse_domain(js_file) in scope else False for scope in scope_list].index(True) else False
                    store_urls(js_file)
                except:
                    pass
        else:
            # handles both relative files and relative urls
            if (js_file[0] != "/"): 
                js_file = "/" + js_file
                store_urls(target_url + js_file)
            else:
                store_urls(target_url + js_file)
