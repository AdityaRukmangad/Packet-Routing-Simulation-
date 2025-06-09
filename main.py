import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from matplotlib.lines import Line2D
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
import matplotlib
from matplotlib.patches import Circle
import json
from datetime import datetime

matplotlib.use("TkAgg")


class ModernNetworkRoutingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Network Routing Simulator v2.0")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1a1a2e")

        # Modern color scheme
        self.colors = {
            "primary_bg": "#1a1a2e",
            "secondary_bg": "#16213e",
            "accent_bg": "#0f3460",
            "card_bg": "#16213e",
            "text_primary": "#ffffff",
            "text_secondary": "#b8c6db",
            "accent": "#00d4ff",
            "success": "#00ff88",
            "warning": "#ffb347",
            "error": "#ff6b6b",
            "bfs": "#3498db",
            "dfs": "#e74c3c",
            "dijkstra": "#2ecc71",
            "bellman": "#9b59b6",
            "astar": "#f39c12",
            "button_hover": "#00b8d4"
        }

        # Network parameters
        self.network = None
        self.pos = None
        self.source = None
        self.destination = None
        self.manual_mode = False
        self.selected_nodes = []
        self.node_positions = {}
        self.edge_weights = {}

        # Animation variables
        self.animation = None
        self.packet = None
        self.current_algorithm = None

        # Performance tracking
        self.algorithm_stats = {}

        # Setup styles
        self.setup_styles()

        # Create UI
        self.create_modern_ui()

        # Bind events
        self.bind_events()

    def setup_styles(self):
        """Setup modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure styles
        style.configure('Modern.TFrame', background=self.colors["card_bg"])
        style.configure('Modern.TLabel', background=self.colors["card_bg"],
                        foreground=self.colors["text_primary"], font=('Arial', 10))
        style.configure('Modern.TButton', background=self.colors["accent"],
                        foreground='white', font=('Arial', 10, 'bold'))
        style.map('Modern.TButton', background=[('active', self.colors["button_hover"])])
        style.configure('Modern.TCheckbutton', background=self.colors["card_bg"],
                        foreground=self.colors["text_primary"], font=('Arial', 9))

    def create_modern_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors["primary_bg"])
        main_container.pack(fill='both', expand=True, padx=10, pady=10)

        # Left panel - Controls
        self.create_control_panel(main_container)

        # Right panel - Visualization
        self.create_visualization_panel(main_container)

        # Bottom panel - Status and Results
        self.create_status_panel(main_container)

    def create_control_panel(self, parent):
        # Control panel with tabs
        control_frame = tk.Frame(parent, bg=self.colors["secondary_bg"], relief='raised', bd=2)
        control_frame.pack(side='left', fill='y', padx=(0, 10))

        # Title
        title_frame = tk.Frame(control_frame, bg=self.colors["accent"], height=50)
        title_frame.pack(fill='x', padx=5, pady=5)
        title_frame.pack_propagate(False)

        title_label = tk.Label(title_frame, text="🌐 Network Control Center",
                               font=('Arial', 14, 'bold'), bg=self.colors["accent"],
                               fg='white')
        title_label.pack(expand=True)

        # Notebook for tabs
        notebook = ttk.Notebook(control_frame)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Tab 1: Network Generation
        self.create_generation_tab(notebook)

        # Tab 2: Manual Editing
        self.create_manual_tab(notebook)

        # Tab 3: Algorithm Selection
        self.create_algorithm_tab(notebook)

        # Tab 4: Visualization Settings
        self.create_visualization_tab(notebook)

        # Tab 5: Statistics
        self.create_stats_tab(notebook)

    def create_generation_tab(self, notebook):
        gen_frame = ttk.Frame(notebook, style='Modern.TFrame')
        notebook.add(gen_frame, text='🔧 Generate')

        # Network parameters
        params_frame = tk.LabelFrame(gen_frame, text="Network Parameters",
                                     bg=self.colors["card_bg"], fg=self.colors["accent"],
                                     font=('Arial', 10, 'bold'), padx=10, pady=10)
        params_frame.pack(fill='x', padx=5, pady=5)

        # Nodes slider
        tk.Label(params_frame, text="Nodes:", bg=self.colors["card_bg"],
                 fg=self.colors["text_primary"]).grid(row=0, column=0, sticky='w', pady=2)
        self.nodes_var = tk.IntVar(value=10)
        nodes_scale = tk.Scale(params_frame, from_=5, to=50, orient='horizontal',
                               variable=self.nodes_var, bg=self.colors["card_bg"],
                               fg=self.colors["text_primary"], highlightthickness=0)
        nodes_scale.grid(row=0, column=1, sticky='ew', padx=5)

        # Edges slider
        tk.Label(params_frame, text="Edges:", bg=self.colors["card_bg"],
                 fg=self.colors["text_primary"]).grid(row=1, column=0, sticky='w', pady=2)
        self.edges_var = tk.IntVar(value=20)
        edges_scale = tk.Scale(params_frame, from_=5, to=100, orient='horizontal',
                               variable=self.edges_var, bg=self.colors["card_bg"],
                               fg=self.colors["text_primary"], highlightthickness=0)
        edges_scale.grid(row=1, column=1, sticky='ew', padx=5)

        params_frame.columnconfigure(1, weight=1)

        # Network types
        type_frame = tk.LabelFrame(gen_frame, text="Network Type",
                                   bg=self.colors["card_bg"], fg=self.colors["accent"],
                                   font=('Arial', 10, 'bold'), padx=10, pady=10)
        type_frame.pack(fill='x', padx=5, pady=5)

        self.network_type = tk.StringVar(value="random")
        types = [("Random", "random"), ("Scale-Free", "scale_free"),
                 ("Small World", "small_world"), ("Grid", "grid")]

        for i, (text, value) in enumerate(types):
            tk.Radiobutton(type_frame, text=text, variable=self.network_type, value=value,
                           bg=self.colors["card_bg"], fg=self.colors["text_primary"],
                           selectcolor=self.colors["accent"]).grid(row=i // 2, column=i % 2, sticky='w')

        # Generation button
        gen_btn = tk.Button(gen_frame, text="🚀 Generate Network",
                            command=self.generate_network,
                            bg=self.colors["success"], fg='white',
                            font=('Arial', 11, 'bold'), pady=8)
        gen_btn.pack(fill='x', padx=5, pady=10)

    def create_manual_tab(self, notebook):
        manual_frame = ttk.Frame(notebook, style='Modern.TFrame')
        notebook.add(manual_frame, text='✏ Manual Edit')

        # Mode toggle
        mode_frame = tk.Frame(manual_frame, bg=self.colors["card_bg"])
        mode_frame.pack(fill='x', padx=5, pady=5)

        self.manual_mode_var = tk.BooleanVar()
        mode_check = tk.Checkbutton(mode_frame, text="Enable Manual Mode",
                                    variable=self.manual_mode_var,
                                    command=self.toggle_manual_mode,
                                    bg=self.colors["card_bg"], fg=self.colors["text_primary"],
                                    font=('Arial', 10, 'bold'))
        mode_check.pack(pady=5)

        # Manual controls
        controls_frame = tk.LabelFrame(manual_frame, text="Manual Controls",
                                       bg=self.colors["card_bg"], fg=self.colors["accent"],
                                       font=('Arial', 10, 'bold'))
        controls_frame.pack(fill='x', padx=5, pady=5)

        # Add node
        add_node_frame = tk.Frame(controls_frame, bg=self.colors["card_bg"])
        add_node_frame.pack(fill='x', pady=2)
        tk.Label(add_node_frame, text="Node ID:", bg=self.colors["card_bg"],
                 fg=self.colors["text_primary"]).pack(side='left')
        self.new_node_var = tk.StringVar()
        tk.Entry(add_node_frame, textvariable=self.new_node_var, width=10).pack(side='left', padx=5)
        tk.Button(add_node_frame, text="Add Node", command=self.add_manual_node,
                  bg=self.colors["accent"], fg='white', font=('Arial', 8)).pack(side='left')

        # Add edge
        add_edge_frame = tk.Frame(controls_frame, bg=self.colors["card_bg"])
        add_edge_frame.pack(fill='x', pady=2)
        tk.Label(add_edge_frame, text="From:", bg=self.colors["card_bg"],
                 fg=self.colors["text_primary"]).pack(side='left')
        self.edge_from_var = tk.StringVar()
        tk.Entry(add_edge_frame, textvariable=self.edge_from_var, width=5).pack(side='left', padx=2)
        tk.Label(add_edge_frame, text="To:", bg=self.colors["card_bg"],
                 fg=self.colors["text_primary"]).pack(side='left')
        self.edge_to_var = tk.StringVar()
        tk.Entry(add_edge_frame, textvariable=self.edge_to_var, width=5).pack(side='left', padx=2)
        tk.Label(add_edge_frame, text="Weight:", bg=self.colors["card_bg"],
                 fg=self.colors["text_primary"]).pack(side='left')
        self.edge_weight_var = tk.StringVar(value="1")
        tk.Entry(add_edge_frame, textvariable=self.edge_weight_var, width=5).pack(side='left', padx=2)
        tk.Button(add_edge_frame, text="Add Edge", command=self.add_manual_edge,
                  bg=self.colors["accent"], fg='white', font=('Arial', 8)).pack(side='left')

        # Clear network
        tk.Button(controls_frame, text="🗑 Clear Network", command=self.clear_network,
                  bg=self.colors["error"], fg='white', font=('Arial', 10, 'bold')).pack(pady=5)

        # Save/Load
        io_frame = tk.Frame(controls_frame, bg=self.colors["card_bg"])
        io_frame.pack(fill='x', pady=5)
        tk.Button(io_frame, text="💾 Save", command=self.save_network,
                  bg=self.colors["warning"], fg='white', font=('Arial', 9)).pack(side='left', fill='x', expand=True,
                                                                                 padx=2)
        tk.Button(io_frame, text="📂 Load", command=self.load_network,
                  bg=self.colors["warning"], fg='white', font=('Arial', 9)).pack(side='right', fill='x', expand=True,
                                                                                 padx=2)

    def create_algorithm_tab(self, notebook):
        algo_frame = ttk.Frame(notebook, style='Modern.TFrame')
        notebook.add(algo_frame, text='🧠 Algorithms')

        # Source and destination
        route_frame = tk.LabelFrame(algo_frame, text="Route Configuration",
                                    bg=self.colors["card_bg"], fg=self.colors["accent"],
                                    font=('Arial', 10, 'bold'), padx=10, pady=10)
        route_frame.pack(fill='x', padx=5, pady=5)

        # Source
        source_frame = tk.Frame(route_frame, bg=self.colors["card_bg"])
        source_frame.pack(fill='x', pady=2)
        tk.Label(source_frame, text="Source:", bg=self.colors["card_bg"],
                 fg=self.colors["text_primary"]).pack(side='left')
        self.source_var = tk.StringVar(value="1")
        source_combo = ttk.Combobox(source_frame, textvariable=self.source_var, width=8)
        source_combo.pack(side='right')
        self.source_combo = source_combo

        # Destination
        dest_frame = tk.Frame(route_frame, bg=self.colors["card_bg"])
        dest_frame.pack(fill='x', pady=2)
        tk.Label(dest_frame, text="Destination:", bg=self.colors["card_bg"],
                 fg=self.colors["text_primary"]).pack(side='left')
        self.dest_var = tk.StringVar(value="10")
        dest_combo = ttk.Combobox(dest_frame, textvariable=self.dest_var, width=8)
        dest_combo.pack(side='right')
        self.dest_combo = dest_combo

        # Algorithm selection
        algo_select_frame = tk.LabelFrame(algo_frame, text="Select Algorithms",
                                          bg=self.colors["card_bg"], fg=self.colors["accent"],
                                          font=('Arial', 10, 'bold'), padx=10, pady=10)
        algo_select_frame.pack(fill='x', padx=5, pady=5)

        # Algorithm checkboxes with colors
        algorithms = [
            ("BFS", "bfs_var", self.colors["bfs"]),
            ("DFS", "dfs_var", self.colors["dfs"]),
            ("Dijkstra", "dijkstra_var", self.colors["dijkstra"]),
            ("Bellman-Ford", "bellman_var", self.colors["bellman"]),
            ("A*", "astar_var", self.colors["astar"])
        ]

        for i, (name, var_name, color) in enumerate(algorithms):
            setattr(self, var_name, tk.BooleanVar(value=True))
            check_frame = tk.Frame(algo_select_frame, bg=self.colors["card_bg"])
            check_frame.pack(fill='x', pady=1)

            # Color indicator
            color_label = tk.Label(check_frame, text="●", fg=color, bg=self.colors["card_bg"], font=('Arial', 16))
            color_label.pack(side='left')

            tk.Checkbutton(check_frame, text=name, variable=getattr(self, var_name),
                           bg=self.colors["card_bg"], fg=self.colors["text_primary"],
                           font=('Arial', 9)).pack(side='left')

        # Run button
        run_btn = tk.Button(algo_frame, text="🏃 Run Algorithms",
                            command=self.run_algorithms,
                            bg=self.colors["success"], fg='white',
                            font=('Arial', 11, 'bold'), pady=8)
        run_btn.pack(fill='x', padx=5, pady=10)

    def create_visualization_tab(self, notebook):
        viz_frame = ttk.Frame(notebook, style='Modern.TFrame')
        notebook.add(viz_frame, text='🎨 Visualization')

        # Animation settings
        anim_frame = tk.LabelFrame(viz_frame, text="Animation Settings",
                                   bg=self.colors["card_bg"], fg=self.colors["accent"],
                                   font=('Arial', 10, 'bold'), padx=10, pady=10)
        anim_frame.pack(fill='x', padx=5, pady=5)

        # Speed
        tk.Label(anim_frame, text="Speed:", bg=self.colors["card_bg"],
                 fg=self.colors["text_primary"]).pack(anchor='w')
        self.speed_var = tk.IntVar(value=200)
        speed_scale = tk.Scale(anim_frame, from_=50, to=500, orient='horizontal',
                               variable=self.speed_var, bg=self.colors["card_bg"],
                               fg=self.colors["text_primary"], highlightthickness=0)
        speed_scale.pack(fill='x')

        # Node size
        tk.Label(anim_frame, text="Node Size:", bg=self.colors["card_bg"],
                 fg=self.colors["text_primary"]).pack(anchor='w')
        self.node_size_var = tk.IntVar(value=500)
        node_scale = tk.Scale(anim_frame, from_=200, to=1000, orient='horizontal',
                              variable=self.node_size_var, bg=self.colors["card_bg"],
                              fg=self.colors["text_primary"], highlightthickness=0)
        node_scale.pack(fill='x')

        # Layout selection
        layout_frame = tk.LabelFrame(viz_frame, text="Layout Options",
                                     bg=self.colors["card_bg"], fg=self.colors["accent"],
                                     font=('Arial', 10, 'bold'), padx=10, pady=10)
        layout_frame.pack(fill='x', padx=5, pady=5)

        self.layout_var = tk.StringVar(value="spring")
        layouts = [("Spring", "spring"), ("Circular", "circular"),
                   ("Random", "random"), ("Shell", "shell")]

        for text, value in layouts:
            tk.Radiobutton(layout_frame, text=text, variable=self.layout_var, value=value,
                           bg=self.colors["card_bg"], fg=self.colors["text_primary"],
                           selectcolor=self.colors["accent"], command=self.update_layout).pack(anchor='w')

        # Theme selection
        theme_frame = tk.LabelFrame(viz_frame, text="Color Theme",
                                    bg=self.colors["card_bg"], fg=self.colors["accent"],
                                    font=('Arial', 10, 'bold'), padx=10, pady=10)
        theme_frame.pack(fill='x', padx=5, pady=5)

        tk.Button(theme_frame, text="🎨 Customize Colors", command=self.customize_colors,
                  bg=self.colors["accent"], fg='white', font=('Arial', 9)).pack(fill='x')

    def create_stats_tab(self, notebook):
        stats_frame = ttk.Frame(notebook, style='Modern.TFrame')
        notebook.add(stats_frame, text='📊 Statistics')

        # Performance metrics
        self.stats_text = tk.Text(stats_frame, height=15, bg=self.colors["card_bg"],
                                  fg=self.colors["text_primary"], font=('Consolas', 9))
        self.stats_text.pack(fill='both', expand=True, padx=5, pady=5)

        # Clear stats button
        tk.Button(stats_frame, text="🗑 Clear Stats", command=self.clear_stats,
                  bg=self.colors["error"], fg='white', font=('Arial', 9)).pack(pady=5)

    def create_visualization_panel(self, parent):
        viz_container = tk.Frame(parent, bg=self.colors["secondary_bg"], relief='raised', bd=2)
        viz_container.pack(side='left', fill='both', expand=True)

        # Toolbar
        toolbar = tk.Frame(viz_container, bg=self.colors["accent"], height=40)
        toolbar.pack(fill='x', padx=5, pady=5)
        toolbar.pack_propagate(False)

        # Toolbar buttons
        tk.Label(toolbar, text="🖥 Network Visualization", font=('Arial', 12, 'bold'),
                 bg=self.colors["accent"], fg='white').pack(side='left', padx=10)

        # Control buttons
        btn_frame = tk.Frame(toolbar, bg=self.colors["accent"])
        btn_frame.pack(side='right', padx=10)

        tk.Button(btn_frame, text="⏸", command=self.pause_animation,
                  bg='white', fg=self.colors["accent"], font=('Arial', 12)).pack(side='left', padx=2)
        tk.Button(btn_frame, text="⏹", command=self.stop_animation,
                  bg='white', fg=self.colors["accent"], font=('Arial', 12)).pack(side='left', padx=2)
        tk.Button(btn_frame, text="🔄", command=self.refresh_visualization,
                  bg='white', fg=self.colors["accent"], font=('Arial', 12)).pack(side='left', padx=2)

        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 8), facecolor='#1a1a2e')
        self.ax.set_facecolor('#16213e')
        self.fig.tight_layout()

        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_container)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)

        # Initial display
        self.show_welcome_message()

    def create_status_panel(self, parent):
        status_container = tk.Frame(parent, bg=self.colors["secondary_bg"], relief='raised', bd=2)
        status_container.pack(side='bottom', fill='x', pady=(10, 0))

        # Status bar
        status_bar = tk.Frame(status_container, bg=self.colors["accent"], height=30)
        status_bar.pack(fill='x', padx=5, pady=5)
        status_bar.pack_propagate(False)

        self.status_var = tk.StringVar(value="Ready - Generate a network to begin")
        status_label = tk.Label(status_bar, textvariable=self.status_var,
                                bg=self.colors["accent"], fg='white', font=('Arial', 10))
        status_label.pack(side='left', padx=10)

        # Time display
        self.time_var = tk.StringVar()
        time_label = tk.Label(status_bar, textvariable=self.time_var,
                              bg=self.colors["accent"], fg='white', font=('Arial', 10))
        time_label.pack(side='right', padx=10)
        self.update_time()

        # Results area
        results_frame = tk.Frame(status_container, bg=self.colors["card_bg"])
        results_frame.pack(fill='x', padx=5, pady=(0, 5))

        tk.Label(results_frame, text="📋 Algorithm Results:", bg=self.colors["card_bg"],
                 fg=self.colors["accent"], font=('Arial', 10, 'bold')).pack(anchor='w', padx=5)

        self.results_text = tk.Text(results_frame, height=6, bg=self.colors["primary_bg"],
                                    fg=self.colors["text_primary"], font=('Consolas', 9))
        self.results_text.pack(fill='x', padx=5, pady=5)

    def bind_events(self):
        """Bind mouse events for manual editing"""
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)

    def show_welcome_message(self):
        """Show welcome message on startup"""
        self.ax.clear()
        self.ax.text(0.5, 0.5, "Welcome to Advanced Network Routing Simulator v2.0\n\n"
                               "🚀 Generate a network to begin\n"
                               "✏ Use manual mode for custom networks\n"
                               "🧠 Compare different routing algorithms\n"
                               "📊 View detailed performance statistics",
                     horizontalalignment='center', verticalalignment='center',
                     fontsize=14, color=self.colors["accent"], weight='bold',
                     bbox=dict(boxstyle="round,pad=1", facecolor=self.colors["card_bg"], alpha=0.8))
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.canvas.draw()

    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_var.set(f"🕐 {current_time}")
        self.root.after(1000, self.update_time)

    def generate_network(self):
        """Generate network based on selected type"""
        try:
            nodes = self.nodes_var.get()
            edges = self.edges_var.get()
            network_type = self.network_type.get()

            if nodes < 2:
                messagebox.showerror("Error", "Number of nodes must be at least 2")
                return

            self.status_var.set("Generating network...")
            self.root.update()

            # Generate based on type
            if network_type == "random":
                self.network = self.generate_random_network(nodes, edges)
            elif network_type == "scale_free":
                self.network = nx.barabasi_albert_graph(nodes, max(1, edges // nodes))
                self.network = nx.relabel_nodes(self.network, {i: str(i + 1) for i in range(nodes)})
            elif network_type == "small_world":
                self.network = nx.watts_strogatz_graph(nodes, max(2, edges // nodes), 0.3)
                self.network = nx.relabel_nodes(self.network, {i: str(i + 1) for i in range(nodes)})
            elif network_type == "grid":
                size = int(np.sqrt(nodes))
                self.network = nx.grid_2d_graph(size, size)
                self.network = nx.convert_node_labels_to_integers(self.network, first_label=1)
                self.network = nx.relabel_nodes(self.network, {i: str(i) for i in self.network.nodes()})

            # Add random weights
            for edge in self.network.edges():
                self.network[edge[0]][edge[1]]['weight'] = random.randint(1, 10)

            # Update layout
            self.update_layout()

            # Update combo boxes
            node_list = list(self.network.nodes())
            self.source_combo['values'] = node_list
            self.dest_combo['values'] = node_list
            if node_list:
                self.source_var.set(node_list[0])
                self.dest_var.set(node_list[-1])

            # Draw network
            self.draw_network()

            self.status_var.set(
                f"Network generated: {len(self.network.nodes())} nodes, {len(self.network.edges())} edges")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate network: {str(e)}")

    def generate_random_network(self, nodes, edges):
        """Generate a random connected network"""
        G = nx.Graph()

        # Add nodes
        for i in range(1, nodes + 1):
            G.add_node(str(i))

        # Create minimum spanning tree for connectivity
        node_list = list(G.nodes())
        connected = {node_list[0]}
        unconnected = set(node_list[1:])

        while unconnected:
            source = random.choice(list(connected))
            target = random.choice(list(unconnected))
            weight = random.randint(1, 10)
            G.add_edge(source, target, weight=weight)
            connected.add(target)
            unconnected.remove(target)

        # Add remaining edges
        remaining = edges - (nodes - 1)
        attempts = 0
        max_attempts = nodes * 10

        while remaining > 0 and attempts < max_attempts:
            u, v = random.sample(node_list, 2)
            if not G.has_edge(u, v):
                weight = random.randint(1, 10)
                G.add_edge(u, v, weight=weight)
                remaining -= 1
            attempts += 1

        return G

    def update_layout(self):
        """Update network layout"""
        if not self.network:
            return

        layout_type = self.layout_var.get()

        if layout_type == "spring":
            self.pos = nx.spring_layout(self.network, seed=42, k=2, iterations=50)
        elif layout_type == "circular":
            self.pos = nx.circular_layout(self.network)
        elif layout_type == "random":
            self.pos = nx.random_layout(self.network, seed=42)
        elif layout_type == "shell":
            self.pos = nx.shell_layout(self.network)

        if hasattr(self, 'canvas'):
            self.draw_network()

    def draw_network(self):
        """Draw the network with modern styling"""
        if not self.network:
            return

        self.ax.clear()
        self.ax.set_facecolor('#16213e')
        # Get source and destination
        try:
            source = self.source_var.get()
            destination = self.dest_var.get()

            if source not in self.network.nodes():
                source = list(self.network.nodes())[0]
                self.source_var.set(source)
            if destination not in self.network.nodes():
                destination = list(self.network.nodes())[-1]
                self.dest_var.set(destination)

        except:
            nodes_list = list(self.network.nodes())
            source = nodes_list[0] if nodes_list else None
            destination = nodes_list[-1] if len(nodes_list) > 1 else nodes_list[0] if nodes_list else None

            # Node colors with gradient effect
        node_colors = []
        for node in self.network.nodes():
            if node == source:
                node_colors.append('#00ff88')  # Bright green for source
            elif node == destination:
                node_colors.append('#ff6b6b')  # Bright red for destination
            else:
                node_colors.append('#00d4ff')  # Cyan for regular nodes

        # Draw nodes with enhanced styling
        nx.draw_networkx_nodes(self.network, self.pos,
                               node_color=node_colors,
                               node_size=self.node_size_var.get(),
                               alpha=0.9,
                               linewidths=2,
                               edgecolors='white',
                               ax=self.ax)

        # Draw edges with varied thickness based on weight
        edges = self.network.edges()
        weights = [self.network[u][v].get('weight', 1) for u, v in edges]
        max_weight = max(weights) if weights else 1
        edge_widths = [2 + 3 * (w / max_weight) for w in weights]

        nx.draw_networkx_edges(self.network, self.pos,
                               edge_color='#4a90e2',
                               width=edge_widths,
                               alpha=0.6,
                               ax=self.ax)

        # Draw labels with better visibility
        nx.draw_networkx_labels(self.network, self.pos,
                                font_size=10,
                                font_color='white',
                                font_weight='bold',
                                ax=self.ax)

        # Draw edge labels (weights)
        edge_labels = nx.get_edge_attributes(self.network, 'weight')
        nx.draw_networkx_edge_labels(self.network, self.pos,
                                     edge_labels=edge_labels,
                                     font_size=8,
                                     font_color='#ffeb3b',
                                     bbox=dict(boxstyle="round,pad=0.2",
                                               facecolor='black', alpha=0.7),
                                     ax=self.ax)

        # Add grid and styling
        self.ax.grid(True, alpha=0.2, color='white')
        self.ax.set_title(f"Network Topology ({len(self.network.nodes())} nodes, {len(self.network.edges())} edges)",
                          fontsize=14, color='white', weight='bold', pad=20)

        # Remove axes
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # Add legend for node types
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#00ff88',
                   markersize=10, label='Source'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#ff6b6b',
                   markersize=10, label='Destination'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#00d4ff',
                   markersize=10, label='Regular Node')
        ]
        self.ax.legend(handles=legend_elements, loc='upper right',
                       facecolor='#16213e', edgecolor='white',
                       labelcolor='white', fontsize=9)

        self.canvas.draw()

    def toggle_manual_mode(self):
        """Toggle manual editing mode"""
        self.manual_mode = self.manual_mode_var.get()
        if self.manual_mode:
            self.status_var.set("Manual mode enabled - Click to add nodes, select nodes to connect")
        else:
            self.status_var.set("Manual mode disabled")

    def on_canvas_click(self, event):
        """Handle canvas clicks for manual editing"""
        if not self.manual_mode or event.inaxes != self.ax:
            return

        x, y = event.xdata, event.ydata
        if x is None or y is None:
            return

        # Find closest node if clicking near one
        closest_node = None
        min_distance = float('inf')

        if self.network and self.pos:
            for node in self.network.nodes():
                node_x, node_y = self.pos[node]
                distance = np.sqrt((x - node_x) * 2 + (y - node_y) * 2)
                if distance < 0.1 and distance < min_distance:  # Threshold for node selection
                    min_distance = distance
                    closest_node = node

        if closest_node:
            # Select/deselect node
            if closest_node in self.selected_nodes:
                self.selected_nodes.remove(closest_node)
                self.status_var.set(f"Deselected node {closest_node}")
            else:
                self.selected_nodes.append(closest_node)
                self.status_var.set(f"Selected node {closest_node}")

                # If two nodes selected, create edge
                if len(self.selected_nodes) == 2:
                    self.create_edge_between_selected()
        else:
            # Add new node at click position
            self.add_node_at_position(x, y)

    def add_node_at_position(self, x, y):
        """Add a new node at the specified position"""
        if not self.network:
            self.network = nx.Graph()
            self.pos = {}

        # Generate new node ID
        existing_nums = []
        for node in self.network.nodes():
            try:
                existing_nums.append(int(node))
            except:
                pass

        new_id = str(max(existing_nums) + 1 if existing_nums else 1)

        # Add node
        self.network.add_node(new_id)
        self.pos[new_id] = (x, y)

        # Update combo boxes
        self.update_node_combos()

        # Redraw
        self.draw_network()
        self.status_var.set(f"Added node {new_id}")

    def add_manual_node(self):
        """Add node manually via text input"""
        node_id = self.new_node_var.get().strip()
        if not node_id:
            messagebox.showerror("Error", "Please enter a node ID")
            return

        if not self.network:
            self.network = nx.Graph()
            self.pos = {}

        if node_id in self.network.nodes():
            messagebox.showerror("Error", f"Node {node_id} already exists")
            return

        # Add node at random position
        self.network.add_node(node_id)
        self.pos[node_id] = (random.uniform(-1, 1), random.uniform(-1, 1))

        # Clear input
        self.new_node_var.set("")

        # Update and redraw
        self.update_node_combos()
        self.draw_network()
        self.status_var.set(f"Added node {node_id}")

    def add_manual_edge(self):
        """Add edge manually via text input"""
        from_node = self.edge_from_var.get().strip()
        to_node = self.edge_to_var.get().strip()

        try:
            weight = int(self.edge_weight_var.get())
        except:
            weight = 1

        if not from_node or not to_node:
            messagebox.showerror("Error", "Please enter both nodes")
            return

        if not self.network:
            messagebox.showerror("Error", "No network exists")
            return

        if from_node not in self.network.nodes():
            messagebox.showerror("Error", f"Node {from_node} does not exist")
            return

        if to_node not in self.network.nodes():
            messagebox.showerror("Error", f"Node {to_node} does not exist")
            return

        if self.network.has_edge(from_node, to_node):
            messagebox.showerror("Error", f"Edge {from_node}-{to_node} already exists")
            return

        # Add edge
        self.network.add_edge(from_node, to_node, weight=weight)

        # Clear inputs
        self.edge_from_var.set("")
        self.edge_to_var.set("")
        self.edge_weight_var.set("1")

        # Redraw
        self.draw_network()
        self.status_var.set(f"Added edge {from_node}-{to_node} with weight {weight}")

    def create_edge_between_selected(self):
        """Create edge between two selected nodes"""
        if len(self.selected_nodes) != 2:
            return

        node1, node2 = self.selected_nodes

        if self.network.has_edge(node1, node2):
            self.status_var.set(f"Edge {node1}-{node2} already exists")
        else:
            weight = random.randint(1, 10)
            self.network.add_edge(node1, node2, weight=weight)
            self.status_var.set(f"Created edge {node1}-{node2} with weight {weight}")
            self.draw_network()

        # Clear selection
        self.selected_nodes.clear()

    def update_node_combos(self):
        """Update source and destination combo boxes"""
        if self.network:
            node_list = sorted(list(self.network.nodes()), key=lambda x: int(x) if x.isdigit() else x)
            self.source_combo['values'] = node_list
            self.dest_combo['values'] = node_list

    def clear_network(self):
        """Clear the entire network"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the network?"):
            self.network = None
            self.pos = None
            self.selected_nodes.clear()
            self.source_combo['values'] = []
            self.dest_combo['values'] = []
            self.show_welcome_message()
            self.status_var.set("Network cleared")

    def save_network(self):
        """Save network to file"""
        if not self.network:
            messagebox.showerror("Error", "No network to save")
            return

        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", ".json"), ("All files", ".*")]
        )

        if filename:
            try:
                data = {
                    'nodes': list(self.network.nodes()),
                    'edges': [(u, v, self.network[u][v]) for u, v in self.network.edges()],
                    'positions': self.pos
                }
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                self.status_var.set(f"Network saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")

    def load_network(self):
        """Load network from file"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", ".json"), ("All files", ".*")]
        )

        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)

                self.network = nx.Graph()
                self.network.add_nodes_from(data['nodes'])

                for u, v, attrs in data['edges']:
                    self.network.add_edge(u, v, **attrs)

                self.pos = data.get('positions', {})

                # If no positions, generate them
                if not self.pos:
                    self.update_layout()

                self.update_node_combos()
                self.draw_network()
                self.status_var.set(f"Network loaded from {filename}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {str(e)}")

    def customize_colors(self):
        """Open color customization dialog"""
        color_window = tk.Toplevel(self.root)
        color_window.title("Customize Colors")
        color_window.geometry("400x300")
        color_window.configure(bg=self.colors["primary_bg"])

        # Color options
        color_options = [
            ("BFS Algorithm", "bfs"),
            ("DFS Algorithm", "dfs"),
            ("Dijkstra Algorithm", "dijkstra"),
            ("Bellman-Ford Algorithm", "bellman"),
            ("A* Algorithm", "astar")
        ]

        for i, (name, key) in enumerate(color_options):
            frame = tk.Frame(color_window, bg=self.colors["primary_bg"])
            frame.pack(fill='x', padx=10, pady=5)

            tk.Label(frame, text=name, bg=self.colors["primary_bg"],
                     fg=self.colors["text_primary"]).pack(side='left')

            color_btn = tk.Button(frame, text="●", fg=self.colors[key],
                                  bg=self.colors["primary_bg"], font=('Arial', 16),
                                  command=lambda k=key: self.change_color(k))
            color_btn.pack(side='right')

    def change_color(self, color_key):
        """Change color for specific algorithm"""
        color = colorchooser.askcolor(color=self.colors[color_key])[1]
        if color:
            self.colors[color_key] = color
            self.status_var.set(f"Updated {color_key} color")

    def run_algorithms(self):
        """Run selected routing algorithms"""
        if not self.network:
            messagebox.showerror("Error", "Please generate a network first")
            return

        source = self.source_var.get()
        destination = self.dest_var.get()

        if source not in self.network.nodes() or destination not in self.network.nodes():
            messagebox.showerror("Error", "Invalid source or destination node")
            return

        if source == destination:
            messagebox.showwarning("Warning", "Source and destination are the same")
            return

        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.algorithm_stats.clear()

        # Run selected algorithms
        algorithms = []

        if self.bfs_var.get():
            start_time = time.time()
            bfs_result = self.bfs_path(source, destination)
            bfs_time = time.time() - start_time
            algorithms.append(("BFS", bfs_result, self.colors["bfs"], bfs_time))

        if self.dfs_var.get():
            start_time = time.time()
            dfs_result = self.dfs_path(source, destination)
            dfs_time = time.time() - start_time
            algorithms.append(("DFS", dfs_result, self.colors["dfs"], dfs_time))

        if self.dijkstra_var.get():
            start_time = time.time()
            dijkstra_result = self.dijkstra_path(source, destination)
            dijkstra_time = time.time() - start_time
            algorithms.append(("Dijkstra", dijkstra_result, self.colors["dijkstra"], dijkstra_time))

        if self.bellman_var.get():
            start_time = time.time()
            bellman_result = self.bellman_ford_path(source, destination)
            bellman_time = time.time() - start_time
            algorithms.append(("Bellman-Ford", bellman_result, self.colors["bellman"], bellman_time))

        if self.astar_var.get():
            start_time = time.time()
            astar_result = self.astar_path(source, destination)
            astar_time = time.time() - start_time
            algorithms.append(("A*", astar_result, self.colors["astar"], astar_time))

        if not algorithms:
            messagebox.showwarning("Warning", "Please select at least one algorithm")
            return

        # Display results
        self.display_results(algorithms, source, destination)

        # Start visualization
        self.visualize_algorithms(algorithms)

    def bfs_path(self, source, destination):
        """Breadth-First Search pathfinding"""
        try:
            return nx.shortest_path(self.network, source=source, target=destination)
        except nx.NetworkXNoPath:
            return None

    def dfs_path(self, source, destination):
        """Depth-First Search pathfinding"""
        visited = {source}
        stack = [source]
        parent = {source: None}

        while stack:
            node = stack.pop()
            if node == destination:
                path = []
                while node is not None:
                    path.append(node)
                    node = parent[node]
                return path[::-1]

            for neighbor in self.network.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
                    parent[neighbor] = node
        return None

    def dijkstra_path(self, source, destination):
        """Dijkstra's shortest path algorithm"""
        try:
            return nx.dijkstra_path(self.network, source=source, target=destination, weight='weight')
        except nx.NetworkXNoPath:
            return None

    def bellman_ford_path(self, source, destination):
        """Bellman-Ford shortest path algorithm"""
        try:
            return nx.bellman_ford_path(self.network, source=source, target=destination, weight='weight')
        except nx.NetworkXNoPath:
            return None

    def astar_path(self, source, destination):
        """A* pathfinding algorithm"""
        try:
            def heuristic(u, v):
                # Euclidean distance heuristic
                if self.pos and u in self.pos and v in self.pos:
                    x1, y1 = self.pos[u]
                    x2, y2 = self.pos[v]
                    return np.sqrt((x1 - x2) * 2 + (y1 - y2) * 2)
                return 0

            return nx.astar_path(self.network, source, destination, heuristic=heuristic, weight='weight')
        except nx.NetworkXNoPath:
            return None

    def display_results(self, algorithms, source, destination):
        """Display algorithm results and statistics"""
        self.results_text.insert(tk.END, f"🎯 Route Analysis: {source} → {destination}\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")

        # Calculate statistics for each algorithm
        results_data = []

        for name, path, color, exec_time in algorithms:
            if path:
                # Calculate path cost
                path_cost = 0
                for i in range(len(path) - 1):
                    path_cost += self.network[path[i]][path[i + 1]]['weight']

                hop_count = len(path) - 1
                results_data.append((name, path, path_cost, hop_count, exec_time))

                # Store statistics
                self.algorithm_stats[name] = {
                    'path': path,
                    'cost': path_cost,
                    'hops': hop_count,
                    'time': exec_time
                }

                # Display result
                self.results_text.insert(tk.END, f"🔹 {name}:\n")
                self.results_text.insert(tk.END, f"   Path: {' → '.join(path)}\n")
                self.results_text.insert(tk.END, f"   Cost: {path_cost} units\n")
                self.results_text.insert(tk.END, f"   Hops: {hop_count}\n")
                self.results_text.insert(tk.END, f"   Time: {exec_time:.6f}s\n\n")
            else:
                self.results_text.insert(tk.END, f"🔹 {name}: No path found\n\n")

        # Performance comparison
        if results_data:
            self.results_text.insert(tk.END, "📊 Performance Comparison:\n")
            self.results_text.insert(tk.END, "-" * 30 + "\n")

            # Sort by cost
            results_data.sort(key=lambda x: x[2])

            for i, (name, path, cost, hops, exec_time) in enumerate(results_data):
                rank = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i + 1}."
                self.results_text.insert(tk.END, f"{rank} {name}: {cost} units\n")

        # Update statistics tab
        self.update_statistics_display()

    def update_statistics_display(self):
        """Update the statistics tab with detailed metrics"""
        self.stats_text.delete(1.0, tk.END)

        if not self.algorithm_stats:
            self.stats_text.insert(tk.END, "No statistics available. Run algorithms first.")
            return

        self.stats_text.insert(tk.END, "🏆 ALGORITHM PERFORMANCE STATISTICS\n")
        self.stats_text.insert(tk.END, "=" * 50 + "\n\n")

        # Network info
        if self.network:
            self.stats_text.insert(tk.END, f"📊 Network Information:\n")
            self.stats_text.insert(tk.END, f"   Nodes: {len(self.network.nodes())}\n")
            self.stats_text.insert(tk.END, f"   Edges: {len(self.network.edges())}\n")
            self.stats_text.insert(tk.END, f"   Density: {nx.density(self.network):.3f}\n")
            self.stats_text.insert(tk.END, f"   Connected: {'Yes' if nx.is_connected(self.network) else 'No'}\n\n")

        # Algorithm comparison table
        self.stats_text.insert(tk.END,
                               f"{'Algorithm':<15} {'Cost':<8} {'Hops':<6} {'Time (ms)':<10} {'Efficiency':<10}\n")
        self.stats_text.insert(tk.END, "-" * 60 + "\n")

        best_cost = min(stats['cost'] for stats in self.algorithm_stats.values() if stats['cost'] > 0)

        for name, stats in self.algorithm_stats.items():
            cost = stats['cost']
            hops = stats['hops']
            time_ms = stats['time'] * 1000
            efficiency = best_cost / cost if cost > 0 else 0

            self.stats_text.insert(tk.END, f"{name:<15} {cost:<8} {hops:<6} {time_ms:<10.3f} {efficiency:<10.3f}\n")

    def visualize_algorithms(self, algorithms):
        """Visualize algorithm paths with animations"""
        if not algorithms:
            return

        self.status_var.set("Starting algorithm visualization...")

        # Show algorithms one by one
        for i, (name, path, color, exec_time) in enumerate(algorithms):
            if path:
                self.visualize_single_algorithm(name, path, color)
                time.sleep(2)  # Pause between algorithms

        self.status_var.set("Algorithm visualization complete")

    def visualize_single_algorithm(self, algorithm_name, path, color):
        """Visualize a single algorithm's path"""
        if not path:
            return

        # Stop any current animation
        if hasattr(self, 'animation') and self.animation is not None:
            try:
                self.animation.event_source.stop()
            except:
                pass

        # Redraw network
        self.draw_network()

        # Highlight the path
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(self.network, self.pos, edgelist=path_edges,
                               edge_color=color, width=5, alpha=0.8, ax=self.ax)

        # Create packet animation
        if not hasattr(self, 'packet') or self.packet is None:
            self.packet, = self.ax.plot([], [], 'o', color='yellow', markersize=15,
                                        markeredgecolor='black', markeredgewidth=2)

        # Get positions along path
        path_positions = [self.pos[node] for node in path]

        def init_animation():
            self.packet.set_data([], [])
            return self.packet,

        def animate_packet(frame):
            if frame < len(path_positions):
                x, y = path_positions[frame]
                self.packet.set_data([x], [y])
            return self.packet,

        # Create and start animation
        self.animation = animation.FuncAnimation(
            self.fig, animate_packet, init_func=init_animation,
            frames=len(path_positions), interval=self.speed_var.get(),
            repeat=False, blit=True
        )

        # Update title and canvas
        self.ax.set_title(f"🚀 {algorithm_name} Pathfinding in Progress",
                          fontsize=14, color='white', weight='bold')
        self.canvas.draw()

        self.status_var.set(f"Visualizing {algorithm_name} algorithm")

    def pause_animation(self):
        """Pause current animation"""
        if hasattr(self, 'animation') and self.animation is not None:
            try:
                self.animation.pause()
                self.status_var.set("Animation paused")
            except:
                pass

    def stop_animation(self):
        """Stop current animation"""
        if hasattr(self, 'animation') and self.animation is not None:
            try:
                self.animation.event_source.stop()
                self.status_var.set("Animation stopped")
            except:
                pass

    def refresh_visualization(self):
        """Refresh the visualization"""
        if self.network:
            self.draw_network()
            self.status_var.set("Visualization refreshed")
        else:
            self.show_welcome_message()

    def clear_stats(self):
        """Clear statistics"""
        self.algorithm_stats.clear()
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, "Statistics cleared.")
        self.status_var.set("Statistics cleared")

    def main(self):
        root = tk.Tk()
        app = ModernNetworkRoutingSimulator(root)
        root.mainloop()

    if __name__ == "_main_":
        main()
def main():
    try:
        root = tk.Tk()
        app = ModernNetworkRoutingSimulator(root)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to close...")

if __name__ == "__main__":
    main()
