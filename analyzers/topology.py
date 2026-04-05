class TopologyAnalyzer:

    def analyze(self, model, context=None):
        if model is None:
            raise ValueError("Model is None")

        return {
            "vertex_count": int(len(model.vertices)),
            "face_count": int(len(model.faces)),
            "edge_count": int(len(model.edges_unique)),
            "euler_number": int(model.euler_number)
        }