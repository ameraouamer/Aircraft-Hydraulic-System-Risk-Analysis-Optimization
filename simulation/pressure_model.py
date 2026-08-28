import random

def calculate_pump_pressure(node_data: dict, current_time: int) -> float:
    """
    Calculates the current pressure output of a pump, including natural variance
    and potential failures/wear.
    """
    base_pressure = node_data.get("Nominal_Pressure_Threshold", 3000.0)
    
    # Introduce natural minor fluctuations (Gaussian noise)
    noise = random.gauss(mu=0, sigma=10.0)
    
    # Check if a failure mode is currently active on this pump
    damage_factor = node_data.get("Wear_Factor", 0.0)
    
    # The more damaged it is, the less pressure it can produce 
    # and the more erratic it becomes
    current_pressure = (base_pressure * (1.0 - damage_factor)) + noise
    
    return max(0.0, current_pressure) # Pressure can't go below 0

def calculate_pressure_drop(pipe_attributes: dict, upstream_pressure: float) -> float:
    """
    Simulates friction and fluid dynamics. Pressure drops across long or narrow pipes.
    """
    length = pipe_attributes.get("length", 1.0)
    diameter = pipe_attributes.get("diameter", 0.02)
    
    # Simplified fluid dynamics: pressure drop is proportional to length 
    # and inversely proportional to the diameter squared.
    friction_coefficient = 0.005
    pressure_loss = (length / (diameter ** 2)) * friction_coefficient
    
    downstream_pressure = upstream_pressure - pressure_loss
    
    return max(0.0, downstream_pressure)

def calculate_actuator_pressure(node_data: dict, upstream_pressure: float, is_active: bool) -> float:
    """
    Calculates the pressure inside an actuator. If active, it draws massive fluid,
    dropping the local pressure.
    """
    if is_active:
        # Actuator consumes pressure to do mechanical work
        # Draw depends on the component, simplified here to a 15% drop
        draw_factor = 0.85
        return upstream_pressure * draw_factor
    else:
        # If inactive, pressure normalizes to the upstream pressure
        return upstream_pressure
