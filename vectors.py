import numpy as np


class Vector3(np.ndarray):
    def __new__(cls, *args, **kwargs):
        if len(args) == 3:
            #TODO: add QVector
            for arg in args:
                if not (isinstance(arg, int) or isinstance(arg, float)):
                    raise TypeError(f"{arg} is not an int or a float")
            arr = np.asarray([args[0], args[1], args[2]]).view(cls)
            
        elif len(args) == 1:
            if isinstance(args[0], list):
                arr = np.asarray(args[0]).view(cls)
            elif isinstance(args[0], tuple):
                arr = np.asarray(args[0]).view(cls)
            elif isinstance(args[0], cls):
                arr = np.asarray([args[0].x(), args[0].y(), args[0].z()]).view(cls)
            else:
                raise TypeError(f"type {type(args[0])} is not supported as input.")
        else:
            raise ValueError(f"should be 3 values, {len(args)} are given.")
        arr = arr.astype('float64')
        return arr
    
    # operator overwrites
    def __add__(self, v2):
        if isinstance(v2, type(self)):
            return np.add(self, v2)
        else:
            raise TypeError(f"{v2} is not an instance of {type(self)}")
        
    def __sub__(self, v2):
        if isinstance(v2, type(self)):
            return super().__sub__(v2)
        else:
            raise TypeError(f"{v2} is not an instance of {type(self)}")

    def __mul__(self, value):
        if isinstance(value, int) or isinstance(value, float):
            return super().__mul__(value)
        elif isinstance(value, type(self)):
            return super().dot(value)
        else:
            raise TypeError(f"{type(value)} is not supported")
        
    def __floordiv__(self, value):
        if isinstance(value, int) or isinstance(value, float):
            return super().__floordiv__(value)
        return
    
    def __truediv__(self, value):
        if isinstance(value, int) or isinstance(value, float):
            return super().__truediv__(value)
        return
    
    # some vector functions
    def length(self):
        return np.sqrt(self.x() ** 2 + self.y() ** 2 + self.z() ** 2)
    
    def norm(self):
        return self * (1 / self.length())
    
    def normalize(self):
        new_vec = self.norm()
        self[0] = float(new_vec[0])
        self[1] = float(new_vec[1])
        self[2] = float(new_vec[2])
        
    def set_length(self, value):
        new_vec = self.norm() * value
        self[0] = float(new_vec[0])
        self[1] = float(new_vec[1])
        self[2] = float(new_vec[2])
        
    def distance_to(self, v2):
        if isinstance(v2, type(self)):
            return np.sqrt((v2.x() - self.x()) ** 2 +
                           (v2.y() - self.y()) ** 2 +
                           (v2.z() - self.z()) ** 2)
        else:
            raise TypeError(f"{v2} is not an instance of {type(self)}")

    # Accessors
    def x(self):
        return self[0]

    def y(self):
        return self[1]
    
    def z(self):
        return self[2]
    
    def xyz(self):
        return (self.x(), self.y(), self.z())
    
    # Mutators
    def set_x(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self[0] = value
        else:
            raise TypeError(f"{value} is not an int or a float")
            
    def set_y(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self[1] = value
        else:
            raise TypeError(f"{value} is not an int or a float")
        
    def set_z(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self[2] = value
        else:
            raise TypeError(f"{value} is not an int or a float")



class Vector2(np.ndarray):
    def __new__(cls, *args, **kwargs):
        if len(args) == 2:
            #TODO: add QVector
            for arg in args:
                if not (isinstance(arg, int) or isinstance(arg, float)):
                    raise TypeError(f"{arg} is not an int or a float")
            arr = np.asarray([args[0], args[1]]).view(cls)
            
        elif len(args) == 1:
            if isinstance(args[0], list):
                arr = np.asarray(args[0]).view(cls)
            elif isinstance(args[0], tuple):
                arr = np.asarray(args[0]).view(cls)
            elif isinstance(args[0], cls):
                arr = np.asarray(args[0]).view(cls)
            else:
                raise TypeError(f"type {type(args[0])} is not supported as input.")
        else:
            raise ValueError(f"should be 2 values, {len(args)} are given.")
        return arr
    
    # operator overwrites
    def __add__(self, v2):
        if isinstance(v2, type(self)):
            return np.add(self, v2)
        else:
            raise TypeError(f"{v2} is not an instance of {type(self)}")
        
    def __sub__(self, v2):
        if isinstance(v2, type(self)):
            return super().__sub__(v2)
        else:
            raise TypeError(f"{v2} is not an instance of {type(self)}")

    def __mul__(self, value):
        if isinstance(value, int) or isinstance(value, float):
            return super().__mul__(value)
        elif isinstance(value, type(self)):
            return super().dot(value)
        
    def __floordiv__(self, value):
        if isinstance(value, int) or isinstance(value, float):
            return super().__floordiv__(value)
        return
    
    def __truediv__(self, value):
        if isinstance(value, int) or isinstance(value, float):
            return super().__truediv__(value)
        return

    # some vector functions
    def length(self):
        return np.sqrt(self.x() ** 2 + self.y() ** 2)
    
    def norm(self):
        return self * (1 / self.length())
    
    def normalize(self):
        new_vec = self.norm()
        self[0] = float(new_vec[0])
        self[1] = float(new_vec[1])
        
    def set_length(self, value):
        new_vec = self.norm() * value
        self[0] = float(new_vec[0])
        self[1] = float(new_vec[1])
        
    def distance_to(self, v2):
        if isinstance(v2, type(self)):
            return np.sqrt((v2.x() - self.x()) ** 2 +
                             (v2.y() - self.y()) ** 2)
        else:
            raise TypeError(f"{v2} is not an instance of {type(self)}")

    # Accessors
    def x(self):
        return self[0]

    def y(self):
        return self[1]
    
    def xy(self):
        return (self.x(), self.y())

    # Mutators
    def set_x(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self[0] = value
        else:
            raise TypeError(f"{value} is not an int or a float")
            
    def set_y(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self[1] = value
        else:
            raise TypeError(f"{value} is not an int or a float")

def distance(v1, v2):
    return v1.distance_to(v2)

if __name__ == "__main__":
    # Tests
    v1 = Vector3(1,2,3)
    v1.set_length(10)
    v2 = Vector3([-5,20,0])
    v3 = Vector3((0,0,1))
    v2.normalize()
    v3 = v3.norm()
    v2 = v2 * (v1 * v1)
    print(v1, v2, v3) 
    