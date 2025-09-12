
from __future__ import annotations
import logging
from typing import List, TypedDict

import ros_api

logger = logging.getLogger('MikrotikRouter.Mqtt')

class DnsDict(TypedDict, total=False):
    id: str           # '.id'
    name: str
    address: str
    ttl: str
    dynamic: str
    disabled: str
    comment: str


class SystemResourceDict(TypedDict, total=False):
    uptime: str
    version: str
    build_time: str  # 'build-time'
    factory_software: str  # 'factory-software'
    free_memory: str  # 'free-memory'
    total_memory: str  # 'total-memory'
    cpu: str
    cpu_count: str  # 'cpu-count'
    cpu_frequency: str  # 'cpu-frequency'
    cpu_load: str  # 'cpu-load'
    free_hdd_space: str  # 'free-hdd-space'
    total_hdd_space: str  # 'total-hdd-space'
    write_sect_since_reboot: str  # 'write-sect-since-reboot'
    write_sect_total: str  # 'write-sect-total'
    bad_blocks: str  # 'bad-blocks'
    architecture_name: str  # 'architecture-name'
    board_name: str  # 'board-name'
    platform: str

class InterfaceDict(TypedDict, total=False):
    id: str  # '.id'
    name: str
    default_name: str  # 'default-name'
    type: str
    mtu: str
    actual_mtu: str  # 'actual-mtu'
    l2mtu: str
    max_l2mtu: str  # 'max-l2mtu'
    mac_address: str  # 'mac-address'
    link_downs: str  # 'link-downs'
    rx_byte: str  # 'rx-byte'
    tx_byte: str  # 'tx-byte'
    rx_packet: str  # 'rx-packet'
    tx_packet: str  # 'tx-packet'
    rx_drop: str  # 'rx-drop'
    tx_drop: str  # 'tx-drop'
    tx_queue_drop: str  # 'tx-queue-drop'
    rx_error: str  # 'rx-error'
    tx_error: str  # 'tx-error'
    fp_rx_byte: str  # 'fp-rx-byte'
    fp_tx_byte: str  # 'fp-tx-byte'
    fp_rx_packet: str  # 'fp-rx-packet'
    fp_tx_packet: str  # 'fp-tx-packet'
    running: str
    slave: str
    disabled: str

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

class MonitorTrafficDict(TypedDict, total=False):
    name: str
    rx_packets_per_second: str  # 'rx-packets-per-second'
    rx_bits_per_second: str     # 'rx-bits-per-second'
    fp_rx_packets_per_second: str  # 'fp-rx-packets-per-second'
    fp_rx_bits_per_second: str     # 'fp-rx-bits-per-second'
    rx_drops_per_second: str
    rx_errors_per_second: str
    tx_packets_per_second: str
    tx_bits_per_second: str
    fp_tx_packets_per_second: str  # 'fp-tx-packets-per-second'
    fp_tx_bits_per_second: str     # 'fp-tx-bits-per-second'
    tx_drops_per_second: str
    tx_queue_drops_per_second: str
    tx_errors_per_second: str    

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

    def getListOfInterfaces(self) -> List[InterfaceDict]:
        r = self.router.talk('/interface/print')
        return r

    def getSystemResources(self) -> SystemResourceDict:
        r = self.router.talk('/system/resource/print')
        return r[0]

    def getMonitorTraffic(self, interfaceName: str) -> MonitorTrafficDict:
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

    def getDns(self) -> List[DnsDict]:
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
