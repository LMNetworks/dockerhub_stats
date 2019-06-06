#!/usr/bin/env python3
'''Command Line Interface for dockerhub_stats'''

import argparse
import sys
from datetime import datetime


from . import __description__, __version__
from .dockerhub import DockerHub

class DockerhubStats():
    '''main application class'''
    def __init__(self, repositories):
        self.hub = DockerHub()
        self.data = None
        self.last_update = None
        self.repositories = repositories

    def _fetch_data(self):
        '''fetch data from Docker Hub API'''
        if self.data is None:
            self.data = {}
            self.last_update = datetime.now()
            for org, repo in self.repositories:
                if repo is None:
                    self.data.update(self.hub.get_repository_list(org))
                else:
                    self.data.update(self.hub.get_repository_stats(org, repo))
        return self.data

    def export_influxdb(self, host, port=8086, database='dockerhub'):
        '''export data to InfluxDB'''
        self._fetch_data()
        from .influxdb import InfluxDBWriter
        influx = InfluxDBWriter(host, port, database)
        influx.export(self.data, self.last_update)

    def pretty_print(self, sortby):
        '''pretty print a table with repositories data to standard output'''
        self._fetch_data()
        from prettytable import PrettyTable
        pretty_columns = ['repository name', 'description', 'star count', 'pull count',
                          'last update']
        pretty = PrettyTable(pretty_columns)
        pretty.align["repository name"] = "l"
        pretty.align["description"] = "l"
        pretty.align["star count"] = "r"
        pretty.align["pull count"] = "r"
        pretty.align["last update"] = "l"
        pretty.padding_width = 1
        for repo in self.data:
            data = self.data[repo]
            pretty.add_row([repo,
                            data['description'],
                            data['star_count'],
                            data['pull_count'],
                            data['last_updated']])
        sortreverse = sortby in ['pulls', 'stars']
        sortby = {'name': 'repository name',
                  'pulls': 'pull count',
                  'stars': 'star count'}[sortby]
        print(pretty.get_string(sortby=sortby, reversesort=sortreverse))

# ###################################### CLI

def parse_arguments(args):
    '''parse command line arguments'''
    parser = argparse.ArgumentParser(description=__description__) #, prog='dockerhub_stats')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='do not print results on stdout')
    parser.add_argument('-s', '--sort', choices=['name', 'pulls', 'stars'], default='name',
                        help='table sort order')
    parser.add_argument('-v', '--version', action='version',
                        version=f'dockerhub_stats {__version__}')
    parser.add_argument('--influxhost', help='InfluxDB host')
    parser.add_argument('--influxport', help='InfluxDB port', type=int, default=8086)
    parser.add_argument('--influxdatabase', help='InfluxDB database', type=str, default='dockerhub')
    parser.add_argument('repositories', metavar='REPO', type=str, nargs='+',
                        help='repository names')
    args = parser.parse_args()
    return args

def cli():
    '''CLI entry point'''
    args = parse_arguments(sys.argv)

    # collect list of repositories
    repos = []
    for hub_ref in args.repositories:
        if '/' not in hub_ref:
            organization = hub_ref
            reponame = None
        else:
            organization, reponame = hub_ref.split('/')
        repos.append((organization, reponame))

    dhs = DockerhubStats(repos)

    if not args.quiet:
        dhs.pretty_print(args.sort)

    if args.influxhost is not None:
        dhs.export_influxdb(args.influxhost,
                            args.influxport,
                            args.influxdatabase)

# note: when installed using setuptools the entry point will be cli() above!
if __name__ == '__main__':
    cli()
