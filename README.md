# 🧠 **MODELOSCOPE**

**Modeloscope** is a project for analyzing, visualizing, and inspecting 3D meshes.
It is light weight, performance efficient and supports file formats such as `.stl`, `.off`, `.ply`, `obj`, `.gltf` and `.glb`.


## 🚀 FEATURES

### 🔍 **Analyzers**
* Topology analysis
* Geometry analysis
* Statistics metrics
* Distributions metrics
* Integrity metrics

### 🎨 **Renderers**
* Flat render
* Shaded render
* Wireframe render
* Pointcloud render

### 🧪 **Inspectors**
* Duplicate vertices inspection
* Non manifold edges inspection
* Sharp edges inspection
* Degenerate faces inspection
* Flipped normals inspection

### ❤ **Enhancements**
* Generate and Export analysis report
* Custom rendering pipeline using VisPy
* Smooth camera controls (rotate, zoom, reset)
* Highlight heatmap regions on inspection


## 🧱 ARCHITECTURE OVERVIEW

   ```
   Modeloscope/
   │
   ├── functions/       # Functional logics
   ├── interfaces/      # Interfaces logics
   ├── analyzers/       # Analyzing logics
   ├── renderers/       # Rendering logics
   ├── inspectors/      # Inspection logics
   └── launch.py        # Entry point
   ```


## 🖥️ INSTALLATION METHODS

### Option 1: Run Prebuilt Executable
1. Download the latest release

2. Run:
```bash
Modeloscope.exe
```

### Option 2: Run from Source
1. Clone the repository:
```bash
git clone https://github.com/GJO37/Modeloscope.git
cd Modeloscope   
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python launch.py
```


## 🧭 HOW TO USE

1. Launch the application

2. Use different interfaces:
   * **Analyze** → compute metrics
   * **Render** → visualize mesh
   * **Inspect** → highlight features

3. Load an 3D mesh 

4. **Analyze**, **Render** or **Inspect**


## ⚙️ TECH STACK

* **Python 3.13**
* **NumPy**   – Numerical computations
* **Trimesh** – Mesh processing
* **VisPy**   – GPU-based rendering
* **Tkinter** – User interface


## 📈 VERSION HIGLIGHTS

### v3.6 (Latest)
* Overlay Loading
* Altered Inspection Modes
* Altered Model Support

### v3.5
* Screen Scaling
* Screen Layout
* Cursor Feedback
* Updated Libraries

### v3.4
* Added Threading
* Async Behaviour
* Flow Changes

### v3.3
* Changed Clear Button
* Various Improvements
* State Handling
* Quality Additions

### v3.2
* Added New Renderer
* New Camera Movement
* Exception Handeling
* Fxied Hidden Bugs
* Quality Additions

### v3.1
* Pipeline Standardization
* Better Error Handling
* Fixed Hidden Bugs

### v3.0
* Introduced inspection pipeline
* Visual mesh inspection system

### v2.2
* Removed SciPy dependency
* Reduced build size
* Architectural Overhaul
* Improved UI Experience

### v2.1
* Changed Viewport Background
* Improved Shaded Rendering
* Improved Pointcloud rendering
* Fixed Packaging Issues

### v2.0
* Introduced 3D renderer

### v1.0
* Initial release with analysis engine
