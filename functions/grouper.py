def group_features(node_features, edge_features, mesh_features):
    grouped_features = {
        "topology": {
            "vertex_count": node_features.get("vertex_count"),
            "edge_count": edge_features.get("edge_count"),
            "face_count": mesh_features.get("face_count"),

            "euler_number": mesh_features.get("euler_number"),
            "genus": mesh_features.get("genus"),
        },
        "geometry": {
            "area": mesh_features.get("area"),
            "volume": mesh_features.get("volume"),

            "face_density_area": mesh_features.get("face_density_area"),
            "face_density_volume": mesh_features.get("face_density_volume"),

            "centroid": node_features.get("centroid"),
            "center_mass": node_features.get("center_mass"),

            "bounding_box": mesh_features.get("bounding_box"),
            "bounding_ellipsoid_axes": mesh_features.get("bounding_ellipsoid_axes"),

            "pca_components": mesh_features.get("pca_components"),
            "principal_axes": mesh_features.get("principal_axes")
        },
        "statistics": {
            "distance_to_centroid_min": node_features.get("distance_to_centroid_min"),
            "distance_to_centroid_max": node_features.get("distance_to_centroid_max"),
            "distance_to_centroid_mean": node_features.get("distance_to_centroid_mean"),
            "distance_to_centroid_variance": node_features.get("distance_to_centroid_variance"),

            "edge_length_min": edge_features.get("edge_length_min"),
            "edge_length_max": edge_features.get("edge_length_max"),
            "edge_length_mean": edge_features.get("edge_length_mean"),
            "edge_length_variance": edge_features.get("edge_length_variance"),

            "face_area_mean": mesh_features.get("face_area_mean"),
            "face_area_max": mesh_features.get("face_area_max"),
            "face_area_min": mesh_features.get("face_area_min"),
            "face_area_variance": mesh_features.get("face_area_variance"),

            "face_normal_mean": mesh_features.get("face_normal_mean"),
            "face_normal_max": mesh_features.get("face_normal_max"),
            "face_normal_min": mesh_features.get("face_normal_min"),
            "face_normal_variance": mesh_features.get("face_normal_variance")
        },
        "distributions": {
            "duplicate_vertex_ratio": node_features.get("duplicate_vertex_ratio"),
            "degenerate_edge_ratio": edge_features.get("degenerate_edge_ratio"),
            "sharp_edge_ratio": edge_features.get("sharp_edge_ratio"),

            "area_to_volume_ratio": mesh_features.get("area_to_volume_ratio"),
            "degenerate_face_ratio": mesh_features.get("degenerate_face_ratio"),
            "elongation_ratio": mesh_features.get("elongation_ratio")
        },
        "integrity": {
            "is_empty": mesh_features.get("is_empty"),
            "is_volume": mesh_features.get("is_volume"),
            "is_watertight": mesh_features.get("is_watertight"),
            "is_winding_consistent": mesh_features.get("is_winding_consistent"),

            "duplicate_vertices": node_features.get("duplicate_vertices"),
            "degenerate_edges": edge_features.get("degenerate_edges"),
            "sharp_edges": edge_features.get("sharp_edges"),

            "degenerate_faces": mesh_features.get("degenerate_faces"),
            "face_area_uniformity": mesh_features.get("face_area_uniformity"),
            "shape_eccentricity": mesh_features.get("shape_eccentricity"),
            "roughness_index": mesh_features.get("roughness_index")
        }
    }

    return grouped_features