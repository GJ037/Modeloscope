# 🧠 Modeloscope

**Modeloscope** is a desktop application for analyzing, visualizing, and inspecting 3D mesh models.
It provides an integrated workflow combining **geometry analysis**, **interactive rendering**, and **visual inspection tools** in a single interface.

---

## 🚀 Features

### 🔍 Analysis Engine

* Geometry analysis
* Topology analysis
* Quality metrics
* Performance metrics
* Toggle-based analyzers

### 🎨 3D Renderer

* Interactive mesh visualization
* Smooth camera controls (rotate, zoom, reset)
* Scene axis display
* Efficient rendering pipeline using VisPy

### 🧪 Inspection Pipeline

* Visual inspection of mesh structures
* Highlighting of regions and features
* Integrated with rendering system
* Real-time overlay visualization

---

## 📦 Supported Formats

* `.stl`
* `.obj`
* `.ply`

---

## 🖥️ Installation

### Option 1: Run Prebuilt Executable

1. Download the latest release
2. Run:

   ```bash
   Modeloscope_vX.X.exe
   ```

---

### Option 2: Run from Source

```bash
git clone https://github.com/your-username/modeloscope.git
cd modeloscope

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python launch.py
```

---

## 🧭 How to Use

1. Launch the application
2. Load a 3D model (`.stl / .obj / .ply`)
3. Navigate using:

   * Mouse drag → rotate
   * Scroll → zoom
4. Use different interfaces:

   * **Render** → visualize mesh
   * **Analyze** → compute metrics
   * **Inspect** → highlight features

---

## 🧱 Architecture Overview

Modeloscope is structured into modular systems:

```
Modeloscope/
│
├── core/            # Core logic (rendering, analysis)
├── interface/       # UI interfaces
├── renderers/       # Rendering implementations
├── inspectors/      # Inspection pipeline
├── launch.py        # Entry point
└── runner.py        # Legacy runner (if present)
```

---

## ⚙️ Tech Stack

* **Python 3.13**
* **VisPy** – GPU-based rendering
* **Trimesh** – mesh processing
* **NumPy** – numerical computations
* **Tkinter** – GUI

---

## 📈 Version Highlights

### v3.4 (Latest)

* Added application icon
* UI polish and stability improvements
* Maintained optimized build (~34MB)

### v3.2

* Inspection pipeline refinements
* Improved rendering + inspection integration

### v3.0

* Introduced inspection pipeline
* Visual mesh inspection system

### v2.2

* Removed SciPy dependency
* Reduced build size (~63MB → ~34MB)
* Improved performance

### v2.0

* Introduced 3D renderer

### v1.0

* Initial release with analysis engine

---

## 📊 Performance & Optimization

* Lightweight executable (~34MB)
* No unnecessary dependencies
* Clean packaging with PyInstaller
* Cross-system compatibility

---

## 🧩 Future Roadmap

* Heatmap-based inspection
* Edge and normal visualization
* Model comparison tools
* Export reports (JSON / PDF)
* Installer support

---

## 👤 Author

**Joel Sheno**

---

## 📄 License

This project is licensed under the MIT License.
