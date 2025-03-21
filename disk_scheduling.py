import numpy as np
from typing import List, Tuple

class DiskScheduler:
    @staticmethod
    def fcfs(requests: List[int], head: int, cylinders: int) -> Tuple[List[int], int]:
        """First-Come, First-Served disk scheduling algorithm."""
        sequence = [head] + requests
        seek_time = sum(abs(sequence[i] - sequence[i-1]) for i in range(1, len(sequence)))
        return sequence, seek_time

    @staticmethod
    def sstf(requests: List[int], head: int, cylinders: int) -> Tuple[List[int], int]:
        """Shortest Seek Time First disk scheduling algorithm."""
        current = head
        remaining = requests.copy()
        sequence = [head]
        seek_time = 0

        while remaining:
            # Find the closest request
            distances = [abs(current - r) for r in remaining]
            next_index = distances.index(min(distances))
            next_request = remaining[next_index]
            
            seek_time += abs(current - next_request)
            current = next_request
            sequence.append(current)
            remaining.pop(next_index)

        return sequence, seek_time

    @staticmethod
    def scan(requests: List[int], head: int, cylinders: int, direction: str = 'up') -> Tuple[List[int], int]:
        """SCAN (Elevator) disk scheduling algorithm."""
        sequence = [head]
        seek_time = 0
        current = head
        
        # Sort requests
        requests = sorted(requests)
        
        if direction == 'up':
            # Handle requests greater than head
            for request in [r for r in requests if r >= head]:
                sequence.append(request)
                seek_time += abs(request - current)
                current = request
            
            # Go to the end
            if current < cylinders - 1:
                sequence.append(cylinders - 1)
                seek_time += abs(cylinders - 1 - current)
                current = cylinders - 1
            
            # Handle requests less than head
            for request in reversed([r for r in requests if r < head]):
                sequence.append(request)
                seek_time += abs(request - current)
                current = request
        else:
            # Handle requests less than head
            for request in reversed([r for r in requests if r <= head]):
                sequence.append(request)
                seek_time += abs(request - current)
                current = request
            
            # Go to the beginning
            if current > 0:
                sequence.append(0)
                seek_time += abs(current)
                current = 0
            
            # Handle requests greater than head
            for request in [r for r in requests if r > head]:
                sequence.append(request)
                seek_time += abs(request - current)
                current = request

        return sequence, seek_time

    @staticmethod
    def cscan(requests: List[int], head: int, cylinders: int) -> Tuple[List[int], int]:
        """C-SCAN disk scheduling algorithm."""
        sequence = [head]
        seek_time = 0
        current = head
        
        # Sort requests
        requests = sorted(requests)
        
        # Handle requests greater than head
        for request in [r for r in requests if r >= head]:
            sequence.append(request)
            seek_time += abs(request - current)
            current = request
        
        # Go to the end and then to the beginning
        if current < cylinders - 1:
            sequence.append(cylinders - 1)
            seek_time += abs(cylinders - 1 - current)
        
        sequence.append(0)
        seek_time += (cylinders - 1)
        current = 0
        
        # Handle requests less than head
        for request in [r for r in requests if r < head]:
            sequence.append(request)
            seek_time += abs(request - current)
            current = request

        return sequence, seek_time

    @staticmethod
    def look(requests: List[int], head: int, cylinders: int, direction: str = 'up') -> Tuple[List[int], int]:
        """LOOK disk scheduling algorithm."""
        sequence = [head]
        seek_time = 0
        current = head
        
        # Sort requests
        requests = sorted(requests)
        
        if direction == 'up':
            # Handle requests greater than head
            for request in [r for r in requests if r >= head]:
                sequence.append(request)
                seek_time += abs(request - current)
                current = request
            
            # Handle requests less than head
            for request in reversed([r for r in requests if r < head]):
                sequence.append(request)
                seek_time += abs(request - current)
                current = request
        else:
            # Handle requests less than head
            for request in reversed([r for r in requests if r <= head]):
                sequence.append(request)
                seek_time += abs(request - current)
                current = request
            
            # Handle requests greater than head
            for request in [r for r in requests if r > head]:
                sequence.append(request)
                seek_time += abs(request - current)
                current = request

        return sequence, seek_time

    @staticmethod
    def clook(requests: List[int], head: int, cylinders: int) -> Tuple[List[int], int]:
        """C-LOOK disk scheduling algorithm."""
        sequence = [head]
        seek_time = 0
        current = head
        
        # Sort requests
        requests = sorted(requests)
        
        # Handle requests greater than head
        for request in [r for r in requests if r >= head]:
            sequence.append(request)
            seek_time += abs(request - current)
            current = request
        
        # Handle requests less than head
        if [r for r in requests if r < head]:
            first_request = min(requests)
            seek_time += abs(current - first_request)
            current = first_request
            sequence.append(current)
            
            for request in [r for r in requests if head > r > first_request]:
                sequence.append(request)
                seek_time += abs(request - current)
                current = request

        return sequence, seek_time 