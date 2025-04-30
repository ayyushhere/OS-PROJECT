# OS Algorithms Simulator - Streamlit Web App

This is a web application version of the OS Algorithms Simulator, which visualizes various disk scheduling and page replacement algorithms used in operating systems.

## Features

- **Disk Scheduling Algorithms:**
  - FCFS (First-Come-First-Served)
  - SSTF (Shortest-Seek-Time-First)
  - SCAN (Elevator)
  - C-SCAN (Circular SCAN)
  - LOOK
  - C-LOOK (Circular LOOK)

- **Page Replacement Algorithms:**
  - FIFO (First-In-First-Out)
  - LRU (Least Recently Used)
  - Optimal
  - LFU (Least Frequently Used)

- **Beautiful UI with Interactive Visualizations:**
  - Interactive charts for disk movement visualization
  - Step-by-step visualization of page replacement
  - Performance metrics (seek time, page faults, hit ratio)

## Installation

1. Make sure you have Python 3.7+ installed on your system.

2. Clone or download this repository.

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the App

To start the Streamlit app, run one of the following commands in your terminal:

```
python -m streamlit run app.py
```

Or if streamlit is in your PATH:

```
streamlit run app.py
```

You can also use the included batch file (Windows only):
```
run_streamlit_app.bat
```

The app will open in your default web browser at `http://localhost:8501`.

## Usage

### Disk Scheduling Simulator

1. Select a disk scheduling algorithm from the dropdown menu.
2. Enter a comma-separated sequence of cylinder requests (e.g., `98, 183, 37, 122, 14, 124, 65, 67`).
3. Specify the initial head position.
4. Enter the total number of cylinders (typically 200).
5. If using SCAN or LOOK algorithms, select the initial direction.
6. Click the "Simulate Disk Algorithm" button to see the results.

### Page Replacement Simulator

1. Select a page replacement algorithm from the dropdown menu.
2. Enter a comma-separated reference string (e.g., `7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1`).
3. Specify the number of frames available in memory.
4. Click the "Simulate Page Algorithm" button to see the results.

## Screenshots

(Note: Add screenshots of the application here)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 