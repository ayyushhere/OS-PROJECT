# Disk Scheduling and Page Replacement Algorithm Simulator

This project is an interactive simulator for various disk scheduling and page replacement algorithms commonly used in operating systems.

## Features

### Disk Scheduling Algorithms
- First-Come, First-Served (FCFS)
- Shortest Seek Time First (SSTF)
- SCAN (Elevator Algorithm)
- C-SCAN (Circular SCAN)
- LOOK
- C-LOOK

### Page Replacement Algorithms
- First-In-First-Out (FIFO)
- Least Recently Used (LRU)
- Optimal Algorithm
- Least Frequently Used (LFU)

## Requirements
- Python 3.7+
- numpy
- matplotlib
- ttkthemes

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the simulator:
```bash
python main.py
```

### Disk Scheduling Tab
1. Select a disk scheduling algorithm
2. Enter the request sequence (comma-separated numbers)
3. Enter the initial head position
4. Enter the total number of cylinders
5. For SCAN and LOOK algorithms, select the direction (up/down)
6. Click "Simulate" to see the visualization and total seek time

### Page Replacement Tab
1. Select a page replacement algorithm
2. Enter the reference string (comma-separated numbers)
3. Enter the number of frames
4. Click "Simulate" to see the step-by-step visualization and total page faults

## Features
- Interactive GUI with dark/light mode toggle
- Real-time visualization of disk movement
- Step-by-step visualization of page replacement
- Performance metrics (seek time, page faults)
- Error handling and input validation

## Contributing
Feel free to submit issues and enhancement requests! 