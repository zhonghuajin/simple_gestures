# triggers/trigger_base.py

class TriggerBase:
    def update(self, state):
        """
        每帧调用，state为输入状态（字典）
        必须实现：识别事件并调用self.on_trigger()
        """
        raise NotImplementedError

    def on_trigger(self):
        """触发时调用此方法"""
        pass