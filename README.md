# 🧠 Modeloscope

**Modeloscope** is a project for analyzing, visualizing, and inspecting 3D models.
It provides an integrated workflow combining **model analysis**, **interactive rendering**, and **visual inspection tools** in 3 different interfaces.

---

## 🚀 Features

### 🔍 Analysis Pipelne

* Meta Data
* Geometry analysis
* Topology analysis
* Quality metrics
* Performance metrics
* Generate Rport
* Export Report

### 🎨 3D Renderer

* Interactive mesh visualization
* Smooth camera controls (rotate, zoom, reset)
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
2. Use different interfaces:

   * **Analyze** → compute metrics
   * **Render** → visualize mesh
   * **Inspect** → highlight features
3. Load a 3D model (`.stl / .obj / .ply`)
4. **Analyze**, **Render** or **Inspect**

---

## 🧱 Architecture Overview

Modeloscope is structured into modular systems:

```
Modeloscope/
│
├── cores/            # Core logic (rendering, analysis)
├── interfaces/       # UI interfaces
├── analyzers/       # Analyzing Logics
├── renderers/       # Rendering implementations
├── inspectors/      # Inspection pipeline
└── launch.py        # Entry point
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

* Added Threading
* Async Behaviour
* Flow Changes

## v3.3

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

## v3.1

* Pipeline Standardization
* Better Error Handling
* Fixed Hidden Bugs

### v3.0

* Introduced inspection pipeline
* Visual mesh inspection system

### v2.2

* Removed SciPy dependency
* Reduced build size (~63MB → ~34MB)
* Architectural Overhaul
* Improved UI Experience

## v2.1

* Changed Viewport Background
* Improved Shaded Rendering
* Improved Pointcloud rendering
* Fixed Packaging Issues

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

## 👤 Author

**Joel Sheno**

---

## 📄 License

This project is licensed under the MIT License.
