# Algorithm Documentation and Input Constraints

## Disk Scheduling Algorithms

### 1. First-Come, First-Served (FCFS)
- **Working**: 
  - Requests are processed in the order they arrive
  - Head moves directly to the requested track
  - No optimization for minimizing seek time
- **Advantages**: Simple, fair to all requests
- **Disadvantages**: Higher seek times, no optimization
- **Input Constraints**:
  - Request sequence: Comma-separated integers (e.g., "23, 89, 132, 42")
  - Initial head position: Integer between 0 and (total cylinders - 1)
  - Total cylinders: Positive integer

### 2. Shortest Seek Time First (SSTF)
- **Working**:
  - Always moves to the closest pending request
  - Minimizes immediate seek time
  - Uses absolute distance to determine next request
- **Advantages**: Better average seek time than FCFS
- **Disadvantages**: May cause starvation for distant requests
- **Input Constraints**: Same as FCFS

### 3. SCAN (Elevator Algorithm)
- **Working**:
  - Head moves in one direction until end
  - Services requests in its path
  - Reverses direction at the end
  - Like an elevator serving people on different floors
- **Advantages**: More fair than SSTF, good for heavy loads
- **Disadvantages**: May cause longer wait times
- **Input Constraints**:
  - Same as FCFS
  - Direction: 'up' or 'down'
  - Head moves to last cylinder in 'up' direction or cylinder 0 in 'down' direction

### 4. C-SCAN (Circular SCAN)
- **Working**:
  - Similar to SCAN but moves in one direction only
  - After reaching end, jumps back to start
  - Services requests only in one direction
- **Advantages**: More uniform waiting time than SCAN
- **Disadvantages**: Longer seek times for some requests
- **Input Constraints**: Same as FCFS

### 5. LOOK
- **Working**:
  - Similar to SCAN but doesn't go to the end
  - Reverses direction at the last request
  - More efficient than SCAN
- **Advantages**: Better performance than SCAN
- **Disadvantages**: Complex implementation
- **Input Constraints**:
  - Same as SCAN
  - Direction affects initial movement

### 6. C-LOOK
- **Working**:
  - Combination of C-SCAN and LOOK
  - Moves in one direction only
  - Jumps back to lowest request after highest
- **Advantages**: Most efficient for heavy loads
- **Disadvantages**: Complex implementation
- **Input Constraints**: Same as FCFS

## Page Replacement Algorithms

### 1. First-In-First-Out (FIFO)
- **Working**:
  - Replaces the oldest page in memory
  - Uses queue data structure
  - Simple to implement
- **Advantages**: Simple, low overhead
- **Disadvantages**: Doesn't consider page usage
- **Input Constraints**:
  - Reference string: Comma-separated integers (e.g., "1, 2, 3, 4")
  - Number of frames: Positive integer
  - Page numbers should be non-negative integers

### 2. Least Recently Used (LRU)
- **Working**:
  - Replaces page that hasn't been used for longest time
  - Tracks last usage time of each page
  - More complex but better performance
- **Advantages**: Good performance, considers temporal locality
- **Disadvantages**: Requires tracking page usage
- **Input Constraints**: Same as FIFO

### 3. Optimal Algorithm
- **Working**:
  - Replaces page that won't be used for longest time
  - Requires future knowledge of page references
  - Theoretical algorithm, not practical
- **Advantages**: Best possible performance
- **Disadvantages**: Requires future knowledge
- **Input Constraints**: Same as FIFO

### 4. Least Frequently Used (LFU)
- **Working**:
  - Replaces page with lowest access frequency
  - Maintains counter for each page
  - Considers historical usage
- **Advantages**: Good for repeated access patterns
- **Disadvantages**: Doesn't consider recent usage
- **Input Constraints**: Same as FIFO

## General Input Guidelines

### Disk Scheduling
1. All numbers must be non-negative integers
2. Initial head position must be within cylinder range
3. Request sequence should not contain duplicates for best results
4. Total cylinders should be greater than max request value
5. Format: Comma-separated values without spaces (e.g., "23,89,132,42")

### Page Replacement
1. All page numbers must be non-negative integers
2. Number of frames should be reasonable (typically 3-10)
3. Reference string can contain duplicates
4. Format: Comma-separated values without spaces (e.g., "1,2,3,2,1,5")

## Performance Metrics

### Disk Scheduling
- **Seek Time**: Time taken to move head between cylinders
- **Total Seek Time**: Sum of all seek movements
- **Average Seek Time**: Total seek time / number of requests

### Page Replacement
- **Page Faults**: Number of times a page needs to be loaded
- **Hit Ratio**: (Total References - Page Faults) / Total References
- **Fault Ratio**: Page Faults / Total References

## Visualization Details

### Disk Scheduling Graph
- X-axis: Request sequence number
- Y-axis: Cylinder number
- Blue line: Head movement path
- Points: Individual requests

### Page Replacement Table
- Columns: Frame numbers and current page
- Rows: Steps in the algorithm
- Shows page replacement history
- Highlights page faults 