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
    parser.add_argument('-i', '--inventory', dest='inventory_file',
                        help='Please select a file in Yaml format')
    parser.add_argument('-f', '--fork', dest='fork', help='forks num',
                        type=int, default=5)
    parser.add_argument('-c', '--command', dest='command', help='command list')
    args = parser.parse_args()

    # TODO: inputの確認処理がない
    print("==== START ====")
    with open(args.inventory_file, 'r') as inventory_yml:
        configs = yaml.safe_load(inventory_yml)
        commands = list()
        with open(args.command, 'r') as commands_yml:
            command = yaml.safe_load(commands_yml)
            for i in range(0, len(configs)):
                commands.append(command[configs[i]['platform']])
            with concurrent.futures.ProcessPoolExecutor(max_workers=args.fork) as excuter:
                excuter.map(scrapli_core._run, configs, commands)
    print("==== END ====")

    end = timer()
    print("#"*70)
    print("# Time elapsed:", end - start)
    print("#"*70)


if __name__ == '__main__':
    main()
