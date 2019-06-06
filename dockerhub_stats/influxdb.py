#!/usr/bin/env python3
'''InfluxDB exporter for dockerhub_stats'''

from influxdb import InfluxDBClient

class InfluxDBWriter():
    '''handles writing to InfluxDB'''
    def __init__(self, address, port=8086, database='dockerhub'):
        self.influx = InfluxDBClient(host=address, port=port, database=database)

    @staticmethod
    def _repo2point(repo_name, repo_data, timestamp):
        '''convert a Docker Hub repository data to an InfluxDB data point'''
        point = {'measurement': 'repositories',
                 'time': timestamp,
                 'tags': {
                     'user': str(repo_data['user']),
                     'name': str(repo_data['name']),
                     'repository': str(repo_name),
                 },
                 'fields': {
                     'pull_count': int(repo_data['pull_count']),
                     'star_count': int(repo_data['star_count']),
                 },
                }
        return point

    def export(self, data, timestamp):
        '''export data to InfluxDB'''
        influx_data = []
        for repo in data.keys():
            point = self._repo2point(repo, data[repo], timestamp)
            influx_data.append(point)
        self.influx.write_points(influx_data)
