import networkx as nx
from typing import Dict, Any

class HydraulicSystemGraph:
    """
    Manages the directed graph representation of the hydraulic system.
    Handles static topology loading and dynamic telemetry updates.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def add_component(self, node_id: str, component_type: str, **attributes):
        """
        Adds a physical component (Node) to the system.
        Validates component type and sets foundational static attributes 
        like thresholds and criticality.
        """
        valid_types = [
            "Engine_Driven_Pump", "Actuator", 
            "Selector_Valve", "Reservoir", "Filter", "Junction"
        ]
        
        if component_type not in valid_types:
            raise ValueError(f"Invalid component_type '{component_type}'. Must be one of {valid_types}")
            
        # Define baseline static thresholds 
        default_attributes = {
            "Nominal_Pressure_Threshold": 3000.0, # psi
            "Max_Temperature_Tolerance": 120.0,   # Celsius
            "Criticality_Score": 0.5              # Default medium criticality
        }
        
        # Custom logic for specific types (can be expanded later)
        if "Pump" in component_type:
            default_attributes["Criticality_Score"] = 0.9
        elif "Actuator" in component_type:
            default_attributes["Criticality_Score"] = 0.8
            
        # Override defaults with any kwargs passed when adding the node
        default_attributes.update(attributes)
        
        self.graph.add_node(node_id, component_type=component_type, **default_attributes)
        
    def add_pipe(self, source_id: str, target_id: str, **attributes):
        """
        Adds a pipe (Edge) connecting two components.
        Validates node existence and enforces static attributes like 
        length, diameter, and material type based on the schema.
        """
        # Ensure both source and target components actually exist in the graph first
        if source_id not in self.graph or target_id not in self.graph:
            raise ValueError(f"Cannot connect '{source_id}' -> '{target_id}': One or both nodes are missing.")

        valid_materials = ["Titanium", "Steel", "Aluminum", "Composite"]
        
        # Validate the material if it was provided
        material = attributes.get("material", "Titanium")
        if material not in valid_materials:
            raise ValueError(f"Invalid material '{material}'. Must be one of {valid_materials}")

        # Define baseline pipe attributes
        default_attributes = {
            "length": 1.0,           # physical distance in meters
            "diameter": 0.02,        # dictation of flow capacity (meters)
            "material": material,
            "max_pressure_rating": 5000.0 if material == "Titanium" else 3500.0,
            "wear_factor": 0.0       # baseline starting wear modeling
        }

        # Override any defaults with custom kwargs passed in
        default_attributes.update(attributes)

        self.graph.add_edge(source_id, target_id, **default_attributes)
        
    def update_telemetry(self, telemetry_data: Dict[str, Dict[str, Any]]):
        """
        Updates the dynamic attributes of the graph continuously and evaluates component status.
        telemetry_data format: { "Node_ID": {"pressure": x, "temperature": y, ...} }
        """
        for node_id, metrics in telemetry_data.items():
            if node_id not in self.graph:
                continue

            # Update the raw telemetry attributes for the node
            for key, value in metrics.items():
                self.graph.nodes[node_id][key] = value

            # Evaluate dynamic status
            node = self.graph.nodes[node_id]
            pressure = node.get("pressure", node.get("Nominal_Pressure_Threshold", 3000.0))
            temperature = node.get("temperature", 50.0) # Assume 50C default

            pressure_threshold = node.get("Nominal_Pressure_Threshold", 3000.0)
            temp_tolerance = node.get("Max_Temperature_Tolerance", 120.0)

            status = "Healthy"
            
            # Simple risk logic based on thresholds
            if pressure > pressure_threshold * 1.2 or temperature >= temp_tolerance:
                status = "Critical"
            elif pressure > pressure_threshold * 1.05 or temperature >= temp_tolerance * 0.9:
                status = "Warning"
            elif pressure < pressure_threshold * 0.5: # e.g. severe leak detected
                status = "Critical"

            self.graph.nodes[node_id]["Status"] = status
        
    def check_flow_path(self, source: str, target: str) -> bool:
        """Verifies if a fluid path exists between a source and a target."""
        try:
            return nx.has_path(self.graph, source, target)
        except nx.NodeNotFound:
            return False

    def identify_bottlenecks(self) -> Dict[str, float]:
        """Calculates betweenness centrality to flag systemic bottlenecks."""
        return nx.betweenness_centrality(self.graph)
