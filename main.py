import time
from datetime import date
import os
from pathlib import Path
import json

import schedule

from configure import save_config, read_config


def run_spider(spider_name, **kwargs):
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    cmd = f'python -m scrapy crawl {spider_name} '
    args = [f'-a {k}={v}' for k, v in kwargs.items()]
    if args:
        cmd += ' '.join(args)
    print(f"Running '{spider_name}' spider [{cmd}]...")
    try:
        os.system(cmd)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("[ERROR]", e)
    print(f"Spider '{spider_name}' stopped!")


def run_spiders(spiders: list, **kwargs):
    for spider in spiders:
        run_spider(spider, **kwargs)


def get_spiders():
    with open('spiders.txt') as file:
        spiders = file.read().splitlines()
        return spiders


def main():
    spiders = get_spiders()
    last_parsed = config['last_parsed'] if not config['force_parse_all'] else None
    run_spiders(spiders, last_parsed=last_parsed)

    config['last_parsed'] = str(date.today())
    save_config(config)


if __name__ == '__main__':
    config = read_config()
    main()

    if config['every_what'] == 'hours':
        schedule.every(config['parse_every']).hours.do(main)
    elif config['every_what'] == 'minutes':
        schedule.every(config['parse_every']).minutes.do(main)
    elif config['every_what'] == 'seconds':
        schedule.every(config['parse_every']).seconds.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
