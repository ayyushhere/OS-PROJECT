from typing import List, Tuple
from collections import deque, defaultdict

class PageReplacement:
    @staticmethod
    def fifo(reference_string: List[int], num_frames: int) -> Tuple[List[List[int]], int]:
        """First-In-First-Out page replacement algorithm."""
        frames = []
        page_faults = 0
        queue = deque(maxlen=num_frames)
        history = []
        
        for page in reference_string:
            if page not in frames:
                page_faults += 1
                if len(frames) >= num_frames:
                    old_page = queue.popleft()
                    frames.remove(old_page)
                frames.append(page)
                queue.append(page)
            history.append(frames.copy())
            
        return history, page_faults

    @staticmethod
    def lru(reference_string: List[int], num_frames: int) -> Tuple[List[List[int]], int]:
        """Least Recently Used page replacement algorithm."""
        frames = []
        page_faults = 0
        page_usage = {}  # Tracks when each page was last used
        history = []
        
        for time, page in enumerate(reference_string):
            if page not in frames:
                page_faults += 1
                if len(frames) >= num_frames:
                    # Find least recently used page
                    lru_page = min(page_usage.items(), key=lambda x: x[1])[0]
                    frames.remove(lru_page)
                    del page_usage[lru_page]
                frames.append(page)
            page_usage[page] = time
            history.append(frames.copy())
            
        return history, page_faults

    @staticmethod
    def optimal(reference_string: List[int], num_frames: int) -> Tuple[List[List[int]], int]:
        """Optimal page replacement algorithm."""
        frames = []
        page_faults = 0
        history = []
        
        for i, page in enumerate(reference_string):
            if page not in frames:
                page_faults += 1
                if len(frames) >= num_frames:
                    # Find page that won't be used for the longest time
                    future_usage = {}
                    for frame in frames:
                        try:
                            next_use = reference_string[i+1:].index(frame)
                            future_usage[frame] = next_use
                        except ValueError:
                            future_usage[frame] = float('inf')
                    victim = max(future_usage.items(), key=lambda x: x[1])[0]
                    frames.remove(victim)
                frames.append(page)
            history.append(frames.copy())
            
        return history, page_faults

    @staticmethod
    def lfu(reference_string: List[int], num_frames: int) -> Tuple[List[List[int]], int]:
        """Least Frequently Used page replacement algorithm."""
        frames = []
        page_faults = 0
        frequency = defaultdict(int)  # Tracks frequency of each page
        history = []
        
        for page in reference_string:
            frequency[page] += 1
            
            if page not in frames:
                page_faults += 1
                if len(frames) >= num_frames:
                    # Find least frequently used page(s)
                    min_freq = min(frequency[p] for p in frames)
                    lfu_pages = [p for p in frames if frequency[p] == min_freq]
                    # If multiple pages have same frequency, remove the first one
                    frames.remove(lfu_pages[0])
                frames.append(page)
            history.append(frames.copy())
            
        return history, page_faults 