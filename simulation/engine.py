from graph.system_graph import HydraulicSystemGraph
from simulation.pressure_model import calculate_pump_pressure
from simulation.failure_model import evaluate_wear_and_tear

class SimulationEngine:
    def __init__(self, graph: HydraulicSystemGraph, duration: int = 3600):
        """
        Initializes the simulation engine with a specific hydraulic system map
        and sets the duration of the flight.
        """
        self.graph = graph
        self.duration = duration
        self.current_time = 0
        self.telemetry_history = [] 

    def tick(self):
        """
        Moves the simulation forward by 1 time step (1 second).
        Applies wear and tear, calculates physics, and updates the graph.
        """
        current_step_data = {}

        # Loop through every node in the graph map
        for node_id, node_data in self.graph.graph.nodes(data=True):
            
            # --- 1. CHAOS PHASE (Failure Model) ---
            # Apply slow wear and tear to the component
            node_data = evaluate_wear_and_tear(node_data, self.current_time)
            
            # --- 2. PHYSICS PHASE (Pressure Model) ---
            current_pressure = node_data.get("pressure", 0.0) # default fallback
            
            if "Pump" in node_data.get("component_type", ""):
                # If it's a pump, actively calculate its pressure generation based on wear
                current_pressure = calculate_pump_pressure(node_data, self.current_time)
            
            # Temperatures could also be calculated here similarly
            current_temperature = node_data.get("temperature", 50.0)

            # Store the calculations for this specific node at this exact second
            current_step_data[node_id] = {
                "pressure": current_pressure,
                "temperature": current_temperature,
                "timestamp": self.current_time,
                "wear_factor": node_data.get("Wear_Factor", 0.0)
            }

        # --- 3. UPDATE PHASE ---
        # Push all newly calculated math back into the Graph so it can 
        # re-evaluate its healthy/warning/critical statuses
        self.graph.update_telemetry(current_step_data)

        # --- 4. MEMORY PHASE ---
        # Save a snapshot of this second for data export later
        self.telemetry_history.append(current_step_data)

        # --- 5. TIME PHASE ---
        self.current_time += 1

    def run(self):
        """
        Runs the simulation loop automatically until the duration is reached.
        Returns the massive dataset of all history.
        """
        print(f"Starting simulation run for {self.duration} seconds...")
        
        while self.current_time < self.duration:
            self.tick()
            
            # Optional: Print progress every 600 seconds (10 minutes)
            if self.current_time % 600 == 0:
                print(f"Simulating... Time: {self.current_time}s / {self.duration}s")
                
        print("Simulation complete!")
        return self.telemetry_history
