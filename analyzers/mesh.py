import numpy as np


def analyze_mesh(mesh):
    if mesh is None:
        raise ValueError("Mesh is None")

    is_empty = bool(mesh.is_empty)
    is_volume = bool(mesh.is_volume)
    is_watertight = bool(mesh.is_watertight)
    is_winding_consistent = bool(mesh.is_winding_consistent)

    euler_number = int(mesh.euler_number)
    genus = int(1 - (euler_number / 2))

    area = float(mesh.area)
    volume = float(mesh.volume) if mesh.is_watertight else 0.0

    face_density_area = len(mesh.faces) / mesh.area if mesh.area > 0 else 0.0
    face_density_volume = len(mesh.faces) / mesh.volume if mesh.is_watertight and mesh.volume > 0 else 0.0
    face_count = int(len(mesh.faces))

    face_area_mean = float(np.mean(mesh.area_faces)) if len(mesh.area_faces) else 0.0
    face_area_max = float(np.max(mesh.area_faces)) if len(mesh.area_faces) else 0.0
    face_area_min = float(np.min(mesh.area_faces)) if len(mesh.area_faces) else 0.0
    face_area_variance = float(np.var(mesh.area_faces)) if len(mesh.area_faces) else 0.0

    face_normal_mean = float(np.mean(mesh.face_normals)) if len(mesh.face_normals) else 0.0
    face_normal_max = float(np.max(mesh.face_normals)) if len(mesh.face_normals) else 0.0
    face_normal_min = float(np.min(mesh.face_normals)) if len(mesh.face_normals) else 0.0
    face_normal_variance = float(np.var(mesh.face_normals)) if len(mesh.face_normals) else 0.0

    covariance = np.cov(mesh.vertices.T)
    eigen_values, eigen_vectors = np.linalg.eigh(covariance)

    bounding_box = mesh.bounding_box.extents.tolist()
    bounding_ellipsoid_axes = np.sqrt(eigen_values).tolist()

    pca_components = eigen_values.tolist()
    principal_axes = mesh.principal_inertia_components.tolist()

    degenerate_faces = int(np.sum(mesh.area_faces < 1e-12))
    face_area_uniformity = float(np.std(mesh.area_faces) / face_area_mean) if face_area_mean > 0 else 0.0
    shape_eccentricity = max(bounding_ellipsoid_axes) / min(bounding_ellipsoid_axes) if min(bounding_ellipsoid_axes) > 0 else None
    roughness_index = float(np.var(np.dot(mesh.face_normals, eigen_vectors)))

    area_to_volume_ratio = (area / volume) if volume > 0 else None
    degenerate_face_ratio = float(degenerate_faces / len(mesh.faces)) if len(mesh.faces) else 0.0
    elongation_ratio = max(principal_axes) / min(principal_axes) if min(principal_axes) > 0 else None

    features = {
        "is_empty": is_empty,
        "is_volume": is_volume,
        "is_watertight": is_watertight,
        "is_winding_consistent": is_winding_consistent,

        "euler_number": euler_number,
        "genus": genus,

        "area": area,
        "volume": volume,

        "face_density_area": face_density_area,
        "face_density_volume": face_density_volume,
        "face_count": face_count,

        "face_area_mean": face_area_mean,
        "face_area_max": face_area_max,
        "face_area_min": face_area_min,
        "face_area_variance": face_area_variance,

        "face_normal_mean": face_normal_mean,
        "face_normal_max": face_normal_max,
        "face_normal_min": face_normal_min,
        "face_normal_variance": face_normal_variance,

        "bounding_box": bounding_box,
        "bounding_ellipsoid_axes": bounding_ellipsoid_axes,

        "pca_components": pca_components,
        "principal_axes": principal_axes,

        "degenerate_faces": degenerate_faces,
        "face_area_uniformity": face_area_uniformity,
        "shape_eccentricity": shape_eccentricity,
        "roughness_index": roughness_index,

        "area_to_volume_ratio": area_to_volume_ratio,
        "degenerate_face_ratio": degenerate_face_ratio,
        "elongation_ratio": elongation_ratio
    }

    return features