#!/usr/bin/env pvpython
"""Render and summarize the G1 ellipse smoke-test Ensight output."""

from pathlib import Path
import argparse

from paraview import servermanager
from paraview.simple import (
    CellDatatoPointData,
    ColorBy,
    Connectivity,
    Contour,
    CreateView,
    EnSightReader,
    GetAnimationScene,
    GetColorTransferFunction,
    Hide,
    SaveScreenshot,
    Show,
    Slice,
    Threshold,
)
from vtk.util.numpy_support import vtk_to_numpy


def leaf_datasets(data):
    if data.IsA("vtkCompositeDataSet"):
        iterator = data.NewIterator()
        iterator.InitTraversal()
        while not iterator.IsDoneWithTraversal():
            yield iterator.GetCurrentDataObject()
            iterator.GoToNextItem()
    else:
        yield data


def cell_values(data, name):
    values = []
    for leaf in leaf_datasets(data):
        array = leaf.GetCellData().GetArray(name)
        if array is not None:
            values.extend(vtk_to_numpy(array))
    return values


def new_view():
    view = CreateView("RenderView")
    view.ViewSize = [1400, 900]
    view.Background = [1.0, 1.0, 1.0]
    view.OrientationAxesVisibility = 1
    return view


def save_xy(view, output):
    view.ResetCamera()
    view.CameraPosition = [2.0, 0.0, 5.0]
    view.CameraFocalPoint = [2.0, 0.0, 0.0]
    view.CameraViewUp = [0.0, 1.0, 0.0]
    view.CameraParallelProjection = 1
    view.CameraParallelScale = 0.62
    SaveScreenshot(str(output), view, ImageResolution=[1400, 900])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("case", type=Path, help="Path to nga.case")
    parser.add_argument("output", type=Path, help="Screenshot output directory")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    reader = EnSightReader(CaseFileName=str(args.case.resolve()))
    reader.CellArrays = [
        "fvf",
        "mesh_mask",
        "porous_mask",
        "pressure",
        "velocity",
        "wall_vf",
    ]
    final_time = reader.TimestepValues[-1] if reader.TimestepValues else 0.0
    animation = GetAnimationScene()
    animation.UpdateAnimationUsingDataTimeSteps()
    animation.AnimationTime = final_time
    reader.UpdatePipeline(time=final_time)

    fetched = servermanager.Fetch(reader)
    porous = cell_values(fetched, "porous_mask")
    mesh = cell_values(fetched, "mesh_mask")
    if not porous or not mesh:
        raise RuntimeError("Expected porous_mask and mesh_mask cell arrays")
    porous_cells = sum(value > 0.0 for value in porous)
    partial_cells = sum(0.0 < value < 1.0 for value in porous)
    mesh_cells = sum(value > 0.0 for value in mesh)
    mesh_only_cells = sum(m > 0.0 and p == 0.0 for m, p in zip(mesh, porous))

    solid = Threshold(Input=reader)
    solid.Scalars = ["CELLS", "porous_mask"]
    solid.LowerThreshold = 0.5
    solid.UpperThreshold = 1.0
    connected = Connectivity(Input=solid)
    connected.ColorRegions = 1
    connected.UpdatePipeline()
    region_range = connected.GetCellDataInformation().GetArray("RegionId").GetRange()
    region_count = int(region_range[1]) + 1

    slice_mask = Slice(Input=reader)
    slice_mask.SliceType = "Plane"
    slice_mask.SliceType.Origin = [2.0, 0.0, 0.0]
    slice_mask.SliceType.Normal = [0.0, 0.0, 1.0]
    mask_view = new_view()
    mask_display = Show(slice_mask, mask_view)
    mask_display.Representation = "Surface"
    ColorBy(mask_display, ("CELLS", "porous_mask"))
    mask_lut = GetColorTransferFunction("porous_mask")
    mask_lut.RescaleTransferFunction(0.0, 1.0)
    mask_display.SetScalarBarVisibility(mask_view, True)
    save_xy(mask_view, args.output / "01_fractional_solver_field.png")
    Hide(slice_mask, mask_view)

    point_data = CellDatatoPointData(Input=reader)
    contour = Contour(Input=point_data)
    contour.ContourBy = ["POINTS", "porous_mask"]
    contour.Isosurfaces = [0.5]
    contour_view = new_view()
    contour_display = Show(contour, contour_view)
    contour_display.Representation = "Surface"
    contour_display.DiffuseColor = [0.85, 0.25, 0.12]
    save_xy(contour_view, args.output / "02_contour_0p5.png")
    Hide(contour, contour_view)

    mesh_cells_filter = Threshold(Input=reader)
    mesh_cells_filter.Scalars = ["CELLS", "mesh_mask"]
    mesh_cells_filter.LowerThreshold = 0.5
    mesh_cells_filter.UpperThreshold = 1.0
    mesh_slice = Slice(Input=mesh_cells_filter)
    mesh_slice.SliceType = "Plane"
    mesh_slice.SliceType.Origin = [2.0, 0.0, 0.0]
    mesh_slice.SliceType.Normal = [0.0, 0.0, 1.0]
    wall_cells_filter = Threshold(Input=reader)
    wall_cells_filter.Scalars = ["CELLS", "wall_vf"]
    wall_cells_filter.LowerThreshold = 0.0
    wall_cells_filter.UpperThreshold = 0.5
    wall_slice = Slice(Input=wall_cells_filter)
    wall_slice.SliceType = "Plane"
    wall_slice.SliceType.Origin = [2.0, 0.0, 0.0]
    wall_slice.SliceType.Normal = [0.0, 0.0, 1.0]
    geometry_view = new_view()
    mesh_display = Show(mesh_slice, geometry_view)
    mesh_display.Representation = "Surface"
    mesh_display.DiffuseColor = [0.10, 0.35, 0.95]
    mesh_display.Opacity = 0.65
    ColorBy(mesh_display, None)
    wall_display = Show(wall_slice, geometry_view)
    wall_display.Representation = "Surface"
    wall_display.DiffuseColor = [0.25, 0.25, 0.25]
    ColorBy(wall_display, None)
    save_xy(geometry_view, args.output / "03_mesh_and_walls.png")

    pressure = cell_values(fetched, "pressure")
    if pressure:
        pressure_slice = Slice(Input=reader)
        pressure_slice.SliceType = "Plane"
        pressure_slice.SliceType.Origin = [2.0, 0.0, 0.0]
        pressure_slice.SliceType.Normal = [0.0, 0.0, 1.0]
        pressure_view = new_view()
        pressure_display = Show(pressure_slice, pressure_view)
        pressure_display.Representation = "Surface"
        ColorBy(pressure_display, ("CELLS", "pressure"))
        pressure_display.RescaleTransferFunctionToDataRange(True, False)
        pressure_display.SetScalarBarVisibility(pressure_view, True)
        save_xy(pressure_view, args.output / "04_final_pressure.png")
        Hide(pressure_slice, pressure_view)
    else:
        print("pressure cell array unavailable; skipped 04_final_pressure.png")

    velocity = cell_values(fetched, "velocity")
    if velocity:
        velocity_slice = Slice(Input=reader)
        velocity_slice.SliceType = "Plane"
        velocity_slice.SliceType.Origin = [2.0, 0.0, 0.0]
        velocity_slice.SliceType.Normal = [0.0, 0.0, 1.0]
        velocity_view = new_view()
        velocity_display = Show(velocity_slice, velocity_view)
        velocity_display.Representation = "Surface"
        ColorBy(velocity_display, ("CELLS", "velocity", "Magnitude"))
        velocity_display.RescaleTransferFunctionToDataRange(True, False)
        velocity_display.SetScalarBarVisibility(velocity_view, True)
        save_xy(velocity_view, args.output / "05_final_velocity_magnitude.png")
    else:
        print("velocity cell array unavailable; skipped 05_final_velocity_magnitude.png")

    print(f"porous-positive cells: {porous_cells}")
    print(f"porous-partial cells: {partial_cells}")
    print(f"mesh-positive cells: {mesh_cells}")
    print(f"mesh-only cells: {mesh_only_cells}")
    print(f"porous connected regions at 0.5: {region_count}")


if __name__ == "__main__":
    main()
