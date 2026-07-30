import random

def evaluate_wear_and_tear(node_data: dict, current_time: int) -> dict:
    """
    Simulates slow, progressive degradation of mechanical parts.
    Increases the 'Wear_Factor' by a tiny amount based on uptime/usage.
    """
    # Base wear factor starts at 0.0 (perfectly healthy)
    current_wear = node_data.get("Wear_Factor", 0.0)
    
    # Only mechanical components like Pumps and Actuators suffer significant wear
    component_type = node_data.get("component_type", "Unknown")
    
    if component_type in ["Engine_Driven_Pump", "Actuator"]:
        # Simulate a tiny, somewhat randomized amount of wear every tick
        # e.g., 0.00001 wear per second
        wear_increment = random.uniform(0.000005, 0.000015)
        new_wear = current_wear + wear_increment
        
        # Cap wear at 1.0 (100% destruction/failure)
        node_data["Wear_Factor"] = min(1.0, new_wear)
        
    return node_data

def inject_sudden_fault(node_data: dict, fault_type: str) -> dict:
    """
    Triggers an immediate, catastrophic event that radically alters component properties.
    """
    if fault_type == "PUMP_RUPTURE":
        # A ruptured pump immediately drops its max threshold and wear hits 100%
        node_data["Nominal_Pressure_Threshold"] *= 0.1  # Drops to 10% capacity
        node_data["Wear_Factor"] = 1.0
        node_data["Status"] = "Critical"
        
    elif fault_type == "VALVE_STUCK_CLOSED":
        # E.g., setting a simulated flow flag to False
        node_data["is_open"] = False
        node_data["Status"] = "Critical"

    return node_data

def calculate_leak_severity(pipe_attributes: dict, time_since_leak: int) -> float:
    """
    Simulates a leak that worsens over time due to high pressure expanding the hole.
    Returns the severity multiplier (0.0 means no leak, higher numbers mean massive loss).
    """
    # A base severity when the leak first forms
    base_leak_factor = pipe_attributes.get("leak_severity", 0.0)
    
    if base_leak_factor > 0:
        # The leak gets exponentially worse the longer it is ignored
        # A tiny growth factor every second
        growth_rate = 1.001 
        worsened_leak = base_leak_factor * (growth_rate ** time_since_leak)
        
        # Max leak severity is capped so the math doesn't explode infinitely
        return min(0.99, worsened_leak) 
        
    return 0.0
