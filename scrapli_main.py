###############################################################################
# python scrapli_main.py -i file/scrapli_auth.yml -f 10
###############################################################################
import argparse
import yaml
import concurrent.futures

import scrapli_core

from timeit import default_timer as timer

def main():
    start = timer()
    parser = argparse.ArgumentParser(prog='SSH Tool')
    parser.add_argument('-i','--inventory', dest='inventory_file', help='Please select a file in Yaml format')
    parser.add_argument('-f','--fork', dest='fork', help='forks num', type=int, default=5)
    args = parser.parse_args()

    print(f"==== START ====")
    with open(args.inventory_file, 'r') as yml:
        configs = yaml.safe_load(yml)
        with concurrent.futures.ProcessPoolExecutor(max_workers=args.fork) as excuter:
            excuter.map(scrapli_core._run, configs)
    print(f"==== END ====")

    end = timer()
    print("#"*70)
    print("# Time elapsed:", end - start)
    print("#"*70)


if __name__ == '__main__':
    main()
