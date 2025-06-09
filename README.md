# Packet-Routing-Simulation-
This is a comprehensive, interactive Python application that simulates and visualizes various network routing algorithms. It provides a modern, dark-themed GUI where users can create networks, run multiple pathfinding algorithms simultaneously, and compare their performance in real-time.

![image_alt](https://github.com/AdityaRukmangad/Packet-Routing-Simulation-/blob/aff6981645863310319ba86fe4c62d198b920d20/Screenshot%20(162).png)
Key Features
🌐 Network Generation

Multiple Network Types: Random, Scale-Free, Small World, and Grid networks
Customizable Parameters: Adjustable number of nodes (5-50) and edges (5-100)
Automatic Weight Assignment: Random edge weights (1-10) for realistic network simulation
Connected Networks: Ensures all generated networks are connected for proper routing

✏️ Manual Network Editing

Interactive Canvas: Click-to-add nodes directly on the visualization
Manual Controls: Add nodes and edges through input fields
Real-time Editing: Modify networks while preserving existing structure
Save/Load: Export and import network configurations as JSON files
Clear Function: Reset networks for new experiments

🧠 Advanced Routing Algorithms
The simulator implements five major pathfinding algorithms:

BFS (Breadth-First Search)

Finds shortest path in terms of hop count
Explores nodes level by level
Guaranteed to find shortest unweighted path


DFS (Depth-First Search)

Explores as far as possible along each branch
Uses stack-based approach
May not find optimal path but useful for comparison


Dijkstra's Algorithm

Finds shortest weighted path
Guarantees optimal solution for non-negative weights
Industry standard for shortest path problems


Bellman-Ford Algorithm

Handles negative edge weights
Detects negative cycles
More robust but slower than Dijkstra


A (A-Star) Algorithm*

Uses heuristic function for faster pathfinding
Combines Dijkstra with distance estimation
Optimal and more efficient than Dijkstra



🎨 Advanced Visualization

Modern Dark Theme: Professional blue/cyan color scheme
Real-time Animation: Packet movement along discovered paths
Color-coded Algorithms: Each algorithm has distinct colors for easy identification
Dynamic Node Sizing: Adjustable node sizes and edge thickness
Multiple Layouts: Spring, Circular, Random, and Shell layout options
Interactive Elements: Hover effects and clickable components

📊 Performance Analytics

Detailed Statistics: Path cost, hop count, execution time for each algorithm
Comparative Analysis: Side-by-side algorithm performance
Efficiency Metrics: Performance ratios and optimization indicators
Network Analysis: Density, connectivity, and structural information
Real-time Results: Live updates during algorithm execution

🖥️ User Interface Components
Tabbed Control Panel

Generate Tab: Network creation with type selection and parameters
Manual Edit Tab: Interactive editing tools and file operations
Algorithms Tab: Route configuration and algorithm selection
Visualization Tab: Animation settings and layout options
Statistics Tab: Detailed performance metrics and comparisons

Visualization Panel

Large matplotlib canvas with interactive capabilities
Animation controls (pause, stop, refresh)
Real-time path highlighting
Professional network rendering

Status Panel

Live status updates
Real-time clock display
Algorithm results summary
Performance comparisons

Technical Implementation
Technologies Used

Python 3.x: Core programming language
Tkinter: GUI framework with modern styling
NetworkX: Graph creation and algorithm implementation
Matplotlib: Scientific plotting and animation
NumPy: Numerical computations and array operations

Architecture

Object-Oriented Design: Clean, modular class structure
Event-Driven Programming: Responsive user interactions
Separation of Concerns: UI, logic, and visualization components
Error Handling: Robust exception management
Memory Efficient: Optimized for large networks

Educational Value
Learning Objectives

Algorithm Comparison: Understand trade-offs between different approaches
Performance Analysis: Learn to evaluate algorithm efficiency
Network Theory: Grasp fundamental graph concepts
Visual Learning: See algorithms in action through animations
Practical Application: Apply theoretical knowledge to real scenarios

Use Cases

Computer Science Education: Teaching graph algorithms and data structures
Network Engineering: Understanding routing protocol behavior
Research: Comparing algorithm performance on different topologies
Professional Development: Learning pathfinding concepts for game development or logistics

Advanced Features
Customization Options

Color Themes: Customizable algorithm colors
Animation Speed: Adjustable visualization speed
Network Parameters: Fine-tune generation settings
Layout Algorithms: Multiple positioning strategies

File Operations

JSON Export/Import: Save and share network configurations
Session Persistence: Maintain work between sessions
Batch Processing: Load predefined network scenarios

Performance Monitoring

Execution Timing: Microsecond-precision measurements
Memory Usage: Efficient resource management
Scalability Testing: Handle networks up to 50 nodes effectively

Future Enhancement Possibilities

Add more algorithms (Floyd-Warshall, Johnson's)
Network topology analysis tools
3D visualization capabilities
Real-time network simulation
Machine learning-based routing
Multi-objective optimization
Large-scale network support

This simulator serves as both an educational tool and a professional application for understanding the fundamental concepts of network routing, making complex algorithms accessible through intuitive visualization and comprehensive analysis tools.
