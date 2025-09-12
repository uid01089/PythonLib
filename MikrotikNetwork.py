from typing import List, TypedDict

from PythonLib.MikrotikRouter import ActivityDict, DnsDict, InterfaceDict, LeaseDict, MikrotikRouter, MonitorTrafficDict, SystemResourceDict, WifiRegistrationDict

class InterfaceMontitorTrafficDict(TypedDict, total=False):
    interface: InterfaceDict
    traffic: MonitorTrafficDict

class MikrotikRouterDict(TypedDict, total=False):
    identity: str
    interfaces: List[InterfaceMontitorTrafficDict]
    systemResources: SystemResourceDict
    leases: List[LeaseDict]
    dns: List[DnsDict]
    wifiRegistrationTable: List[WifiRegistrationDict]
    activities: List[ActivityDict]
    
class MikrotikNetworkDict(TypedDict, total=False):
    routers: List[MikrotikRouterDict]


class MikrotikNetwork:
    def __init__(self, mikrotikRouter: MikrotikRouter) -> None:
        self.mikrotikRouter = mikrotikRouter

    def create(self) -> MikrotikNetworkDict:
        
        mikrotikNetworkDict: MikrotikNetworkDict = {}
        
        
        routers = self.mikrotikRouter.getNeighbors()
        routers.append(self.mikrotikRouter)

        
        mikrotikNetworkDict["routers"] = []
        
        for router in routers:
            routerDict: MikrotikRouterDict = {}
            mikrotikNetworkDict["routers"].append(routerDict)
    
            routerDict["identity"] = router.getIdentity()
            routerDict["systemResources"] = router.getSystemResources()
            routerDict["leases"] = router.getLeases()
            routerDict["dns"] = router.getDns()
            routerDict["wifiRegistrationTable"] = router.getWiFiRegistrationTable()
            routerDict["activities"] = router.getActivities()


            routerDict["interfaces"] = []
            for interface in router.getListOfInterfaces():
                interfaceMontitorTrafficDict:InterfaceMontitorTrafficDict = {}
                interfaceMontitorTrafficDict["interface"] = interface
                interfaceMontitorTrafficDict["traffic"] = router.getMonitorTraffic(interface["name"])
                routerDict["interfaces"].append(interfaceMontitorTrafficDict)
                

        return mikrotikNetworkDict