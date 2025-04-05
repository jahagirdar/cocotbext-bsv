from cocotb_bus import BusDriver
from cocotb.triggers import Lock, RisingEdge


class FIFO(BusDriver):
    inputs='D_IN ENQ DEQ CLR'.split(' ')
    outputs='D_OUT EMPTY_N FULL_N'.split(' ')
    _signals=inputs+ outputs

    def __init__(self, dut, prefix, clk, reset_n):
        self.dut=dut
        self.prefix=prefix
        self.clk=clk
        self.reset_n=reset_n
        self.lock= Lock()
        super.__init__(self,dut,prefix,clk)

    async def enq(self, value):
        await self.lock.acquire()
        await RisingEdge(self.bus.self.bus.RDY_enq)
        self.bus.enq_1.value = value
        self.bus.EN_enq.value = 1
        await RisingEdge(self.clk)
        self.bus.EN_enq.value = 0
        await self.lock.release()

    async def deq(self, value):
        await self.lock.acquire()
        await RisingEdge(self.bus.self.bus.RDY_deq)
        self.bus.EN_deq.value = 1
        await RisingEdge(self.clk)
        self.bus.EN_deq.value = 0
        await self.lock.release()

    def first(self, value):
        return self.bus.first.value


