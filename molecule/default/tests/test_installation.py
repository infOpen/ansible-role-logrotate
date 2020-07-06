"""
Role tests
"""

import os
import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_package(host):
    """
    Ensure package is installed
    """

    assert host.package('logrotate').is_installed


@pytest.mark.parametrize('item_type,path,owner,group,mode', [
    ('file', '/etc/logrotate.conf', 'root', 'root', 0o644),
    ('file', '/etc/logrotate.d/my_app.conf', 'root', 'root', 0o644),
    ('directory', '/etc/logrotate.d', 'root', 'root', 0o755),
])
def test_paths(host, item_type, path, owner, group, mode):
    """
    Ensure logrotate paths exists and have expected permissions
    """

    current_item = host.file(path)

    assert current_item.exists

    if item_type == 'file':
        assert current_item.is_file
    elif item_type == 'directory':
        assert current_item.is_directory

    assert current_item.user == owner
    assert current_item.group == group
    assert current_item.mode == mode
