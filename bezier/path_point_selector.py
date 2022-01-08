from bezier.control_point_handler import ControlPointHandler


class PathPointSelector:
    def __init__(self, control_point_quartet_collection):
        self.control_point_quartet_collection = control_point_quartet_collection
        self.path_point_mapping = {}

    @staticmethod
    def create_key(quartet_index, control_point_index):
        return f'Q{quartet_index}/P{control_point_index}'

    @staticmethod
    def is_path_point(control_point_handler: ControlPointHandler):
        return control_point_handler.control_point_index in [0, 3]

    def create_path_point_mapping(self):

        nr_quartets = self.control_point_quartet_collection.number_of_quartets()

        for index in range(nr_quartets):
            mapped_first_quartet_index = nr_quartets - 1 if index == 0 else index - 1
            mapped_last_quartet_index = index + 1 if index < nr_quartets - 1 else 0
            self.path_point_mapping[self.create_key(index, 0)] = ControlPointHandler(mapped_first_quartet_index, 3)
            self.path_point_mapping[self.create_key(index, 3)] = ControlPointHandler(mapped_last_quartet_index, 0)

    def find_related_path_point(self, control_point_handler: ControlPointHandler):
        if self.is_path_point(control_point_handler):
            key = self.create_key(control_point_handler.quartet_index, control_point_handler.control_point_index)
            return self.path_point_mapping[key]
        else:
            print('error')
            exit(1)

    def find_related_control_point(self, control_point_handler: ControlPointHandler):
        related_control_point = ControlPointHandler(-1, -1)
        last_quartet_index = self.control_point_quartet_collection.number_of_quartets() - 1

        if control_point_handler.control_point_index == 1:
            related_control_point.control_point_index = 2
            if control_point_handler.quartet_index == 0:
                related_control_point.quartet_index = last_quartet_index
            elif control_point_handler.quartet_index > 0:
                related_control_point.quartet_index = control_point_handler.quartet_index - 1

        elif control_point_handler.control_point_index == 2:
            related_control_point.control_point_index = 1
            if control_point_handler.quartet_index < last_quartet_index:
                related_control_point.quartet_index = control_point_handler.quartet_index + 1
            else:
                related_control_point.quartet_index = 0

        return related_control_point

    def get_last_quartet_index(self):
        return self.control_point_quartet_collection.number_of_quartets() - 1

    def get_number_of_quartets(self):
        return self.control_point_quartet_collection.number_of_quartets()

    @staticmethod
    def find_path_point_of_control_point(control_point_handler: ControlPointHandler):
        related_control_point = ControlPointHandler(-1, -1)
        if control_point_handler.control_point_index == 1:
            related_control_point.control_point_index = 0
        elif control_point_handler.control_point_index == 2:
            related_control_point.control_point_index = 3

        related_control_point.quartet_index = control_point_handler.quartet_index

        return related_control_point

    def find_control_points_of_path_point(self, path_point_handler: ControlPointHandler):
        related_control_points = []
        number_of_quartets = self.control_point_quartet_collection.number_of_quartets()
        last_quartet_index = number_of_quartets - 1

        if path_point_handler.control_point_index == 0:
            related_control_points.append(ControlPointHandler(path_point_handler.quartet_index, 1))
            if path_point_handler.quartet_index == 0:
                related_control_points.append(ControlPointHandler(last_quartet_index, 2))
            else:
                related_control_points.append(ControlPointHandler(path_point_handler.quartet_index - 1, 2))

        elif path_point_handler.control_point_index == 3:
            related_control_points.append(ControlPointHandler(path_point_handler.quartet_index, 2))
            if path_point_handler.quartet_index == 0 and number_of_quartets > 1:
                related_control_points.append(ControlPointHandler(path_point_handler.quartet_index + 1, 1))
            elif path_point_handler.quartet_index == last_quartet_index:
                related_control_points.append(ControlPointHandler(0, 1))
            else:
                related_control_points.append(ControlPointHandler(path_point_handler.quartet_index + 1, 1))
        else:
            print('error')
            exit(1)

        return related_control_points

    def get_control_point_pairs(self):
        line_list = []

        control_point1 = self.control_point_quartet_collection.get_control_point(ControlPointHandler(0, 1))
        last_quartet_index = self.get_last_quartet_index()
        control_point2 = self.control_point_quartet_collection.get_control_point(ControlPointHandler(last_quartet_index, 2))
        line_list.append(((control_point1.x, control_point1.y), (control_point2.x, control_point2.y)))

        if self.get_number_of_quartets() > 1:
            for index in range(last_quartet_index):
                control_point1 = self.control_point_quartet_collection.get_control_point(ControlPointHandler(index, 2))
                control_point2 = self.control_point_quartet_collection.get_control_point(ControlPointHandler(index + 1, 1))
                line_list.append(((control_point1.x, control_point1.y), (control_point2.x, control_point2.y)))

        return line_list
