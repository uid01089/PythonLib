
from __future__ import annotations
import logging
from typing import List

import ros_api

logger = logging.getLogger('MikrotikRouter.Mqtt')

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
        neighbors : List[MikrotikRouter] = []

        r = self.router.talk('/ip/neighbor/print')
        for neighbor in r:
            if neighbor['platform'] == 'MikroTik' and neighbor['interface'] == 'vlan30_Parents':
                try:                
                    mikroTikRouter = MikrotikRouter(neighbor['address'], self.user, self.password)
                    neighbors.append(mikroTikRouter)

                except BaseException:
                    logging.exception("Error in setting up Router: %s", neighbor['address'])

        return neighbors

    def getLeases(self) -> List[dict]:
        """
        Retrieves a list of DHCP leases.

        :return: A list of dictionary objects representing leases
        """
        leases : List[dict] = []

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

    def getWiFiRegistrationTable(self) -> List[dict]:
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

    def getActivities(self) -> List[dict]:
        """
        Retrieves a list of kid-control device activities.

        :return: A list of dictionary objects representing kid-control device activities
        """
        r = self.router.talk('/ip/kid-control/device/print')
        return r
