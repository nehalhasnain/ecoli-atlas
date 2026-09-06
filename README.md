# E. coli Atlas 3D · Bacterial Ultrastructure & Macromolecular Architecture

An interactive, scientifically accurate 3D ultrastructural atlas of **Escherichia coli K-12 MG1655** built with React 19, Three.js, and Tailwind/shadcn. Explore the macromolecular organization, cell envelope layers, nucleoid, plasmids, and motility appendages of the quintessential Gram-negative model organism in real time.

---

## Features

- **Assembled & Two-Tier Exploded Inventory**:
  - **Assembled View**: Realistic rod-shaped bacterium (~1.0 × 2.5 µm) featuring a precision front cutaway revealing internal compartmentalization.
  - **Disassembled Gallery**: Two-tier museum inventory where the 5 outer capsule and cell envelope shells are horizontally arranged along the top, while internal macromolecular complexes (nucleoid, plasmids, ribosomes, RNAP, ATP synthases) and surface appendages (fimbriae/pili, flagella, porins) are organized cleanly below.
- **20 Individually Selectable Components**:
  - **Outer Envelope & LPS**: Lipopolysaccharide (LPS) outer layer (Lipid A, Core, O-antigen), Outer Membrane asymmetric bilayer, and OmpF/OmpC porin trimers.
  - **Periplasmic Space**: Redox-active aqueous gel compartment with chaperones and transport SBPs.
  - **Cell Wall**: Peptidoglycan (murein) sacculus open lattice meshwork tethered by Braun's lipoprotein (Lpp).
  - **Inner (Plasma) Membrane**: Fluid mosaic phospholipid bilayer hosting PMF electron transport chains.
  - **Genetic Core**: Supercoiled 4.64-Mbp circular nucleoid with NAPs (HU, H-NS, Fis), high-copy pUC19 plasmid with *bla* $\beta$-lactamase resistance, and low-copy conjugative F-plasmid.
  - **Macromolecular Machinery**: 70S translation ribosomes, RNA polymerase holoenzymes ($\sigma^{70}$), rotary $\text{F}_1\text{F}_0$-ATP synthase motors, and flagellar basal motors ($\text{L, P, MS, C}$ rings & MotA/B stator).
  - **Surface Motility & Adhesion**: Peritrichous helical flagella filaments (FliC) and Type 1 fimbriae (pili) with FimH adhesin tips.
  - **Storage Granules**: Polyphosphate (volutin) and glycogen energy reserve inclusion bodies.
- **Textbook-Grade Written Details**: Deep biochemical, physiological, and clinical pharmacology context for every component.
- **Interactive Controls**: Orbit, pan, zoom, auto-rotation, structure isolation, system visibility toggles, and instant anatomy search with keyboard shortcut (`/`).
- **High-Performance WebGL Engine**: Hardware-accelerated GPU normal packing, single-pass batch rendering, and custom GLSL shaders running at 60+ FPS.

---

## Getting Started

### Prerequisites
- Node.js >= 20 (Node.js 22+ recommended)
- Python 3 (only needed if regenerating 3D procedural geometries)

### Installation & Run

```bash
# Clone the repository
git clone https://github.com/nehalhasnain/ecoli-atlas.git
cd ecoli-atlas

# Install dependencies
npm install

# Start development server
npm run dev
```

Open [http://localhost:3016](http://localhost:3016) in your browser.

### Production Build

```bash
npm run build
```

The optimized static production output is emitted to `dist/`.

---

## Repository Structure

```
ecoli-atlas/
├── app/
│   ├── anatomy.ts             # Cellular systems, Part interfaces, & biochemical descriptions
│   ├── explosion-layout.ts    # Two-tier exploded gallery coordinate mapping
│   ├── scene.tsx              # Three.js WebGL viewport, raycasting, camera damping
│   ├── page.tsx               # Studio UI, search combobox, detail sheets, system controls
│   └── globals.css            # Dark/light glassmorphic styling
├── public/
│   └── models/
│       ├── atlas.json         # Component index, bounds, & Gene Ontology metadata
│       └── body-0.bin.gz      # Compact compressed binary geometry chunk (<450 KB)
├── scripts/
│   └── build_ecoli_atlas.py   # Procedural 3D bacterial geometry generator
└── web/
    └── index.html             # Application HTML shell
```

---

## Scientific References & Data Sources

- **EcoCyc Database**: Comprehensive genomic, biochemical, and metabolic model of *Escherichia coli* K-12 ([ecocyc.org](https://ecocyc.org/)).
- **Cryo-Electron Tomography (Cryo-ET)**: Jensen Lab Atlas of Bacterial Cell Structure ([cellstructureatlas.org](https://www.cellstructureatlas.org/)).
- **RCSB PDB-101**: David S. Goodsell mesoscale cellular landscapes of the *E. coli* cytoplasm.
- **Gene Ontology (GO)** Consortium: Standardized cellular component identifiers for bacterial ultrastructure.

---

## License

[MIT License](LICENSE)
