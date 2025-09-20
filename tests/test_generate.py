import pytest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace
from cli.subcmd import generate

# -------------------------------
# Test 1: Flujo normal con peers bidireccionales
# -------------------------------
@patch('cli.subcmd.generate.os.path.isfile', return_value=True)
@patch('cli.subcmd.generate.load_nodes')
@patch('cli.subcmd.generate.assign_ips')
@patch('cli.subcmd.generate.generate_keypair')
@patch('cli.subcmd.generate.VPNNetwork')
@patch('cli.subcmd.generate.generate_config_files')
def test_generate_normal_flow(mock_generate_config_files, mock_VPNNetwork, mock_generate_keypair,
                              mock_assign_ips, mock_load_nodes, mock_isfile):

    # Dos nodos con peers cruzados
    node1 = SimpleNamespace(name='node1', peers=['node2'], private_key=None, public_key=None, id=None, ip=None, port=None, allowed_ips=None)
    node2 = SimpleNamespace(name='node2', peers=['node1'], private_key=None, public_key=None, id=None, ip=None, port=None, allowed_ips=None)
    nodes = [node1, node2]

    mock_load_nodes.return_value = nodes
    mock_generate_keypair.side_effect = [('priv1','pub1'), ('priv2','pub2')]
    mock_vpn_instance = MagicMock()
    mock_VPNNetwork.return_value = mock_vpn_instance

    args = SimpleNamespace(input='nodes.json', output='/tmp/configs', subnet='10.10.0.0/16')
    generate.run_generate(args)

    assert node1.private_key == 'priv1'
    assert node2.private_key == 'priv2'
    assert node1.public_key == 'pub1'
    assert node2.public_key == 'pub2'

    assert mock_vpn_instance.add_node.call_count == 2
    mock_generate_config_files.assert_called_once_with(nodes, '/tmp/configs', '10.10.0.0/16')


# -------------------------------
# Test 2: Private IP fuera del rango de subred
# -------------------------------
@patch('cli.subcmd.generate.os.path.isfile', return_value=True)
@patch('cli.subcmd.generate.load_nodes')
@patch('cli.subcmd.generate.assign_ips')
def test_generate_private_ip_out_of_range(mock_assign_ips, mock_load_nodes, mock_isfile):
    # Nodo con IP fuera de 10.10.0.0/16
    node = SimpleNamespace(name='node1', peers=[], private_key=None, public_key=None, id=None,
                           ip='192.168.1.5', port=None, allowed_ips=None)
    mock_load_nodes.return_value = [node]
    # assign_ips lanza ValueError si IP fuera de subnet
    mock_assign_ips.side_effect = ValueError("Private IP 192.168.1.5 is outside 10.10.0.0/16")

    args = SimpleNamespace(input='nodes.json', output='/tmp/configs', subnet='10.10.0.0/16')
    with pytest.raises(ValueError, match="Private IP 192.168.1.5 is outside 10.10.0.0/16"):
        generate.run_generate(args)


# -------------------------------
# Test 3: 5 nodos con IPs automáticas
# -------------------------------
@patch('cli.subcmd.generate.os.path.isfile', return_value=True)
@patch('cli.subcmd.generate.load_nodes')
@patch('cli.subcmd.generate.assign_ips')
@patch('cli.subcmd.generate.generate_keypair')
@patch('cli.subcmd.generate.VPNNetwork')
@patch('cli.subcmd.generate.generate_config_files')
def test_generate_five_nodes_auto_ips(mock_generate_config_files, mock_VPNNetwork, mock_generate_keypair,
                                      mock_assign_ips, mock_load_nodes, mock_isfile):
    nodes = [SimpleNamespace(name=f'node{i}', peers=None, private_key=None, public_key=None, id=None, ip=None, port=None, allowed_ips=None)
             for i in range(1, 6)]
    mock_load_nodes.return_value = nodes
    mock_generate_keypair.side_effect = [('priv'+str(i), 'pub'+str(i)) for i in range(1,6)]
    mock_vpn_instance = MagicMock()
    mock_vpn_instance.add_node.side_effect = lambda node: node
    mock_VPNNetwork.return_value = mock_vpn_instance

    args = SimpleNamespace(input='nodes.json', output='/tmp/configs', subnet='10.10.0.0/16')
    generate.run_generate(args)

    for i, node in enumerate(nodes, start=1):
        assert node.private_key == f'priv{i}'
        assert node.public_key == f'pub{i}'

    assert mock_vpn_instance.add_node.call_count == 5
    mock_generate_config_files.assert_called_once_with(nodes, '/tmp/configs', '10.10.0.0/16')
