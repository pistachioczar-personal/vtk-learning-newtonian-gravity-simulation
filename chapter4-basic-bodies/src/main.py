# Personal and default imports
from bodies.NewtonianBody import NewtonianBody
from support import vector_math as vm
import numpy as np  

# VTK imports
import vtkmodules.vtkRenderingOpenGL2
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingFreeType
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindowInteractor,
    vtkRenderWindow,
    vtkRenderer,
    vtkMapper,
    vtkActor,
    vtkTextActor,
    vtkPolyDataMapper
)
from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData,
    vtkVector3d,
    vtkDataObject,
)
from vtkmodules.vtkFiltersSources import (
    vtkSphereSource,
    vtkArrowSource,
    vtkCubeSource,
)
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter


def main(number_of_bodies, bounds: list):

    #Setting visualization objects
    renderer = vtkRenderer()
    renderer.SetBackground(0.9,0.9,0.9)
    render_window = vtkRenderWindow()
    render_window.SetSize(800, 600)
    iren = vtkRenderWindowInteractor()
    render_window.AddRenderer(renderer)
    iren.SetRenderWindow(render_window)

    bodies = [NewtonianBody(None, 0, None, None, 0) for _ in range(number_of_bodies)]

    x_min, x_max, y_min, y_max, z_min, z_max = bounds
    bounds_side_length = max(x_max - x_min, y_max - y_min, z_max - z_min)
    volume = bounds_side_length ** 3

    randomize_bodies(bodies, bounds)

    #Sources to be used for glyphs
    velocity_source = vtkArrowSource()
    gravity_source = vtkArrowSource()
    body_source = vtkSphereSource()

    #Setting arrow properties
    velocity_source.SetShaftRadius(0.05)
    gravity_source.SetShaftRadius(0.05)

    #Glyph data arrays
    gravity_array = vtkDoubleArray()
    gravity_array.SetName("Gravity")
    gravity_array.SetNumberOfComponents(3)

    velocity_array = vtkDoubleArray()
    velocity_array.SetName("Velocity")
    velocity_array.SetNumberOfComponents(3)

    radius_array = vtkDoubleArray()
    radius_array.SetName("Radius")
    radius_array.SetNumberOfComponents(1)

    position_array = vtkPoints()
    position_array.SetNumberOfPoints(number_of_bodies)


    for i, body in enumerate(bodies):
        position_array.SetPoint(i, body.get_position())
        radius_array.InsertTuple1(i, body.get_radius())

        # Add the body radius to its velocity and gravity vectors for visual purposes
        edited_velocity = vm.add_vec_mag(body.get_radius(), body.get_velocity())
        velocity_array.InsertTuple3(i, edited_velocity[0], edited_velocity[1], edited_velocity[2])
        edited_gravity = vm.add_vec_mag(body.get_radius(), body.get_gravity())
        gravity_array.InsertTuple3(i, edited_gravity[0], edited_gravity[1], edited_gravity[2])

    #Master polydata holding all information on bodies.
    body_polydata = vtkPolyData()
    body_polydata.SetPoints(position_array)
    body_polydata.GetPointData().AddArray(radius_array)
    body_polydata.GetPointData().AddArray(velocity_array)
    body_polydata.GetPointData().AddArray(gravity_array)

    #Making the actual Glyphs
    velocity_glyph = vtkGlyph3D()
    gravity_glyph = vtkGlyph3D()
    body_glyph = vtkGlyph3D()

    velocity_glyph.SetSourceConnection(velocity_source.GetOutputPort())
    gravity_glyph.SetSourceConnection(gravity_source.GetOutputPort())
    body_glyph.SetSourceConnection(body_source.GetOutputPort())

    velocity_glyph.SetInputData(body_polydata)
    gravity_glyph.SetInputData(body_polydata)
    body_glyph.SetInputData(body_polydata)

    #Velocity glyph properties
    velocity_glyph.SetInputArrayToProcess(1,0,0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "Velocity")
    velocity_glyph.OrientOn()
    velocity_glyph.SetScaleModeToScaleByVector()
    velocity_glyph.SetVectorModeToUseVector()

    #Gravity glyph properties
    gravity_glyph.SetInputArrayToProcess(1,0,0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "Gravity")
    gravity_glyph.OrientOn()
    gravity_glyph.SetScaleModeToScaleByVector()
    gravity_glyph.SetVectorModeToUseVector()

    #Body glyph properties
    body_glyph.SetInputArrayToProcess(0,0,0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "Radius")
    body_glyph.SetScaleModeToScaleByScalar()


    #Making the mappers
    velocity_mapper = vtkPolyDataMapper()
    gravity_mapper = vtkPolyDataMapper()
    body_mapper = vtkPolyDataMapper()

    velocity_mapper.SetInputConnection(velocity_glyph.GetOutputPort())
    gravity_mapper.SetInputConnection(gravity_glyph.GetOutputPort())
    body_mapper.SetInputConnection(body_glyph.GetOutputPort())

    velocity_mapper.ScalarVisibilityOff() 
    gravity_mapper.ScalarVisibilityOff()
    body_mapper.ScalarVisibilityOff()

    #Setting actors
    velocity_actor = vtkActor()
    gravity_actor = vtkActor()
    body_actor = vtkActor()

    #Velocity actor properties
    velocity_actor.SetMapper(velocity_mapper)
    velocity_actor.GetProperty().SetColor(1, 0, 0)  # makes velocity vectors red

    #Gravity actor properties
    gravity_actor.SetMapper(gravity_mapper)
    gravity_actor.GetProperty().SetColor(0,0,1)  # makes gravity vectors blue

    #Body actor properties
    body_actor.SetMapper(body_mapper)
    body_actor.GetProperty().SetColor(.01,.01,.01) # makes body spheres dark gray

    renderer.AddActor(velocity_actor)
    renderer.AddActor(gravity_actor)
    renderer.AddActor(body_actor)

    #Bounding box
    bounding_box_source = vtkCubeSource()
    bounding_box_source.SetBounds(*bounds)
    outline_filter = vtkOutlineFilter()
    outline_filter.SetInputConnection(bounding_box_source.GetOutputPort())

    bounding_box_mapper = vtkPolyDataMapper()
    bounding_box_mapper.SetInputConnection(outline_filter.GetOutputPort())
    bounding_box_actor = vtkActor()
    bounding_box_actor.SetMapper(bounding_box_mapper)

    renderer.AddActor(bounding_box_actor)

    #Text for the energies in the system
    kinetic_text = vtkTextActor()
    potential_text = vtkTextActor()
    total_text = vtkTextActor()

    #Setting text
    font_size = 20
    kinetic_text.GetTextProperty().SetFontSize(font_size)
    potential_text.GetTextProperty().SetFontSize(font_size)
    total_text.GetTextProperty().SetFontSize(font_size)

    kinetic_text.GetProperty().SetColor(0,0,0)
    potential_text.GetProperty().SetColor(0,0,0)
    total_text.GetProperty().SetColor(0,0,0)

    kinetic_text.SetInput("Kinetic Energy: " + str(NewtonianBody.get_system_kinetic(bodies)))
    potential_text.SetInput("Potential Energy: " + str(NewtonianBody.get_system_potential(bodies)))
    total_text.SetInput("Total Energy: " + str(NewtonianBody.get_system_energy(bodies)))

    #update window
    render_window.Render()

    #Positioning text
    window_bounds = render_window.GetSize()

    text_size = [0.0, 0.0]
    #Setting kinetic text position
    kinetic_text.GetSize(renderer, text_size)
    kinetic_y = int(window_bounds[1] - text_size[1])
    kinetic_text.SetDisplayPosition(0, kinetic_y)

    #Setting potential text position
    potential_text.GetSize(renderer, text_size)
    potential_y = int(window_bounds[1] - 2*text_size[1])
    potential_text.SetDisplayPosition(0, potential_y)

    #Setting total text position
    total_text.GetSize(renderer, text_size)
    total_y = int(window_bounds[1] - 3*text_size[1])
    total_text.SetDisplayPosition(0, total_y)

    renderer.AddActor(kinetic_text)
    renderer.AddActor(potential_text)
    renderer.AddActor(total_text)

    renderer.ResetCamera()
    renderer.GetActiveCamera().SetFocalPoint(bounds[0] + (bounds[1] - bounds[0]) / 2, bounds[2] + (bounds[3] - bounds[2]) / 2, bounds[4] + (bounds[5] - bounds[4]) / 2)
    render_window.Render()

    iren.Initialize()
    iren.Start()


def find_max_radius(number_of_bodies: int, ratio: float, volume: float):
    if ratio > 1 or ratio <= 0:
        raise ValueError("Ratio must be a positive float less than or equal to 1")
    max_radius = ratio/2 * (volume / number_of_bodies) ** (1/3)
    return max_radius

def get_volume(bounds):
    return (bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) * (bounds[5] - bounds[4])


def randomize_bodies(bodies, bounds):

    rand = np.random.default_rng()

    max_radius = find_max_radius(len(bodies), 0.8, get_volume(bounds))

    #Handles position making so there are no intersections.
    bodies_made = []
    for body in bodies:
        while(1):

            rad = rand.uniform(0.01, max_radius)
            

            x = rand.uniform(bounds[0]+rad, bounds[1]-rad)
            y = rand.uniform(bounds[2]+rad, bounds[3]-rad)
            z = rand.uniform(bounds[4]+rad, bounds[5]-rad)
            
            body.set_radius(rad)
            body.set_position(vtkVector3d(x, y, z))

            does_intersect = False
            for other_body in bodies_made:
                if body.does_intersect(other_body):
                    break
            else:
                bodies_made.append(body)
                break


        #Handling randomized mass based off density and size of body
        density = rand.uniform(0.1,10)
        volume = (4/3) * np.pi * rad**3
        mass = density * volume
        body.set_mass(mass)

        #Handling randomized velocity
        vel = np.random.rand(3)
        vel = vel / np.linalg.norm(vel) * rand.uniform(0, 0.05)
        body.set_velocity(vtkVector3d(*vel))

    for body in bodies:
        body.set_gravity(bodies)

if __name__ == "__main__":
    main(100, [0,20,0,20,0,20])