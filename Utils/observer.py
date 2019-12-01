class Subject(object):
    def __init__(self):
        self.observers=[]
    def notify(self):
        print("Subject.notify()")
        for obs in self.observers:
            obs.update(self)
    def attach(self, obs):
        if not hasattr(obs,"update"):
            raise ValueError("Observer must have an update() method")
        if not obs in self.observers:
            self.observers.append(obs)
    def detach(self, obs):
        if obs in self.observers :
            self.observers.remove(obs)

class Observer:
    def update(self, subject):
        raise NotImplementedError
