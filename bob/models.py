# -*- coding: utf-8 -*-

import os
import envoy
import sys
from tempfile import mkstemp

from .utils import deps_extract, path_extract, mkdir_p, process, pipe, targz_tree

WORKSPACE = os.environ.get('WORKSPACE', 'workspace')
DEFAULT_BUILD_PATH = os.environ.get('DEFAULT_BUILD_PATH', '/app/.heroku/')
HOME_PWD = os.getcwd()

class Formula(object):

    def __init__(self, path):
        self.path = path
        self.archive_path = None

    def __repr__(self):
        return '<Formula {}>'.format(self.path)

    @property
    def workspace_path(self):
        return os.path.join(WORKSPACE, self.path)

    @property
    def full_path(self):
        return os.path.abspath(self.workspace_path)

    @property
    def exists(self):
        """Returns True if the forumla appears to exist."""
        return os.path.exists(self.workspace_path)

    @property
    def depends_on(self):
        # TODO: full cascade? (e.g. resolve first?)
        return deps_extract(self.full_path)

    @property
    def build_path(self):
        return build_path_extract(self.full_path) or DEFAULT_BUILD_PATH

    def build(self):

        # Prepare build directory.
        mkdir_p(self.build_path)

        print 'Building formula {}:'.format(self.path)

        # Execute the formula script.
        cmd = [self.full_path, self.build_path]
        p = process(cmd, cwd=self.build_path)

        pipe(p.stdout, sys.stdout, indent=True)
        p.wait()

        if p.returncode != 0:
            print
            print 'WARNING: An error occurred:'
            pipe(p.stderr, sys.stderr, indent=True)
            exit()


    def archive(self):
        """Archives the build directory as a tar.gz."""
        archive = mkstemp()
        targz_tree(self.build_path, archive)

        print archive
        self.archive_path = archive


    def deploy(self):
        pass






