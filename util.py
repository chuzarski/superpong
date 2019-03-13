class LifeCycle():
    def __init__(self, surface):

        self.set_surface(surface)

    def set_surface(self, surface):
        self.surface = surface

        # update the surface height/width
        self.surface_size = surface.get_size()

    def cycle(self):
        raise NotImplementedError


class LifeCycles():

    def __init__(self):
        self.__lifecycles = dict()

    def register_lifecycle(self, tag, obj):
        if tag not in self.__lifecycles:
            self.__lifecycles[tag] = obj
        else:
            return False

    def get_lifecycle(self, tag):
        if tag in self.__lifecycles:
            return self.__lifecycles[tag]
        else:
            return False

    def get_tags(self):
        return self.__lifecycles.keys()