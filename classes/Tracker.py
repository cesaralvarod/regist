import math

class Tracker:
    def __init__(self) -> None:
        self.central_positions={}
        self.id_count=1

    def tracking(self, objects):
        objects_id=[]

        print(objects)