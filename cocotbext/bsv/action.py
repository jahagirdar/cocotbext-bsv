import cocotb
from cocotb_bus.drivers import BusDriver
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly, Timer, ReadWrite, Lock

class Action(BusDriver):
    _signals = []
    def __init__(self, entity, name, clock, params=None, generator=None):
        if params is not None:
            self._signals.extend(params)
        BusDriver.__init__(self, entity, name, clock)
        self.bus._add_signal('en', f'EN_{name}')
        self.bus._add_signal('rdy', f'RDY_{name}')
        self.bus_lock = Lock("%s_txn" % name)
        # TODO Initialize input signals self.bus.tag.setimmediatevalue(1)

    def start(self, generator=None):
        pass

    def stop(self):
        pass

    async def action(self,**kwargs):
        await self.bus_lock.acquire()
        if self.bus.rdy.value != 1:
            await RisingEdge(self.bus.rdy)
            for key,val in kwargs.enumerate():
                if key in self.params:
                    sig= getattr(self.bus,key)
                    sig.value=val
                else:
                    assert 0, f'Unknown parameter {key} in {kwargs}'
            self.bus.en.value = 1
        await RisingEdge(self.clock)
        self.bus.en.value = 0
        self.bus_lock.release()

    async def _driver_send(self, txn, sync=True):
        if sync:
            await RisingEdge(self.clock)
        await self.action(**txn)
        self.bus_lock.release()


class Method(BusDriver):
    """
    Method could return multiple values. Should we pass a list of indexes to breakdown the rv on and return a hash?
    """
    pass

class ActionValue(BusDriver):
    pass


