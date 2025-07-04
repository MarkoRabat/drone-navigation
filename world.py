
class World:

    def __init__(self):
        elements = dict()

    def get(element_id: int):
        if element_id in elements:
            return self.elements[element_id]
        else: return None


class WorldObject:

    world_object_id = 0

    def __init__(self):
        WorldObject.world_object_id += 1
        self.my_wid = WorldObject.world_object_id


#class Obj2(WorldObject):
#
#    def __init__(self):
#        super(Obj2, self).__init__()
