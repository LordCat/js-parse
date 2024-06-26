import os, re, asyncio, json, jsbeautifier
from .args import argparser
from .fetch_and_extract_files import extract_urls
from .utils import(
    remove_dupes,
    clean_urls
    )
from .http_probe import filter_urls
from .shared import(
    all_dirs,
    target,
    dict_report
    )
args = argparser()


def store_urls(url):
    try:
        target["domain"], file_name = re.search("(?:[a-zA-Z0-9-](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9-])?\.)+[a-zA-Z]{2,}", url).group(0), re.search("([^/]*\.js)", url).group(0)
        parsed_js_directory_path = f"""{target["domain"]}/parsed-urls/"""
        parsed_files_directory_path = f"""{target["domain"]}/parsed-files/"""

        if (args.isolate or args.merge):
            try:
                os.makedirs(parsed_js_directory_path)
            except FileExistsError:
                pass
            if(args.save):
                os.mkdir(parsed_files_directory_path)

    except FileExistsError:
        pass
    except AttributeError:
        pass

    extracted_urls = extract_urls(url)
    num_urls = len(extracted_urls)
    i = 0
    for quoted_dir in extracted_urls:
        i += 1

    extracted_urls = extract_urls(url)
    num_urls = len(extracted_urls)
    i = 0
    for quoted_dir in extracted_urls:
        i += 1
        try:
            if (args.isolate):
                dir = quoted_dir.strip('"')
                with open(f"""{target["domain"]}/parsed-urls/{file_name}+dirs.txt""", "a", encoding="utf-8") as directories:
                    if i == num_urls:
                        directories.write(dir + '\n')  # No comma for the last directory
                    else:
                        directories.write(dir + ',\n')
                    if i == num_urls:
                        directories.write(dir + '\n')  # No comma for the last directory
                    else:
                        directories.write(dir + ',\n')
            elif (args.merge):
                dir = quoted_dir.strip('"')
                all_dirs.append(dir)  # No comma for the last directory
            else:
                dir = quoted_dir.strip('"')
                all_dirs.append(dir)
        finally:
             if(args.save):
                parsed_files_directory_path = f"""{target["domain"]}/parsed-files/"""
                if not (os.path.exists(parsed_files_directory_path)):
                    os.makedirs(parsed_files_directory_path)
def write_files():
    i = 0
    remove_dupes(all_dirs)
    if (args.remove_third_parties):
        if (args.filter and args.stdout):
            asyncio.run(filter_urls())
        elif (args.json_report and not args.filter):
            print("must have -f (filter) option with json_report option")
        elif (args.filter):
            asyncio.run(filter_urls())
        else:
            print("must have -f (filter) option with --remove-third-parties")
            quit()
    elif (args.json_report and not args.filter):
            print("must have -f (filter) option with json_report option")
    elif (args.filter and args.stdout):
            asyncio.run(filter_urls())
    elif (args.filter):
        asyncio.run(filter_urls())
    if not (args.json_report):
        with open(f"""{target["domain"]}/parsed-urls/all_urls.txt""", "w", encoding="utf-8") as directories:
            directories.write('')
        with open(f"""{target["domain"]}/parsed-urls/all_urls.txt""", "a", encoding="utf-8") as directories:
            print()
            for unique_dir in all_dirs:
                i += 1
                if (i == len(all_dirs)):
                    directories.write(clean_urls(unique_dir) + '\n')
                else:
                    directories.write(clean_urls(unique_dir) + ',\n')
    if (args.json_report):
        json_report = json.dumps(dict_report)
        beautified_json_report = jsbeautifier.beautify(str(json_report))
        with open(f"""{target["domain"]}/parsed-urls/url_report.json""", "w", encoding="utf-8") as directories:
            directories.write(beautified_json_report)