
from __future__ import annotations
import logging
from typing import List, TypedDict

import ros_api

logger = logging.getLogger('MikrotikRouter.Mqtt')


class LeaseDict(TypedDict, total=False):
    id: str  # '.id'
    address: str
    mac_address: str  # 'mac-address'
    client_id: str  # 'client-id'
    address_lists: str  # 'address-lists'
    server: str
    dhcp_option: str  # 'dhcp-option'
    status: str
    expires_after: str  # 'expires-after'
    last_seen: str  # 'last-seen'
    active_address: str  # 'active-address'
    active_mac_address: str  # 'active-mac-address'
    active_client_id: str  # 'active-client-id'
    active_server: str  # 'active-server'
    class_id: str  # 'class-id'
    radius: str
    dynamic: str
    blocked: str
    disabled: str
    comment: str

class ActivityDict(TypedDict, total=False):
    id: str  # '.id'
    name: str
    mac_address: str  # 'mac-address'
    user: str
    dynamic: str
    blocked: str
    limited: str
    inactive: str
    disabled: str

class WifiRegistrationDict(TypedDict, total=False):
    id: str  # '.id'
    interface: str
    mac_address: str  # 'mac-address'
    ap: str
    wds: str
    bridge: str
    rx_rate: str  # 'rx-rate'
    tx_rate: str  # 'tx-rate'
    packets: str
    bytes: str
    frames: str
    frame_bytes: str  # 'frame-bytes'
    hw_frames: str  # 'hw-frames'
    hw_frame_bytes: str  # 'hw-frame-bytes'
    tx_frames_timed_out: str  # 'tx-frames-timed-out'
    uptime: str
    last_activity: str  # 'last-activity'
    signal_strength: str  # 'signal-strength'
    signal_to_noise: str  # 'signal-to-noise'
    signal_strength_ch0: str  # 'signal-strength-ch0'
    signal_strength_ch1: str  # 'signal-strength-ch1'
    strength_at_rates: str
    tx_ccq: str  # 'tx-ccq'
    p_throughput: str  # 'p-throughput'
    last_ip: str  # 'last-ip'
    dot1x_port_enabled: str  # '802.1x-port-enabled'
    authentication_type: str
    encryption: str
    group_encryption: str
    management_protection: str
    wmm_enabled: str
    tx_rate_set: str    

    

class MikrotikRouter:
    """
    This class represents a Mikrotik Router and provides methods to retrieve
    various information from the router.
    """

    def __init__(self, ipAddr: str, user: str, passwd: str) -> None:
        """
        Constructor for the MikrotikRouter class.

        :param ipAddr: The IP address of the router
        :param user: The username to authenticate with
        :param passwd: The password to authenticate with
        """
        self.user = user
        self.password = passwd
        self.router = ros_api.Api(ipAddr, user=user, password=passwd)

    def getListOfInterfaces(self) -> List[dict]:
        r = self.router.talk('/interface/print')
        return r

    def getSystemResources(self) -> List[dict]:
        r = self.router.talk('/system/resource/print')
        return r

    def getMonitorTraffic(self, interfaceName: str) -> dict:
        r = self.router.talk(f'/interface/monitor-traffic\n=interface={interfaceName}\n=once=')
        return r

    def getNeighbors(self) -> List[MikrotikRouter]:
        """
        Retrieves a list of neighboring Mikrotik routers.

        :return: A list of MikrotikRouter objects
        """
        neighbors: List[MikrotikRouter] = []

        r = self.router.talk('/ip/neighbor/print')
        for neighbor in r:
            if neighbor['platform'] == 'MikroTik':
                try:
                    mikroTikRouter = MikrotikRouter(neighbor['address'], self.user, self.password)
                    neighbors.append(mikroTikRouter)

                except BaseException:
                    logging.exception("Error in setting up Router: %s", neighbor['address'])

        return neighbors

    def getLeases(self) -> List[LeaseDict]:
        """
        Retrieves a list of DHCP leases.

        :return: A list of dictionary objects representing leases
        """
        leases: List[LeaseDict] = []

        r = self.router.talk('/ip/dhcp-server/lease/print')
        for lease in r:
            if lease['status'] == 'bound':
                leases.append(lease)

        return leases

    def getDns(self) -> List[dict]:
        """
        Retrieves a list of DNS static entries.

        :return: A list of dictionary objects representing DNS static entries
        """
        r = self.router.talk('/ip/dns/static/print')
        return r

    def getWiFiRegistrationTable(self) -> List[WifiRegistrationDict]:
        """
        Retrieves the WiFi registration table.

        :return: A list of dictionary objects representing the WiFi registration table
        """
        r = self.router.talk('/interface/wireless/registration-table/print')
        return r

    def getIdentity(self) -> str:
        """
        Retrieves the identity of the router.

        :return: A string representing the router's identity
        """
        r = self.router.talk('/system/identity/print')
        return r[0]['name']

    def getActivities(self) -> List[ActivityDict]:
        """
        Retrieves a list of kid-control device activities.

        :return: A list of dictionary objects representing kid-control device activities
        """
        r = self.router.talk('/ip/kid-control/device/print')
        return r
    
    def initActivitiesListCreation(self) -> None:
        """
        Initializes the activities list creation process.

        :return: None
        """
        #self.router.talk('/ip kid-control device remove name=DummyDevice user=DummyUser')
        #self.router.talk('/ip kid-control device add name=DummyDevice mac-address=FF:FF:FF:FF:FF:FF user=DummyUser')
