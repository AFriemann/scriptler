# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import unittest, tempfile

from httmock import urlmatch

from scriptler import sources, config

class TestSources(unittest.TestCase):
    pass

@urlmatch(netloc=r'https://raw.githubusercontent.com/(.*)')
def githubusercontent(url, request):
    print(url)
    print(request)

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
            self.client.get(self.source, 'README.rst', f.name)

        assert False

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
