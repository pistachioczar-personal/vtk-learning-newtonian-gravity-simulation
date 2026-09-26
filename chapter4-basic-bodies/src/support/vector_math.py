from vtkmodules.vtkCommonDataModel import vtkVector3d

def add_vecs(vec1: vtkVector3d, vec2: vtkVector3d):
    return vtkVector3d(vec1[0] + vec2[0], vec1[1] + vec2[1], vec1[2] + vec2[2])

def scale_vec(scale: float, vector: vtkVector3d):
    return vtkVector3d(scale * vector[0], scale * vector[1], scale * vector[2])

def add_vec_mag(len: float, vector: vtkVector3d):
    unit_vec = vector.Normalized()
    len_vec = scale_vec(len, unit_vec)
    return add_vecs(vector, len_vec)