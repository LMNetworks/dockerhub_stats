#!/usr/bin/env python3
'''Docker Hub API client for dockerhub_stats'''

import json
from datetime import datetime
from urllib.request import urlopen

class DockerHub():
    '''interface to Docker Hub API'''
    _base_url = 'https://hub.docker.com/v2/repositories'

    @staticmethod
    def _parse_repo_data(repo_data):
        '''extract repository data from Docker Hub API response and format to our liking'''
        if repo_data['user'] != 'library':
            repo_name = f"{repo_data['user']}/{repo_data['name']}"
        else:
            repo_name = repo_data['name']
        fields = ['user', 'name', 'description', 'pull_count', 'star_count']
        repo_fields = {}
        for _ in fields:
            repo_fields[_] = repo_data[_]
        if len(repo_data['last_updated']) == 27:
            last_update = datetime.strptime(repo_data['last_updated'], '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            last_update = datetime.strptime(repo_data['last_updated'], '%Y-%m-%dT%H:%M:%SZ')
        repo_fields['last_updated'] = last_update
        return {repo_name: repo_fields}

    def get_repository_stats(self, organization, repository):
        '''fetch and returns stats about a single repository'''
        request_url = f'{self._base_url}/{organization}/{repository}'
        with urlopen(request_url) as response:
            repo_data = json.load(response)
        repo_data = self._parse_repo_data(repo_data)
        return repo_data

    def get_repository_list(self, organization):
        '''fetch and returns the list of repositories published by an organization'''
        request_url = f'{self._base_url}/{organization}'
        repositories = {}
        while request_url is not None:
            with urlopen(request_url) as response:
                repository_data = json.load(response)
            for _ in repository_data['results']:
                repositories.update(self._parse_repo_data(_))
            request_url = repository_data['next']
        return repositories
