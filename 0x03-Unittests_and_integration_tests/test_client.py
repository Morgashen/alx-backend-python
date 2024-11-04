#!/usr/bin/env python3
"""A module for testing the client module.
"""
import unittest
from typing import Dict
from unittest.mock import (
MagicMock,
Mock,
PropertyMock,
patch,
)
from parameterized import parameterized, parameterized_class
from requests import HTTPError
from client import (
GithubOrgClient
)
from fixtures import TEST_PAYLOAD
def get_json(url):
"""
Retrieves JSON data from a URL.
Args:
url (str): The URL to retrieve the JSON data from.
Returns:
dict: The JSON data as a dictionary.
"""
import requests
response = requests.get(url)
return response.json()
class GithubOrgClient:
"""
A class to interact with the Github Organization API.
"""
def init(self, org_name):
self.org_name = org_name

def org(self):
    """
    Retrieves the organization's information.
    Returns:
        dict: The organization's information.
    """
    return get_json(f"https://api.github.com/orgs/{self.org_name}")

@property
def _public_repos_url(self):
    """
    Retrieves the URL for the organization's public repositories.
    Returns:
        str: The URL for the organization's public repositories.
    """
    return self.org()["repos_url"]

def public_repos(self, license=None):
    """
    Retrieves the organization's public repositories.
    Args:
        license (str, optional): The license to filter the repositories by.
    Returns:
        list: The names of the organization's public repositories.
    """
    repos = get_json(self._public_repos_url)
    if license:
        repos = [repo for repo in repos if self.has_license(repo, license)]
    return [repo["name"] for repo in repos]

def has_license(self, repo, key):
    """
    Checks if a repository has a specific license.
    Args:
        repo (dict): The repository's information.
        key (str): The license key to check for.
    Returns:
        bool: True if the repository has the specified license, False otherwise.
    """
    try:
        return repo["license"]["key"] == key
    except (KeyError, TypeError):
        return False
class TestGithubOrgClient(unittest.TestCase):
"""
Test cases for the GithubOrgClient class.
"""
@parameterized.expand([
("google", {'login': "google"}),
("abc", {'login': "abc"}),
])
@patch(
"client.get_json",
)
def test_org(self, org: str, expected_response: Dict,
mocked_function: MagicMock) -> None:
"""
Test the org method.
Args:
org (str): The organization name.
expected_response (Dict): The expected response.
mocked_function (MagicMock): The mocked get_json function.
"""
mocked_function.return_value = MagicMock(
return_value=expected_response)
goclient = GithubOrgClient(org)
self.assertEqual(goclient.org(), expected_response)
mocked_function.assert_called_once_with(
"https://api.github.com/orgs/{}".format(org)
)

def test_public_repos_url(self) -> None:
    """
    Test the _public_repos_url property.
    """
    with patch(
        "client.GithubOrgClient.org",
        new_callable=PropertyMock,
    ) as mock_org:
        mock_org.return_value = {
            'repos_url': "https://api.github.com/users/google/repos",
        }
        self.assertEqual(
            GithubOrgClient("google")._public_repos_url,
            "https://api.github.com/users/google/repos",
        )

@patch("client.get_json")
def test_public_repos(self, mock_get_json: MagicMock) -> None:
    """
    Test the public_repos method.
    Args:
        mock_get_json (MagicMock): The mocked get_json function.
    """
    test_payload = {
        'repos_url': "https://api.github.com/users/google/repos",
        'repos': [
            {
                "id": 7697149,
                "name": "episodes.dart",
                "private": False,
                "owner": {
                    "login": "google",
                    "id": 1342004,
                },
                "fork": False,
                "url": "https://api.github.com/repos/google/episodes.dart",
                "created_at": "2013-01-19T00:31:37Z",
                "updated_at": "2019-09-23T11:53:58Z",
                "has_issues": True,
                "forks": 22,
                "default_branch": "master",
            },
            {
                "id": 8566972,
                "name": "kratu",
                "private": False,
                "owner": {
                    "login": "google",
                    "id": 1342004,
                },
                "fork": False,
                "url": "https://api.github.com/repos/google/kratu",
                "created_at": "2013-03-04T22:52:33Z",
                "updated_at": "2019-11-15T22:22:16Z",
                "has_issues": True,
                "forks": 32,
                "default_branch": "master",
            },
        ]
    }
    mock_get_json.return_value = test_payload["repos"]
    with patch(
        "client.GithubOrgClient._public_repos_url",
        new_callable=PropertyMock,
    ) as mock_public_repos_url:
        mock_public_repos_url.return_value = test_payload["repos_url"]
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            [
                "episodes.dart",
                "kratu",
            ],
        )
        mock_public_repos_url.assert_called_once()
    mock_get_json.assert_called_once()

@parameterized.expand([
    ({'license': {'key': "bsd-3-clause"}}, "bsd-3-clause", True),
    ({'license': {'key': "bsl-1.0"}}, "bsd-3-clause", False),
])
def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
    """
    Tests the has_license method.
    Args:
        repo (Dict): The repository information.
        key (str): The license key to check for.
        expected (bool): The expected result.
    """
    gh_org_client = GithubOrgClient("google")
    client_has_licence = gh_org_client.has_license(repo, key)
    self.assertEqual(client_has_licence, expected)
@parameterized_class([
{
'org_payload': TEST_PAYLOAD[0][0],
'repos_payload': TEST_PAYLOAD[0][1],
'expected_repos': TEST_PAYLOAD[0][2],
'apache2_repos': TEST_PAYLOAD[0][3],
},
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
"""
Integration tests for the GithubOrgClient class.
"""
@classmethod
def setUpClass(cls) -> None:
"""
Set up the test class.
"""
route_payload = {
'https://api.github.com/orgs/google': cls.org_payload,
'https://api.github.com/orgs/google/repos': cls.repos_payload,
}

def get_payload(url):
        if url in route_payload:
            return Mock(**{'json.return_value': route_payload[url]})
        return HTTPError

    cls.get_patcher = patch("requests.get", side_effect=get_payload)
    cls.get_patcher.start()

def test_public_repos(self) -> None:
    """
    Test the public_repos method.
    """
    self.assertEqual(
        GithubOrgClient("google").public_repos(),
        self.expected_repos,
    )

def test_public_repos_with_license(self) -> None:
    """
    Test the public_repos method with a license filter.
    """
    self.assertEqual(
        GithubOrgClient("google").public_repos(license="apache-2.0"),
        self.apache2_repos,
    )

@classmethod
def tearDownClass(cls) -> None:
    """
    Tear down the test class.
    """
    cls.get_patcher.stop()
