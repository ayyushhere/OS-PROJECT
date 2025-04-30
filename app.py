import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from disk_scheduling import DiskScheduler
from page_replacement import PageReplacement

# Configure the page
st.set_page_config(
    page_title="OS Algorithms Simulator",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clear, high-contrast theme for maximum visibility
st.markdown("""
    <style>
        /* Base theme variables */
        :root {
            --text-primary: #0F172A;
            --text-secondary: #334155;
            --text-muted: #64748B;
            --bg-primary: #F8FAFC;
            --bg-card: #FFFFFF;
            --primary-color: #2563EB;
            --primary-light: #DBEAFE;
            --primary-dark: #1E40AF;
            --accent-color: #10B981;
            --accent-light: #D1FAE5;
            --warning-color: #F59E0B;
            --error-color: #EF4444;
            --border-color: #E2E8F0;
            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --corner-radius: 8px;
        }
        
        /* Reset and base styles */
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.5;
        }
        
        /* Ensure the main container has proper background */
        .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"] {
            background-color: var(--bg-primary);
        }
        
        /* Ensure all text has sufficient contrast */
        p, h1, h2, h3, h4, h5, h6, span, div, label, .stMarkdown, [data-testid="stMarkdownContainer"] p {
            color: var(--text-primary);
        }
        
        /* Fix header styling */
        h1 {
            font-size: 2.25rem;
            font-weight: 800;
            color: var(--primary-dark);
            margin: 1rem 0;
        }
        
        h2 {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--primary-dark);
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.25rem;
            border-bottom: 2px solid var(--primary-light);
        }
        
        h3 {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--primary-dark);
            margin: 1rem 0 0.75rem 0;
        }
        
        /* Card containers for each section */
        .card {
            background-color: var(--bg-card);
            border-radius: var(--corner-radius);
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
            margin-bottom: 1.5rem;
            border: 1px solid var(--border-color);
        }
        
        /* High contrast button styling */
        .stButton > button {
            background-color: var(--primary-color);
            color: white;
            font-weight: 600;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: var(--corner-radius);
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            background-color: var(--primary-dark);
            box-shadow: var(--shadow-md);
        }
        
        /* Form elements with better visibility */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            border: 2px solid var(--border-color);
            border-radius: var(--corner-radius);
            padding: 0.75rem;
            font-size: 1rem;
            color: var(--text-primary);
            background-color: white;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px var(--primary-light);
        }
        
        /* Select box with better visibility */
        .stSelectbox > div {
            margin-bottom: 1rem;
        }
        
        .stSelectbox > div > div > div {
            border: 2px solid var(--border-color);
            border-radius: var(--corner-radius);
            background-color: white;
        }
        
        .stSelectbox > div > div > div:hover {
            border-color: var(--primary-color);
        }
        
        .stSelectbox [data-baseweb="select"] [data-baseweb="popover"],
        .stSelectbox [data-baseweb="select"] [data-baseweb="menu"],
        .stSelectbox [role="listbox"],
        .stSelectbox [role="option"] {
            background-color: white;
            color: var(--text-primary);
        }
        
        /* Tab styling for maximum visibility */
        .stTabs {
            background-color: var(--bg-card);
            border-radius: var(--corner-radius);
            padding: 0.5rem;
            box-shadow: var(--shadow-sm);
            margin-bottom: 2rem;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            background-color: var(--bg-primary);
            border-radius: var(--corner-radius);
            padding: 0.25rem;
            gap: 0.25rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: var(--corner-radius);
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 1rem;
            color: var(--text-secondary);
            background-color: transparent;
            border: none;
            transition: all 0.2s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--primary-color);
            color: white;
            box-shadow: var(--shadow-sm);
        }
        
        /* Label styling */
        label, .stTextInput label, .stNumberInput label, .stSelectbox label {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }
        
        /* Metrics with better visibility */
        .stMetric {
            background-color: var(--bg-card);
            padding: 1rem;
            border-radius: var(--corner-radius);
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--border-color);
        }
        
        .stMetric [data-testid="metric-container"] {
            justify-content: center;
            text-align: center;
        }
        
        .stMetric [data-testid="metric-value"] {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--primary-color);
        }
        
        .stMetric [data-testid="metric-label"] {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-secondary);
        }
        
        /* DataFrame styling */
        [data-testid="stDataFrame"] {
            border-radius: var(--corner-radius);
            overflow: hidden;
            border: 1px solid var(--border-color);
        }
        
        /* Ensure plots have proper visibility */
        .js-plotly-plot .plotly .main-svg,
        [data-testid="stPlotlyChart"] > div > div > div {
            background-color: white !important;
        }
        
        .js-plotly-plot .plotly .bg {
            fill: white !important;
        }
        
        .js-plotly-plot .plotly .bg text,
        .js-plotly-plot .plotly .gtitle,
        .js-plotly-plot .plotly .xtick text,
        .js-plotly-plot .plotly .ytick text {
            fill: var(--text-primary) !important;
        }
        
        /* Alert styling */
        .stAlert {
            background-color: var(--bg-card);
            border-radius: var(--corner-radius);
            border-left: 4px solid var(--primary-color);
            box-shadow: var(--shadow-sm);
            padding: 1rem;
        }
        
        .element-container:has(.stAlert) {
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        
        /* Fix empty container styling */
        .element-container:empty {
            display: none !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Hide Streamlit branding */
        #MainMenu, footer, header {
            visibility: hidden;
        }
        
        /* Custom classes for sections */
        .section-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--primary-dark);
            border-left: 4px solid var(--primary-color);
            padding-left: 0.75rem;
            margin: 1rem 0;
        }
        
        .info-box {
            background-color: var(--primary-light);
            border-radius: var(--corner-radius);
            padding: 1rem;
            border-left: 4px solid var(--primary-color);
            margin: 1rem 0;
        }
        
        .result-box {
            background-color: var(--accent-light);
            border-radius: var(--corner-radius);
            padding: 1rem;
            border-left: 4px solid var(--accent-color);
            margin: 1rem 0;
        }
        
        /* Ensure matplotlib has dark elements on light backgrounds */
        .matplotlib-figure text {
            fill: var(--text-primary) !important;
        }
        
        .matplotlib-figure .axis {
            stroke: var(--text-primary) !important;
        }
        
        /* Ensure plotly charts have good visibility */
        [data-testid="stPlotlyChart"] {
            background-color: white;
            border-radius: var(--corner-radius);
            box-shadow: var(--shadow-sm);
            padding: 1rem;
            border: 1px solid var(--border-color);
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# Create a clean header with high visibility
st.markdown("""
<div style="text-align: center; padding: 1.5rem 0; margin-bottom: 2rem;">
    <h1>OS Algorithms Simulator 🖥️</h1>
    <p style="font-size: 1.1rem; color: #334155; max-width: 800px; margin: 0 auto;">
        Interactive visualization of disk scheduling and page replacement algorithms used in operating systems.
    </p>
</div>
""", unsafe_allow_html=True)

# Create tabs with clear labels
tabs = st.tabs(["💽 Disk Scheduling", "📊 Page Replacement"])

with tabs[0]:  # Disk Scheduling Tab
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <h2>Disk Scheduling Algorithms</h2>
    <p style="color: #334155; margin-bottom: 1.5rem;">
        These algorithms determine the order in which disk I/O requests are serviced to minimize seek time and maximize throughput.
    </p>
    """, unsafe_allow_html=True)
    
    # Create a two-column layout
    col1, col2 = st.columns([1, 2])
    
    with col1:  # Input column
        st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)
        
        # Algorithm selection
        disk_algo = st.selectbox(
            "Select Algorithm",
            ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"],
            help="Choose the disk scheduling algorithm to simulate"
        )
        
        # Show algorithm description based on selection
        if disk_algo == "FCFS":
            st.markdown('<div class="info-box">First Come First Served: Requests are serviced in the order they arrive.</div>', unsafe_allow_html=True)
        elif disk_algo == "SSTF":
            st.markdown('<div class="info-box">Shortest Seek Time First: Services the request closest to the current head position.</div>', unsafe_allow_html=True)
        elif disk_algo == "SCAN":
            st.markdown('<div class="info-box">SCAN (Elevator): Head moves in one direction servicing requests until it reaches the end, then reverses.</div>', unsafe_allow_html=True)
        elif disk_algo == "C-SCAN":
            st.markdown('<div class="info-box">Circular SCAN: Like SCAN but head returns to the beginning without servicing requests on the return trip.</div>', unsafe_allow_html=True)
        elif disk_algo == "LOOK":
            st.markdown('<div class="info-box">LOOK: Similar to SCAN but only goes as far as the last request in each direction.</div>', unsafe_allow_html=True)
        elif disk_algo == "C-LOOK":
            st.markdown('<div class="info-box">Circular LOOK: Like C-SCAN but only goes as far as the last request in each direction.</div>', unsafe_allow_html=True)
        
        # Request sequence input with example
        st.markdown('<label for="req_seq">Request Sequence (comma-separated)</label>', unsafe_allow_html=True)
        request_sequence = st.text_input(
            label="Request Sequence",
            label_visibility="collapsed",
            key="req_seq",
            placeholder="Example: 98, 183, 37, 122, 14, 124, 65, 67"
        )
        
        # Initial head position
        head_pos = st.number_input(
            "Initial Head Position",
            min_value=0,
            value=50,
            step=1,
            help="The starting position of the disk head"
        )
        
        # Total cylinders
        total_cylinders = st.number_input(
            "Total Cylinders",
            min_value=1,
            value=200,
            step=1,
            help="The maximum number of cylinders on the disk"
        )
        
        # Direction (for SCAN and LOOK)
        if disk_algo in ["SCAN", "C-SCAN", "LOOK", "C-LOOK"]:
            direction = st.selectbox(
                "Direction",
                ["up", "down"],
                help="The initial direction of the head movement"
            )
        else:
            direction = "up"  # Default value
        
        # Simulate button with high visibility
        st.markdown("<br>", unsafe_allow_html=True)
        simulate_disk = st.button("▶️ Simulate Algorithm", use_container_width=True)
    
    with col2:  # Results column
        st.markdown('<div class="section-title">Visualization & Results</div>', unsafe_allow_html=True)
        
        # Container for results
        result_container = st.container()
        
        if simulate_disk:
            try:
                # Validate request sequence
                if not request_sequence:
                    st.error("Request sequence cannot be empty. Please enter comma-separated numbers.")
                else:
                    requests = [int(x.strip()) for x in request_sequence.split(",") if x.strip()]
                    
                    # Validate requests are within cylinder range
                    if max(requests) >= total_cylinders:
                        st.error(f"All requests must be less than total cylinders ({total_cylinders})")
                    # Validate head position is within cylinder range
                    elif head_pos >= total_cylinders:
                        st.error(f"Head position must be less than total cylinders ({total_cylinders})")
                    else:
                        # Create scheduler instance
                        scheduler = DiskScheduler()
                        
                        # Execute selected algorithm
                        if disk_algo == 'FCFS':
                            sequence, seek_time = scheduler.fcfs(requests, head_pos, total_cylinders)
                        elif disk_algo == 'SSTF':
                            sequence, seek_time = scheduler.sstf(requests, head_pos, total_cylinders)
                        elif disk_algo == 'SCAN':
                            sequence, seek_time = scheduler.scan(requests, head_pos, total_cylinders, direction)
                        elif disk_algo == 'C-SCAN':
                            sequence, seek_time = scheduler.cscan(requests, head_pos, total_cylinders)
                        elif disk_algo == 'LOOK':
                            sequence, seek_time = scheduler.look(requests, head_pos, total_cylinders, direction)
                        else:  # C-LOOK
                            sequence, seek_time = scheduler.clook(requests, head_pos, total_cylinders)
                        
                        # Display results
                        with result_container:
                            # Create DataFrame for visualization
                            df = pd.DataFrame({
                                'Order': range(len(sequence)),
                                'Cylinder': sequence
                            })
                            
                            # Make sure we have data before plotting
                            if len(sequence) > 0:
                                # Calculate appropriate y-axis range
                                min_cyl = min(sequence)
                                max_cyl = max(sequence)
                                # If all values are the same, ensure some visible range
                                if min_cyl == max_cyl:
                                    y_padding = 5
                                else:
                                    y_padding = (max_cyl - min_cyl) * 0.1 or 10
                                y_min = max(0, min_cyl - y_padding)
                                y_max = min(total_cylinders, max_cyl + y_padding)
                                
                                # Create DataFrame for plotting (guaranteed to have at least one row)
                                df = pd.DataFrame({
                                    'Order': range(len(sequence)),
                                    'Cylinder': sequence
                                })
                                
                                # Use matplotlib for classic disk scheduling style (always visible)
                                import matplotlib.pyplot as plt
                                fig, ax = plt.subplots(figsize=(10, 5))
                                
                                # Draw the seek sequence with arrows
                                for i in range(len(sequence)-1):
                                    ax.annotate(
                                        '',
                                        xy=(sequence[i+1], i+1),
                                        xytext=(sequence[i], i),
                                        arrowprops=dict(facecolor='#111827', edgecolor='#111827', arrowstyle='->', lw=2),
                                        size=15
                                    )
                                # Draw the points
                                ax.plot(sequence, range(len(sequence)), 'o-', color='#111827', markersize=8, linewidth=2)
                                
                                ax.set_xlabel('Cylinder Number', fontsize=13, color='#111827')
                                ax.set_ylabel('Step', fontsize=13, color='#111827')
                                ax.set_title(f'{disk_algo} Disk Scheduling Algorithm', fontsize=15, color='#111827')
                                ax.grid(True, which='both', linestyle='--', color='#CBD5E1', alpha=0.7)
                                ax.set_facecolor('white')
                                fig.patch.set_facecolor('white')
                                ax.tick_params(axis='x', colors='#111827')
                                ax.tick_params(axis='y', colors='#111827')
                                
                                st.pyplot(fig)
                                plt.close(fig)
                                

                                # Show metrics in a clear layout
                                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Total Seek Time", seek_time)
                                with col2:
                                    st.metric("Average Seek Time", round(seek_time / len(requests), 2))
                                
                                # Display sequence clearly
                                st.markdown("""
                                <div style="margin-top: 1rem;">
                                    <strong style="color: #0F172A; font-size: 1.1rem;">Head Movement Sequence:</strong>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Format the sequence display nicely
                                sequence_df = pd.DataFrame({
                                    "Step": range(len(sequence)),
                                    "Cylinder": sequence
                                })
                                st.dataframe(sequence_df, use_container_width=True, hide_index=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                            else:
                                st.error("No data to display. Please check algorithm implementation.")
            except ValueError as e:
                st.error(f"Input Error: {str(e)}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
                st.exception(e)  # Shows the full traceback for debugging
                # Validate request sequence
                if not request_sequence:
                    st.error("Request sequence cannot be empty. Please enter comma-separated numbers.")
                else:
                    requests = [int(x.strip()) for x in request_sequence.split(",") if x.strip()]
                    
                    # Validate requests are within cylinder range
                    if max(requests) >= total_cylinders:
                        st.error(f"All requests must be less than total cylinders ({total_cylinders})")
                    # Validate head position is within cylinder range
                    elif head_pos >= total_cylinders:
                        st.error(f"Head position must be less than total cylinders ({total_cylinders})")
                    else:
                        # Create scheduler instance
                        scheduler = DiskScheduler()
                        
                        # Execute selected algorithm
                        if disk_algo == 'FCFS':
                            sequence, seek_time = scheduler.fcfs(requests, head_pos, total_cylinders)
                        elif disk_algo == 'SSTF':
                            sequence, seek_time = scheduler.sstf(requests, head_pos, total_cylinders)
                        elif disk_algo == 'SCAN':
                            sequence, seek_time = scheduler.scan(requests, head_pos, total_cylinders, direction)
                        elif disk_algo == 'C-SCAN':
                            sequence, seek_time = scheduler.cscan(requests, head_pos, total_cylinders)
                        elif disk_algo == 'LOOK':
                            sequence, seek_time = scheduler.look(requests, head_pos, total_cylinders, direction)
                        else:  # C-LOOK
                            sequence, seek_time = scheduler.clook(requests, head_pos, total_cylinders)
                        
                        # Display results
                        with result_container:
                            # Create DataFrame for visualization
                            df = pd.DataFrame({
                                'Order': range(len(sequence)),
                                'Cylinder': sequence
                            })
                            
                            # Create Plotly figure with high visibility settings
                            fig = px.line(
                                df, 
                                x='Order', 
                                y='Cylinder', 
                                markers=True, 
                                title=f"{disk_algo} Disk Scheduling Algorithm"
                            )
                            
                            fig.update_layout(
                                xaxis_title="Request Order",
                                yaxis_title="Cylinder Number",
                                height=400,
                                font=dict(family="Inter, sans-serif", size=14, color="#334155"),
                                title_font=dict(family="Inter, sans-serif", size=20, color="#1E40AF"),
                                plot_bgcolor='white',
                                paper_bgcolor='white',
                                xaxis=dict(gridcolor='#E2E8F0', zeroline=False),
                                yaxis=dict(gridcolor='#E2E8F0', zeroline=True, zerolinecolor='#CBD5E1'),
                                yaxis_range=[0, total_cylinders],
                                margin=dict(t=60, r=30, b=60, l=60),
                                hoverlabel=dict(bgcolor="white", font_size=14)
                            )
                            
                            fig.update_traces(
                                line=dict(color='#2563EB', width=3),
                                marker=dict(size=10, color='#1E40AF', line=dict(width=2, color='white'))
                            )
                            
                            # Add initial head position as a horizontal line
                            fig.add_hline(
                                y=head_pos, 
                                line_dash="dash", 
                                line_color="#F59E0B", 
                                annotation_text="Initial Head Position",
                                annotation_position="bottom right"
                            )
                            
                            # Display the chart only if data is valid
                            if df.shape[0] > 0 and len(sequence) > 1:
                                min_cyl = int(df['Cylinder'].min())
                                max_cyl = int(df['Cylinder'].max())
                                fig.update_layout(yaxis_range=[min_cyl - 1, max_cyl + 1])
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.warning("No valid data to plot. Please check your input and algorithm.")
                            
                            # Show metrics in a clear layout
                            st.markdown('<div class="result-box">', unsafe_allow_html=True)
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Total Seek Time", seek_time)
                            with col2:
                                st.metric("Average Seek Time", round(seek_time / len(requests), 2))
                            
                            # Display sequence clearly
                            st.markdown("""
                            <div style="margin-top: 1rem;">
                                <strong style="color: #0F172A; font-size: 1.1rem;">Head Movement Sequence:</strong>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Format the sequence display nicely
                            sequence_df = pd.DataFrame({
                                "Step": range(len(sequence)),
                                "Cylinder": sequence
                            })
                            st.dataframe(sequence_df, use_container_width=True, hide_index=True)
                            st.markdown('</div>', unsafe_allow_html=True)
            except ValueError as e:
                st.error(f"Input Error: {str(e)}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
                
    st.markdown('</div>', unsafe_allow_html=True)  # Close card

with tabs[1]:  # Page Replacement Tab
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <h2>Page Replacement Algorithms</h2>
    <p style="color: #334155; margin-bottom: 1.5rem;">
        These algorithms decide which memory pages to swap out when a new page needs to be loaded into memory that is already full.
    </p>
    """, unsafe_allow_html=True)
    
    # Create a two-column layout
    col1, col2 = st.columns([1, 2])
    
    with col1:  # Input column
        st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)
        
        # Algorithm selection
        page_algo = st.selectbox(
            "Select Algorithm",
            ["FIFO", "LRU", "Optimal", "LFU"],
            help="Choose the page replacement algorithm to simulate"
        )
        
        # Show algorithm description based on selection
        if page_algo == "FIFO":
            st.markdown('<div class="info-box">First In First Out: Replaces the oldest page in memory.</div>', unsafe_allow_html=True)
        elif page_algo == "LRU":
            st.markdown('<div class="info-box">Least Recently Used: Replaces the page that hasn\'t been used for the longest time.</div>', unsafe_allow_html=True)
        elif page_algo == "Optimal":
            st.markdown('<div class="info-box">Optimal: Replaces the page that won\'t be used for the longest time in the future.</div>', unsafe_allow_html=True)
        elif page_algo == "LFU":
            st.markdown('<div class="info-box">Least Frequently Used: Replaces the page with the lowest usage frequency.</div>', unsafe_allow_html=True)
        
        # Reference string input with example
        st.markdown('<label for="ref_string">Reference String (comma-separated)</label>', unsafe_allow_html=True)
        ref_string = st.text_input(
            label="Reference String",
            label_visibility="collapsed",
            key="ref_string",
            placeholder="Example: 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2"
        )
        
        # Number of frames
        num_frames = st.number_input(
            "Number of Frames",
            min_value=1,
            value=3,
            step=1,
            help="The number of available page frames in memory"
        )
        
        # Simulate button with high visibility
        st.markdown("<br>", unsafe_allow_html=True)
        simulate_page = st.button("▶️ Simulate Algorithm", key="sim_page", use_container_width=True)
    
    with col2:  # Results column
        st.markdown('<div class="section-title">Visualization & Results</div>', unsafe_allow_html=True)
        
        # Container for results
        page_result_container = st.container()
        
        if simulate_page:
            try:
                # Validate reference string
                if not ref_string:
                    st.error("Reference string cannot be empty. Please enter comma-separated numbers.")
                else:
                    ref_sequence = [int(x.strip()) for x in ref_string.split(",") if x.strip()]
                    
                    # Validate all page numbers are non-negative
                    if any(page < 0 for page in ref_sequence):
                        st.error("All page numbers must be non-negative")
                    else:
                        # Create page replacement instance
                        replacer = PageReplacement()
                        
                        # Execute selected algorithm
                        if page_algo == 'FIFO':
                            history, page_faults = replacer.fifo(ref_sequence, num_frames)
                        elif page_algo == 'LRU':
                            history, page_faults = replacer.lru(ref_sequence, num_frames)
                        elif page_algo == 'Optimal':
                            history, page_faults = replacer.optimal(ref_sequence, num_frames)
                        else:  # LFU
                            history, page_faults = replacer.lfu(ref_sequence, num_frames)
                        
                        # Display results with much better visibility
                        with page_result_container:
                            # Display reference string clearly
                            st.markdown("""
                            <div style="background-color: #EFF6FF; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; border-left: 4px solid #2563EB;">
                                <strong style="color: #1E40AF;">Reference String:</strong>
                                <div style="font-family: monospace; font-size: 1.1rem; margin-top: 0.5rem; overflow-x: auto; white-space: nowrap;">
                            """, unsafe_allow_html=True)
                            
                            # Show reference sequence with page fault indicators
                            for i, page in enumerate(ref_sequence):
                                is_fault = i < len(history) and (i == 0 or history[i] != history[i-1])
                                if is_fault:
                                    st.markdown(f"""
                                    <span style="display: inline-block; padding: 0.3rem 0.6rem; background-color: #FEE2E2; 
                                    color: #B91C1C; border-radius: 6px; margin-right: 0.5rem; font-weight: 600;">{page} ⚠️</span>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.markdown(f"""
                                    <span style="display: inline-block; padding: 0.3rem 0.6rem; background-color: #DCFCE7; 
                                    color: #166534; border-radius: 6px; margin-right: 0.5rem; font-weight: 600;">{page} ✓</span>
                                    """, unsafe_allow_html=True)
                            
                            st.markdown("</div></div>", unsafe_allow_html=True)
                            
                            # Show metrics clearly
                            st.markdown('<div class="result-box">', unsafe_allow_html=True)
                            metric_cols = st.columns(3)
                            with metric_cols[0]:
                                st.metric("Total Page Faults", page_faults)
                            with metric_cols[1]:
                                hit_ratio = (len(ref_sequence) - page_faults) / len(ref_sequence)
                                st.metric("Hit Ratio", f"{hit_ratio:.2%}")
                            with metric_cols[2]:
                                fault_ratio = page_faults / len(ref_sequence)
                                st.metric("Fault Ratio", f"{fault_ratio:.2%}")
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Create a better frame state visualization
                            st.markdown("""
                            <div style="margin-top: 1.5rem;">
                                <strong style="color: #0F172A; font-size: 1.1rem;">Frame States by Step:</strong>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Build a more readable frame state history
                            frame_states = []
                            
                            for i, frame_state in enumerate(history):
                                state_dict = {"Step": i+1, "Reference": ref_sequence[i]}
                                
                                # Create actual frame content
                                for j in range(num_frames):
                                    if j < len(frame_state):
                                        state_dict[f"Frame {j+1}"] = frame_state[j]
                                    else:
                                        state_dict[f"Frame {j+1}"] = ""
                                
                                # Is this a page fault?
                                is_fault = i == 0 or frame_state != history[i-1]
                                state_dict["Fault"] = "Yes ⚠️" if is_fault else "No ✓"
                                
                                frame_states.append(state_dict)
                            
                            # Convert to DataFrame and display with better styling
                            history_df = pd.DataFrame(frame_states)
                            st.dataframe(
                                history_df,
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "Step": st.column_config.NumberColumn("Step", format="%d"),
                                    "Reference": st.column_config.NumberColumn("Page Ref", format="%d"),
                                    "Fault": st.column_config.TextColumn("Page Fault")
                                }
                            )
                            
                            # Create a better visualization
                            st.markdown("""
                            <div style="margin-top: 1.5rem;">
                                <strong style="color: #0F172A; font-size: 1.1rem;">Visual Representation:</strong>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Prepare visualization with matplotlib for better visibility
                            fig, ax = plt.subplots(figsize=(12, 6))
                            
                            # Better styling with clear colors
                            ax.set_facecolor('#F8FAFC')
                            fig.patch.set_facecolor('#F8FAFC')
                            
                            # Setup title and labels with better visibility
                            # Setup title and labels with better visibility
                            ax.set_title(f"{page_algo} Page Replacement Algorithm", fontsize=16, fontweight='bold', color='#1E40AF')
                            ax.set_xlabel('Page Reference Sequence', fontsize=12, fontweight='bold', color='#334155')
                            ax.set_ylabel('Frames', fontsize=12, fontweight='bold', color='#334155')
                            
                            # Set axis limits
                            ax.set_xlim(-0.5, len(ref_sequence) - 0.5)
                            ax.set_ylim(-0.5, num_frames - 0.5)
                            
                            # Set grid for better readability
                            ax.grid(True, linestyle='--', alpha=0.6, color='#CBD5E1')
                            
                            # Custom y-ticks for frame numbers
                            ax.set_yticks(range(num_frames))
                            ax.set_yticklabels([f"Frame {i+1}" for i in range(num_frames)])
                            
                            # Custom x-ticks for reference sequence
                            ax.set_xticks(range(len(ref_sequence)))
                            ax.set_xticklabels(ref_sequence)
                            
                            # Color mapping for pages
                            unique_pages = set()
                            for seq in ref_sequence:
                                unique_pages.add(seq)
                            
                            # Create a colormap with distinct colors
                            import matplotlib.colors as mcolors
                            colors = list(mcolors.TABLEAU_COLORS.values())
                            if len(unique_pages) > len(colors):
                                # If more pages than colors, use a colormap
                                cmap = plt.cm.get_cmap('tab20', len(unique_pages))
                                colors = [cmap(i) for i in range(len(unique_pages))]
                            
                            # Create a mapping of page to color
                            color_map = {}
                            for i, page in enumerate(unique_pages):
                                color_map[page] = colors[i % len(colors)]
                            
                            # Plot each cell with corresponding page value and color
                            for i, frame_state in enumerate(history):
                                for j in range(min(len(frame_state), num_frames)):
                                    page = frame_state[j]
                                    if page is not None and page != "":
                                        # Use lighter version of the color for the cell
                                        rgba_color = mcolors.to_rgba(color_map[page])
                                        lighter_color = (rgba_color[0], rgba_color[1], rgba_color[2], 0.5)
                                        
                                        # Draw colored cell
                                        rect = plt.Rectangle(
                                            (i - 0.4, j - 0.4),
                                            0.8, 0.8,
                                            facecolor=lighter_color,
                                            edgecolor=color_map[page],
                                            linewidth=2,
                                            alpha=0.8
                                        )
                                        ax.add_patch(rect)
                                        
                                        # Add text for page number
                                        ax.text(
                                            i, j,
                                            str(page),
                                            fontsize=12,
                                            ha='center',
                                            va='center',
                                            fontweight='bold',
                                            color='#0F172A'
                                        )
                            
                            # Mark page faults with red outline
                            for i in range(len(history)):
                                is_fault = i == 0 or history[i] != history[i-1]
                                if is_fault:
                                    rect = plt.Rectangle(
                                        (i - 0.5, -0.5),
                                        1, num_frames,
                                        fill=False,
                                        edgecolor='#EF4444',
                                        linewidth=2,
                                        linestyle='-',
                                        alpha=0.7
                                    )
                                    ax.add_patch(rect)
                                    ax.text(
                                        i, num_frames - 0.2,
                                        "FAULT",
                                        color='#B91C1C',
                                        fontsize=8,
                                        ha='center',
                                        va='top',
                                        fontweight='bold',
                                        bbox=dict(
                                            boxstyle="round,pad=0.2",
                                            facecolor='#FEE2E2',
                                            edgecolor='#EF4444',
                                            alpha=0.8
                                        )
                                    )
                            
                            # Add a legend for the pages
                            handles = []
                            for page in sorted(unique_pages):
                                color = color_map[page]
                                handle = plt.Line2D(
                                    [0], [0],
                                    marker='s',
                                    color='w',
                                    markerfacecolor=color,
                                    markeredgecolor=color,
                                    markersize=10,
                                    label=f"Page {page}"
                                )
                                handles.append(handle)
                            
                            legend = ax.legend(
                                handles=handles,
                                loc='upper center',
                                bbox_to_anchor=(0.5, -0.12),
                                ncol=min(8, len(unique_pages)),
                                frameon=True,
                                fancybox=True,
                                shadow=True,
                                fontsize=10
                            )
                            
                            # Adjust figure for better layout
                            plt.tight_layout()
                            
                            # Show the visualization
                            fig.tight_layout()
                            st.pyplot(fig)
                            plt.close(fig)  # Ensure the figure is closed to avoid display issues
                            
                            # Add explanation of the algorithm
                            st.markdown('<div class="info-box">', unsafe_allow_html=True)
                            st.markdown(f"<strong>Algorithm Explanation: {page_algo}</strong>", unsafe_allow_html=True)
                            
                            if page_algo == 'FIFO':
                                st.markdown("""
                                <p>The <strong>First-In-First-Out (FIFO)</strong> algorithm replaces the oldest page in memory. It works as follows:</p>
                                <ol>
                                    <li>When a page is requested, check if it's already in memory</li>
                                    <li>If not (page fault), remove the page that was loaded first (oldest)</li>
                                    <li>Load the new page into that frame</li>
                                </ol>
                                <p>FIFO is simple to implement but can suffer from "Belady's anomaly", where increasing the number of frames can sometimes increase page faults.</p>
                                """, unsafe_allow_html=True)
                            elif page_algo == 'LRU':
                                st.markdown("""
                                <p>The <strong>Least Recently Used (LRU)</strong> algorithm replaces the page that hasn't been used for the longest time. It works as follows:</p>
                                <ol>
                                    <li>When a page is requested, check if it's already in memory</li>
                                    <li>If not (page fault), remove the page that was accessed longest ago</li>
                                    <li>Load the new page into that frame</li>
                                    <li>Update the "last used" timestamp for the accessed page</li>
                                </ol>
                                <p>LRU performs well for most workloads but requires additional overhead to track page access times.</p>
                                """, unsafe_allow_html=True)
                            elif page_algo == 'Optimal':
                                st.markdown("""
                                <p>The <strong>Optimal</strong> algorithm (also called MIN or OPT) replaces the page that won't be used for the longest time in the future. It works as follows:</p>
                                <ol>
                                    <li>When a page is requested, check if it's already in memory</li>
                                    <li>If not (page fault), look at future references and remove the page that will not be used for longest time</li>
                                    <li>Load the new page into that frame</li>
                                </ol>
                                <p>The Optimal algorithm provides the best possible performance (minimum page faults), but it requires future knowledge of the reference string, making it impractical for real systems. It's used mainly as a theoretical benchmark.</p>
                                """, unsafe_allow_html=True)
                            elif page_algo == 'LFU':
                                st.markdown("""
                                <p>The <strong>Least Frequently Used (LFU)</strong> algorithm replaces the page with the lowest usage count. It works as follows:</p>
                                <ol>
                                    <li>When a page is requested, check if it's already in memory</li>
                                    <li>If not (page fault), remove the page with the lowest access count</li>
                                    <li>Load the new page into that frame</li>
                                    <li>Increment the counter for the accessed page</li>
                                </ol>
                                <p>LFU can perform well for stable workloads but may not adapt quickly to changing access patterns since it emphasizes historical frequency over recency.</p>
                                """, unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
            except ValueError as e:
                st.error(f"Input Error: {str(e)}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
                
    st.markdown('</div>', unsafe_allow_html=True)  # Close card

# Footer with information
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #64748B; margin-top: 2rem; border-top: 1px solid #E2E8F0;">
    <p>OS Algorithms Simulator v1.0 — Built with Streamlit</p>
    <p style="font-size: 0.9rem;">A visual educational tool for understanding operating system scheduling algorithms.</p>
</div>
""", unsafe_allow_html=True)

# Add helper classes for required functionality

class DiskScheduler:
    """Class to implement various disk scheduling algorithms"""
    
    def fcfs(self, requests, head_pos, total_cylinders):
        """First Come First Served - process requests in order they arrive"""
        sequence = [head_pos] + requests
        seek_time = sum(abs(sequence[i] - sequence[i-1]) for i in range(1, len(sequence)))
        return sequence, seek_time
    
    def sstf(self, requests, head_pos, total_cylinders):
        """Shortest Seek Time First - pick closest request to current position"""
        sequence = [head_pos]
        remaining = requests.copy()
        current_pos = head_pos
        seek_time = 0
        
        while remaining:
            # Find closest request
            closest = min(remaining, key=lambda x: abs(x - current_pos))
            seek_time += abs(closest - current_pos)
            current_pos = closest
            sequence.append(current_pos)
            remaining.remove(closest)
        
        return sequence, seek_time
    
    def scan(self, requests, head_pos, total_cylinders, direction="up"):
        """SCAN (Elevator) - Move in one direction until end, then reverse"""
        # Create sequence starting with head position
        sequence = [head_pos]
        # Total seek time
        seek_time = 0
        # Current head position
        current_pos = head_pos
        
        # Make a copy of requests
        remaining = requests.copy()
        
        # If going up first
        if direction == "up":
            # Process requests greater than head position in ascending order
            for request in sorted([r for r in remaining if r >= current_pos]):
                seek_time += abs(request - current_pos)
                current_pos = request
                sequence.append(current_pos)
                remaining.remove(request)
            
            # Go to the end of disk
            if current_pos < total_cylinders - 1:
                seek_time += abs(total_cylinders - 1 - current_pos)
                current_pos = total_cylinders - 1
                sequence.append(current_pos)
            
            # Process requests less than head position in descending order
            for request in sorted([r for r in remaining], reverse=True):
                seek_time += abs(request - current_pos)
                current_pos = request
                sequence.append(current_pos)
        
        # If going down first        
        else:
            # Process requests less than head position in descending order
            for request in sorted([r for r in remaining if r <= current_pos], reverse=True):
                seek_time += abs(request - current_pos)
                current_pos = request
                sequence.append(current_pos)
                remaining.remove(request)
            
            # Go to the beginning of disk
            if current_pos > 0:
                seek_time += abs(current_pos)
                current_pos = 0
                sequence.append(current_pos)
            
            # Process requests greater than head position in ascending order
            for request in sorted([r for r in remaining]):
                seek_time += abs(request - current_pos)
                current_pos = request
                sequence.append(current_pos)
        
        return sequence, seek_time
    
    def cscan(self, requests, head_pos, total_cylinders):
        """Circular SCAN - One-way scan with quick return to beginning"""
        # Create sequence starting with head position
        sequence = [head_pos]
        # Total seek time
        seek_time = 0
        # Current head position
        current_pos = head_pos
        
        # Make a copy of requests
        remaining = requests.copy()
        
        # Process requests greater than head position in ascending order
        higher_requests = sorted([r for r in remaining if r >= current_pos])
        for request in higher_requests:
            seek_time += abs(request - current_pos)
            current_pos = request
            sequence.append(current_pos)
            remaining.remove(request)
        
        # If we still have requests, we need to circle around
        if remaining:
            # Go to the end of disk
            if current_pos < total_cylinders - 1:
                seek_time += abs(total_cylinders - 1 - current_pos)
                current_pos = total_cylinders - 1
                sequence.append(current_pos)
            
            # Jump to the beginning (seek time counted as movement to end + movement to beginning)
            seek_time += total_cylinders - 1
            current_pos = 0
            sequence.append(current_pos)
            
            # Process remaining requests in ascending order
            for request in sorted(remaining):
                seek_time += abs(request - current_pos)
                current_pos = request
                sequence.append(current_pos)
        
        return sequence, seek_time
    
    def look(self, requests, head_pos, total_cylinders, direction="up"):
        """LOOK - Like SCAN but only go as far as last request"""
        # Create sequence starting with head position
        sequence = [head_pos]
        # Total seek time
        seek_time = 0
        # Current head position
        current_pos = head_pos
        
        # Make a copy of requests
        remaining = requests.copy()
        
        # If going up first
        if direction == "up":
            # Process requests greater than head position in ascending order
            higher_requests = sorted([r for r in remaining if r >= current_pos])
            for request in higher_requests:
                seek_time += abs(request - current_pos)
                current_pos = request
                sequence.append(current_pos)
                remaining.remove(request)
            
            # If we have more requests, change direction
            if remaining:
                # Process requests less than head position in descending order
                for request in sorted(remaining, reverse=True):
                    seek_time += abs(request - current_pos)
                    current_pos = request
                    sequence.append(current_pos)
        
        # If going down first        
        else:
            # Process requests less than head position in descending order
            lower_requests = sorted([r for r in remaining if r <= current_pos], reverse=True)
            for request in lower_requests:
                seek_time += abs(request - current_pos)
                current_pos = request
                sequence.append(current_pos)
                remaining.remove(request)
            
            # If we have more requests, change direction
            if remaining:
                # Process remaining requests in ascending order
                for request in sorted(remaining):
                    seek_time += abs(request - current_pos)
                    current_pos = request
                    sequence.append(current_pos)
        
        return sequence, seek_time
    
    def clook(self, requests, head_pos, total_cylinders):
        """C-LOOK - Like C-SCAN but only go as far as last request"""
        # Create sequence starting with head position
        sequence = [head_pos]
        # Total seek time
        seek_time = 0
        # Current head position
        current_pos = head_pos
        
        # Make a copy of requests
        remaining = requests.copy()
        
        # Process requests greater than head position in ascending order
        higher_requests = sorted([r for r in remaining if r >= current_pos])
        for request in higher_requests:
            seek_time += abs(request - current_pos)
            current_pos = request
            sequence.append(current_pos)
            remaining.remove(request)
        
        # If we still have requests, we need to circle around
        if remaining:
            # Find the lowest request
            lowest_request = min(remaining)
            
            # Jump directly to the lowest request (count the seek time)
            seek_time += abs(current_pos - lowest_request)
            current_pos = lowest_request
            sequence.append(current_pos)
            remaining.remove(lowest_request)
            
            # Process remaining requests in ascending order
            for request in sorted(remaining):
                seek_time += abs(request - current_pos)
                current_pos = request
                sequence.append(current_pos)
        
        return sequence, seek_time


class PageReplacement:
    """Class to implement various page replacement algorithms"""
    
    def fifo(self, reference_string, num_frames):
        """First-In First-Out page replacement algorithm"""
        frames = []  # Current state of frames
        page_faults = 0
        history = []  # Track frame state after each reference
        
        for page in reference_string:
            # Check if page is already in memory
            if page not in frames:
                # Page fault
                page_faults += 1
                
                # If frames are full, remove oldest (first) page
                if len(frames) == num_frames:
                    frames.pop(0)
                
                # Add new page to the end
                frames.append(page)
            
            # Add current frame state to history
            history.append(frames.copy())
        
        return history, page_faults
    
    def lru(self, reference_string, num_frames):
        """Least Recently Used page replacement algorithm"""
        frames = []  # Current state of frames
        page_faults = 0
        history = []  # Track frame state after each reference
        
        # Track when each page was last used
        last_used = {}
        
        for i, page in enumerate(reference_string):
            # Check if page is already in memory
            if page not in frames:
                # Page fault
                page_faults += 1
                
                # If frames are full, remove least recently used page
                if len(frames) == num_frames:
                    # Find least recently used page in frames
                    lru_page = min([(p, last_used[p]) for p in frames], key=lambda x: x[1])[0]
                    # Remove it
                    frames.remove(lru_page)
                
                # Add new page
                frames.append(page)
            else:
                # Move the page to the end to show it was most recently used
                frames.remove(page)
                frames.append(page)
            
            # Update when this page was last used
            last_used[page] = i
            
            # Add current frame state to history
            history.append(frames.copy())
        
        return history, page_faults
    
    def optimal(self, reference_string, num_frames):
        """Optimal (MIN/OPT) page replacement algorithm"""
        frames = []  # Current state of frames
        page_faults = 0
        history = []  # Track frame state after each reference
        
        for i, page in enumerate(reference_string):
            # Check if page is already in memory
            if page not in frames:
                # Page fault
                page_faults += 1
                
                # If frames are full, find page that won't be used for longest time
                if len(frames) == num_frames:
                    # For each page in frames, find when it will be used next
                    next_use = {}
                    for p in frames:
                        # Look for next occurrence
                        try:
                            next_index = reference_string[i+1:].index(p) + i + 1
                            next_use[p] = next_index
                        except ValueError:
                            # Page won't be used again, assign infinity
                            next_use[p] = float('inf')
                    
                    # Find page with furthest next use
                    victim = max(next_use.items(), key=lambda x: x[1])[0]
                    # Remove it
                    frames.remove(victim)
                
                # Add new page
                frames.append(page)
            
            # Add current frame state to history
            history.append(frames.copy())
        
        return history, page_faults
    
    def lfu(self, reference_string, num_frames):
        """Least Frequently Used page replacement algorithm"""
        frames = []  # Current state of frames
        page_faults = 0
        history = []  # Track frame state after each reference
        
        # Track frequency of use for each page
        frequency = {}
        # Track when each page was last used (for tie breaking)
        last_used = {}
        
        for i, page in enumerate(reference_string):
            # Update frequency counter
            if page in frequency:
                frequency[page] += 1
            else:
                frequency[page] = 1
            
            # Update last used
            last_used[page] = i
            
            # Check if page is already in memory
            if page not in frames:
                # Page fault
                page_faults += 1
                
                # If frames are full, remove least frequently used page
                if len(frames) == num_frames:
                    # Get frequencies of pages in frames
                    frame_freqs = [(p, frequency[p], last_used[p]) for p in frames]
                    # Sort by frequency, then by last used time
                    victim = min(frame_freqs, key=lambda x: (x[1], x[2]))[0]
                    # Remove it
                    frames.remove(victim)
                
                # Add new page
                frames.append(page)
            
            # Add current frame state to history
            history.append(frames.copy())
        
        return history, page_faults