class TopologyAnalyzer:
    """
    Computes topological properties of the 3D mesh.

    Calculates:
        - Vertex count
        - Face count
        - Edge count
        - Euler characteristic    
    """

    def analyze(self, model):

        if model is None:
            print("[TopologyAnalyzer ERROR] model is None")
            return None

        try:
            vertex_count = int(len(model.vertices))
            face_count = int(len(model.faces))
            edge_count = int(len(model.edges_unique))

            euler_number = int(model.euler_number)

            return {
                "vertex_count": vertex_count,
                "face_count": face_count,
                "edge_count": edge_count,
                "euler_number": euler_number
            }

        except Exception as e:
            print(f"[TopologyAnalyzer ERROR] {e}")
            return None
            