import numpy as np
import random
from dataclasses import dataclass, asdict
from typing import List, Dict


@dataclass
class SystemState:
    time: int
    pressure: float
    temperature: float
    flow_rate: float
    pump_health: float
    valve_health: float
    leak: int  # 0 or 1
    blockage: int  # 0 or 1


class HydraulicDataGenerator:
    def __init__(
        self,
        n_steps: int = 1000,
        seed: int = 42
    ):
        self.n_steps = n_steps
        self.seed = seed
        np.random.seed(seed)
        random.seed(seed)

        # Initial system conditions
        self.base_pressure = 3000  # psi
        self.base_temp = 50  # Celsius
        self.base_flow = 10  # L/min


    # Core Simulation Functions

    def _simulate_pump_health(self, t: int) -> float:
        """Degrades slowly over time"""
        degradation = 0.0005 * t
        noise = np.random.normal(0, 0.01)
        return max(0, 1 - degradation + noise)

    def _simulate_valve_health(self, t: int) -> float:
        degradation = 0.0003 * t
        noise = np.random.normal(0, 0.01)
        return max(0, 1 - degradation + noise)

    def _inject_failures(self) -> Dict[str, int]:
        """Random failures"""
        leak = 1 if random.random() < 0.01 else 0
        blockage = 1 if random.random() < 0.01 else 0
        return {"leak": leak, "blockage": blockage}

    def _compute_pressure(self, pump_health, leak, blockage) -> float:
        pressure = self.base_pressure * pump_health

        if leak:
            pressure *= np.random.uniform(0.5, 0.8)
        if blockage:
            pressure *= np.random.uniform(1.1, 1.3)

        noise = np.random.normal(0, 50)
        return max(0, pressure + noise)

    def _compute_temperature(self, pressure, blockage) -> float:
        temp = self.base_temp + (pressure / 3000) * 20

        if blockage:
            temp += np.random.uniform(10, 30)

        noise = np.random.normal(0, 2)
        return temp + noise

    def _compute_flow(self, pump_health, leak, blockage) -> float:
        flow = self.base_flow * pump_health

        if leak:
            flow *= np.random.uniform(0.6, 0.9)
        if blockage:
            flow *= np.random.uniform(0.5, 0.7)

        noise = np.random.normal(0, 0.5)
        return max(0, flow + noise)

    # ---------------------------
    # Main Generator
    # ---------------------------

    def generate(self) -> List[Dict]:
        data = []

        for t in range(self.n_steps):
            pump_health = self._simulate_pump_health(t)
            valve_health = self._simulate_valve_health(t)

            failures = self._inject_failures()
            leak = failures["leak"]
            blockage = failures["blockage"]

            pressure = self._compute_pressure(pump_health, leak, blockage)
            temperature = self._compute_temperature(pressure, blockage)
            flow_rate = self._compute_flow(pump_health, leak, blockage)

            state = SystemState(
                time=t,
                pressure=pressure,
                temperature=temperature,
                flow_rate=flow_rate,
                pump_health=pump_health,
                valve_health=valve_health,
                leak=leak,
                blockage=blockage
            )

            data.append(asdict(state))

        return data