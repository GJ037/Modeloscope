from analyzers.base import BaseAnalyzer


class TopologyAnalyzer(BaseAnalyzer):
    """
    Analyzes structural connectivity of the mesh.

    Responsibilities:
    - Counts vertices, edges, and faces
    - Computes Euler characteristic for topology validation

    Describes how the mesh is connected internally, independent of
    its geometric shape.
    """

    def analyze(self, model, context=None):

        if model is None:
            return self.error("Model is None")

        try:
            data = {
                "vertex_count": int(len(model.vertices)),
                "face_count": int(len(model.faces)),
                "edge_count": int(len(model.edges_unique)),
                "euler_number": int(model.euler_number)
            }

            return self.success(data)

        except Exception as e:
            return self.error(str(e))