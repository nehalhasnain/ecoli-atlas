import type {Part} from './anatomy';

export interface LayoutCell {
  x: number;
  y: number;
  width: number;
  height: number;
}

// Perfectly balanced two-tier exploded layout:
// TOP TIER: The 5 Capsule & Envelope Shells horizontally aligned across the canvas.
// MIDDLE TIER: Internal macromolecular complexes (Nucleoid, Plasmids, Ribosomes, RNAP, Granules, ATP Synthase).
// BOTTOM TIER: Surface Appendages (Pili / Fimbriae, 4 Flagellar Filaments, Basal Motors, Porins, Lpp).
// Everything internal and appendages stays strictly BELOW the capsules.
const PART_OFFSETS: Record<string, { x: number; y: number }> = {
  // --- TOP TIER (Capsule & Cell Envelope Shells) ---
  // World Y = +0.95 -> cell.y = +0.10
  'EC_LPS':               { x: -1.90, y:  0.10 }, // 1. Outer LPS Capsule Layer (coral red)
  'EC_OM':                { x: -0.95, y:  0.10 }, // 2. Outer Membrane Bilayer (crimson red)
  'EC_PERI':              { x:  0.00, y:  0.10 }, // 3. Periplasmic Space Shell (amber orange)
  'EC_PG':                { x:  0.95, y:  0.10 }, // 4. Peptidoglycan Cell Wall Sacculus (golden mesh)
  'EC_IM':                { x:  1.90, y:  0.10 }, // 5. Inner Cytoplasmic Membrane (emerald green)

  // --- MIDDLE TIER (Internal Macromolecules - strictly below the shells) ---
  // World Y = -0.28 -> cell.y = -1.13
  'EC_NUCLEOID':          { x: -1.90, y: -1.13 }, // Supercoiled circular chromosome (under LPS)
  'EC_PLASMID_1':         { x: -1.15, y: -1.05 }, // Small pUC19 plasmid (bla resistance)
  'EC_PLASMID_2':         { x: -0.75, y: -1.20 }, // Large conjugative F-plasmid
  'EC_RIBOSOMES':         { x:  0.00, y: -1.13 }, // 70S Translation complexes (cyan)
  'EC_RNAP':              { x:  0.75, y: -1.10 }, // RNA Polymerase complexes (pink)
  'EC_STORAGE_GRANULES':  { x:  1.15, y: -1.18 }, // Energy reserve inclusion granules (green)
  'EC_ATP_SYNTHASE':      { x:  1.90, y: -1.13 }, // Rotary F1F0 ATP Synthases (under IM)

  // --- BOTTOM TIER (Surface Appendages & Pili - strictly along the bottom) ---
  // World Y = -0.98 -> cell.y = -1.83
  'EC_FIMBRIAE':          { x: -1.90, y: -1.83 }, // Type 1 Fimbriae / Pili (under nucleoid)
  'EC_FLAG_1':            { x: -1.15, y: -1.83 }, // Anterior Flagellar Filament wave
  'EC_FLAG_2':            { x: -0.55, y: -1.83 }, // Lateral Flagellar Filament wave
  'EC_FLAG_3':            { x:  0.10, y: -1.83 }, // Posterior Flagellar Filament wave
  'EC_FLAG_4':            { x:  0.75, y: -1.83 }, // Dorsal Flagellar Filament wave
  'EC_FLAG_MOTORS':       { x:  1.30, y: -1.83 }, // Flagellar basal motor complexes
  'EC_PORINS':            { x:  1.75, y: -1.83 }, // Outer Membrane Porin trimers
  'EC_LPP':               { x:  2.05, y: -1.83 }, // Braun Lipoprotein cross-linkers
};

export function createExplosionLayout(parts: Part[], _aspect = 1) {
  const cells = new Map<string, LayoutCell>();
  for (const p of parts) {
    const coord = PART_OFFSETS[p.id] ?? { x: 0, y: 0 };
    cells.set(p.id, {
      x: coord.x,
      y: coord.y,
      width: Math.max(0.4, p.bounds[1][0] - p.bounds[0][0]),
      height: Math.max(0.4, p.bounds[1][1] - p.bounds[0][1]),
    });
  }
  return { cells, width: 5.0, height: 3.0 };
}

