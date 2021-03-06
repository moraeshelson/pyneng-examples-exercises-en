import os
import pytest
import task_20_1
import task_20_2


# Checking that the test is called via pytest ... and not python ...
from _pytest.assertion.rewrite import AssertionRewritingHook

if not isinstance(__loader__, AssertionRewritingHook):
    print(f"Tests should be called using this expression:\npytest {__file__}\n\n")


def test_templates_exists():
    assert os.path.exists(
        "templates/cisco_router_base.txt"
    ), "Template templates/cisco_router_base.txt does not exist"


def test_function_return_value():
    service_section = (
        "service timestamps debug datetime msec localtime show-timezone\n"
        "service timestamps log datetime msec localtime show-timezone\n"
        "service tcp-keepalives-in\n"
        "service tcp-keepalives-out\n"
        "service password-encryption\n"
    )
    alias_section = (
        "alias exec top sh proc cpu sorted | excl 0.00%__0.00%__0.00%\n"
        "alias exec diff sh archive config differences nvram:startup-config system:running-config\n"
        "alias exec bri show ip int bri | exc unass\n"
        "alias exec id show int desc\n"
    )
    eem_section = (
        "event manager applet update-int-desc\n"
        " event neighbor-discovery interface regexp .*Ethernet.* cdp add\n"
        ' action 1.0 cli command "enable"\n'
        ' action 2.0 cli command "config t"\n'
        ' action 3.0 cli command "interface $_nd_local_intf_name"\n'
        ' action 4.0 cli command "description To $_nd_cdp_entry_name $_nd_port_id"\n'
    )

    template = "templates/cisco_router_base.txt"
    data = {"hostname": "R1"}
    return_value = task_20_1.generate_config(template, data)
    assert service_section in return_value, "There is no service commands in the configuration"
    assert alias_section in return_value, "There is no alias commands in the configuration"
    assert (
        eem_section in return_value
    ), "There is no event manager commands in the configuration event manager"
    assert data["hostname"] in return_value, "There is no hostname command in the configuration"
