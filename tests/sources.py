# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import logging
logging.basicConfig(level=logging.DEBUG)

import unittest, tempfile

from httmock import all_requests, HTTMock

from scriptler import sources, config

class TestSources(unittest.TestCase):
    pass

mock_files = {
    'test.sh': '#!/bin/sh\necho "test"'
}

@all_requests
def response_content(url, request):
    file_name = url.path.split('/')[-1]
    return mock_files.get(file_name) or {'status_code': 404, 'content': '404 Not Found'}

class TestGithub(unittest.TestCase):
    def setUp(self):
        self.client = sources.github
        self.source = config.Source(url='github.com/afriemann/scriptler')

    def tearDown(self):
        del self.client
        del self.source

    def test_url_matcher(self):
        for url in [ 'github.com/foobar', 'http://github.com/foobar', 'https://github.com/foobar', 'github.com/foobar/project' ]:
            self.assertTrue(self.client.match(url))

        for url in [ 'github.com' ]:
            self.assertFalse(self.client.match(url))

    def test_build_url(self):
        self.assertEqual(
            self.client.build_url('github.com/foobar/blub', 'some-branch', 'folder/file.sh'),
            'https://raw.githubusercontent.com/foobar/blub/some-branch/folder/file.sh'
        )

        self.assertEqual(
            self.client.build_url('github.com/foobar/blub', None, 'folder/file.sh'),
            'https://raw.githubusercontent.com/foobar/blub/master/folder/file.sh'
        )

    def test_get(self):
        with tempfile.NamedTemporaryFile() as f:
            with HTTMock(response_content):
                self.client.get(self.source, 'test.sh', f.name)

                self.assertEqual(f.read(), mock_files.get('test.sh').encode())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
