import csv
from graph.system_graph import HydraulicSystemGraph
from simulation.engine import SimulationEngine

def build_aviation_system() -> HydraulicSystemGraph:
    """
    Constructs the static physical map of the hydraulic system mapping.
    """
    sys_graph = HydraulicSystemGraph()

    # 1. Add Components (Nodes)
    sys_graph.add_component("Pump_1", "Engine_Driven_Pump")
    sys_graph.add_component("Valve_A", "Selector_Valve")
    sys_graph.add_component("Actuator_LeftWing", "Actuator")

    # 2. Add Piping (Edges)
    sys_graph.add_pipe("Pump_1", "Valve_A", material="Titanium", length=5.0, diameter=0.03)
    sys_graph.add_pipe("Valve_A", "Actuator_LeftWing", material="Aluminum", length=12.0, diameter=0.02)

    return sys_graph

def export_telemetry_to_csv(telemetry_history: list, filename: str):
    """
    Converts the engine's list of dictionaries into a flat CSV file.
    """
    if not telemetry_history:
        print("No data to export!")
        return
        
    print(f"Exporting data to {filename}...")
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write Header
        writer.writerow(["Timestamp_Seconds", "Node_ID", "Pressure_psi", "Temperature_C", "Wear_Factor"])
        
        # Write Data
        for step_data in telemetry_history:
            for node_id, metrics in step_data.items():
                writer.writerow([
                    metrics.get("timestamp", 0),
                    node_id,
                    round(metrics.get("pressure", 0.0), 2),
                    round(metrics.get("temperature", 0.0), 2),
                    round(metrics.get("wear_factor", 0.0), 6)
                ])
                
    print(f"Successfully exported {len(telemetry_history)} time steps!")

def main():
    print("--- Aviation Hydraulic Simulator ---")
    
    # 1. Build the Map
    print("Building system graph...")
    system_graph = build_aviation_system()
    
    # 2. Initialize the Engine (Simulate 1 hour = 3600 seconds)
    duration_seconds = 3600
    simulator = SimulationEngine(graph=system_graph, duration=duration_seconds)
    
    # 3. Run the Simulation
    flight_data = simulator.run()
    
    # 4. Save to CSV
    export_telemetry_to_csv(flight_data, "synthetic_flight_data_001.csv")
    print("Check your folder for the new CSV file!")

if __name__ == "__main__":
    main()
