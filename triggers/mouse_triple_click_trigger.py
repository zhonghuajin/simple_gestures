import time
from .trigger_base import TriggerBase

class MouseTripleClickTrigger(TriggerBase):
    def __init__(self, max_interval=0.3, callback=None):
        """
        :param max_interval: The maximum time (seconds) allowed between clicks to count as a sequence.
        :param callback: Function to call when triple click is detected.
        """
        self.max_interval = max_interval
        self.callback = callback
        
        self.click_count = 0
        self.last_up_time = 0
        self.was_down = False

    def update(self, state):
        is_down = state['left_button']
        now = time.time()

        # Detect Mouse Up (Falling Edge)
        if self.was_down and not is_down:
            # Calculate time since the last click release
            time_diff = now - self.last_up_time
            
            if time_diff < self.max_interval:
                self.click_count += 1
            else:
                # If too much time passed, reset sequence to 1 (this is the first click of a new sequence)
                self.click_count = 1
            
            self.last_up_time = now

            # Check for Triple Click
            if self.click_count == 3:
                self.on_trigger()
                self.click_count = 0  # Reset after triggering

        self.was_down = is_down

    def on_trigger(self):
        if self.callback:
            self.callback()