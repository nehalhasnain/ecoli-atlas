export type SystemId = 'envelope'|'cell_wall'|'periplasm'|'plasma_membrane'|'appendages'|'nucleoid'|'plasmids'|'ribosomes'|'machinery'|'storage'|'cytoplasm';

export const SYSTEMS: {id:SystemId;name:string;color:string;description:string}[] = [
 {id:'envelope',name:'Outer Envelope & LPS',color:'#e54d2e',description:'The outer barrier of Gram-negative bacteria, consisting of lipopolysaccharides (LPS), outer membrane porins, and an asymmetric lipid bilayer providing protection against bile salts and hydrophobic antibiotics.'},
 {id:'cell_wall',name:'Peptidoglycan Cell Wall',color:'#d8b565',description:'The murein sacculus: a covalently closed, mesh-like single layer of glycan strands cross-linked by peptide bridges that maintains cell shape and withstands internal turgor pressure (target of beta-lactam antibiotics).'},
 {id:'periplasm',name:'Periplasmic Space',color:'#f76b15',description:'A concentrated gel-like compartment between inner and outer membranes packed with nutrient-binding proteins, molecular chaperones, folding catalysts (DsbA/B), and hydrolytic enzymes.'},
 {id:'plasma_membrane',name:'Inner (Plasma) Membrane',color:'#30a46c',description:'Symmetric phospholipid bilayer hosting electron transport complexes, proton motive force generation, transport permeases, lipid/peptidoglycan synthases, and sensory kinases.'},
 {id:'appendages',name:'Flagella & Pili',color:'#ffd60a',description:'Surface motility and adhesion appendages, including peritrichous helical flagella driven by proton-motive rotary motors, Type 1 fimbriae with FimH adhesin, and conjugative sex pili.'},
 {id:'nucleoid',name:'Nucleoid (Chromosome)',color:'#3b82f6',description:'The compact 4.64-Mbp circular double-stranded genomic DNA, topologically organized into supercoiled loops by Nucleoid-Associated Proteins (NAPs: HU, H-NS, Fis, IHF) without a nuclear membrane.'},
 {id:'plasmids',name:'Plasmids',color:'#a855f7',description:'Autonomous, self-replicating extrachromosomal circular DNA elements carrying non-essential accessory genes, including antibiotic resistance (e.g. beta-lactamase) and fertility factors (F-plasmid).'},
 {id:'ribosomes',name:'70S Ribosomes',color:'#06b6d4',description:'Bacterial protein translation factories consisting of a 30S small subunit (16S rRNA) and a 50S large subunit (23S and 5S rRNA), translating mRNA concurrently with transcription.'},
 {id:'machinery',name:'Enzyme Complexes & ATP Synthase',color:'#ec4899',description:'Vital macromolecular multi-subunit complexes, including F1F0-ATP synthase rotary engines converting PMF into ATP, and RNA polymerase transcription holoenzymes.'},
 {id:'storage',name:'Storage Granules',color:'#84cc16',description:'Cytoplasmic inclusion bodies, including polyphosphate (volutin) granules and glycogen bodies used for energy, phosphate, and carbon reserves.'},
 {id:'cytoplasm',name:'Cytoplasmic Matrix',color:'#94a3b8',description:'The densely crowded colloidal cytosol (~300-400 mg/mL macromolecules) containing metabolic enzymes, chaperones (GroEL/ES, DnaK), tRNA, and dissolved metabolites.'},
];

export interface Part {id:string;name:string;conceptId:string;system:SystemId;chunk:number;positions:number;normals:number;indices:number;vertexCount:number;indexCount:number;bounds:[number[],number[]]}
export interface Concept {id:string;name:string;elements:string[]}
export interface Atlas {version:string;sex?:'male';source?:string;scope?:string;parts:Part[];concepts:Concept[];chunks:{url:string;bytes:number;gzip?:string;gzipBytes?:number}[];triangles:number}
export type View = 'three-quarter'|'front'|'back'|'side';
export interface SceneState {inspectorOpen?:boolean;explode:number;visible:SystemId[];selected:string[];isolate:boolean;view:View;rotate:boolean;reset:number}

export const DEFAULT_VISIBLE:SystemId[] = ['envelope','cell_wall','periplasm','plasma_membrane','appendages','nucleoid','plasmids','ribosomes','machinery','storage'];

export const EXPLANATIONS:Record<string,string> = {
 'lipopolysaccharide (lps) outer layer (o-antigen & core)':
  'The outer leaflet of the outer membrane. A tripartite glycolipid complex comprising: (1) Lipid A (endotoxin)—a β-D-glucosaminyl-(1→6)-α-D-glucosamine disaccharide phosphorylated at positions 1 and 4\' and acylated with 6 saturated fatty acids (e.g. β-hydroxymyristate) that anchors LPS into the membrane and acts as a potent agonist of TLR4/MD-2, triggering septic shock; (2) Core Oligosaccharide—a conserved inner core containing KDO (3-deoxy-D-manno-oct-2-ulosonic acid) and heptose sugars cross-linked by divalent cations (Mg²⁺, Ca²⁺) to stabilize outer leaflet packing, plus an outer hexose core; and (3) O-Antigen—a polymorphic polysaccharide chain of repeating oligosaccharide units extending into the extracellular space, governing O-serotype (e.g., O157, O104) and conferring resistance against complement lysis and phagocytosis. Imparts a strong negative charge and creates an impenetrable crystalline barrier against hydrophobic antibiotics, detergents, and bile salts.',

 'outer membrane (asymmetric bilayer & omps)':
  'An asymmetric 7–8 nm lipid bilayer unique to Gram-negative bacteria. The outer leaflet is composed almost exclusively of LPS, whereas the inner leaflet is composed of standard phospholipids (75% phosphatidylethanolamine, 20% phosphatidylglycerol, 5% cardiolipin). The outer membrane functions as a selective permeability barrier and hosts essential transmembrane β-barrel outer membrane proteins (OMPs), including trimeric porins (OmpF/OmpC) for nutrient uptake, structural anchors (OmpA), and active TonB-dependent transport ducts. Biogenesis requires the Sec translocon, periplasmic chaperones (SurA/DegP), and the essential β-barrel Assembly Machinery (BAM complex). Covalently tethered to the underlying peptidoglycan meshwork by ~1 million Braun\'s lipoprotein (Lpp) cross-linkers.',

 'periplasmic space & transport gel':
  'A specialized, redox-active aqueous gel compartment comprising 20–40% of total bacterial cell volume located between the inner and outer membranes. Maintains an iso-osmotic buffer packed with molecular chaperones (SurA, Skp, DegP), disulfide bond formation and isomerization catalysts (DsbA, DsbB, DsbC, DsbD), hydrolytic enzymes (alkaline phosphatase), and high-affinity periplasmic substrate-binding proteins (SBPs) that shuttle sugars, amino acids, and inorganic ions to inner membrane ABC transporters. Protected by the outer membrane and essential for protein quality control and envelope homeostasis.',

 'peptidoglycan sacculus (cell wall mesh)':
  'The bacterial murein sacculus: a single bag-shaped, covalently closed macromolecular cage surrounding the cytoplasmic membrane. Composed of linear glycan strands of alternating β-(1→4)-linked N-acetylglucosamine (GlcNAc) and N-acetylmuramic acid (MurNAc), cross-linked by flexible peptide stems containing L-Ala, D-Glu, meso-diaminopimelic acid (meso-DAP), and D-Ala. The sacculus confers mechanical rigidity, defines rod morphology, and withstands internal turgor pressures of 3–5 atmospheres, preventing osmotic lysis. Target of penicillin, ampicillin (beta-lactams inhibiting transpeptidases), and lysozyme (cleaving the glycan backbone).',

 'inner cytoplasmic membrane (phospholipid bilayer)':
  'A symmetric, highly dynamic fluid mosaic phospholipid bilayer (~4 nm thick) consisting predominantly of phosphatidylethanolamine (PE, ~75%), phosphatidylglycerol (PG, ~20%), and cardiolipin (~5%). Serves as the primary metabolic and bioenergetic barrier of the cell. Houses respiratory electron transport chain complexes (NADH dehydrogenases, quinones, cytochrome oxidases) that pump protons to generate the transmembrane proton motive force (PMF, Δp = ΔΨ - 60ΔpH ~ -180 to -220 mV). Anchors nutrient transport permeases, lipid and cell wall biosynthetic enzymes, sensor kinases for two-component regulatory systems, and the SecYEG translocon.',

 'porin trimer channels (ompf / ompc)':
  'Trimeric β-barrel transmembrane channels spanning the outer membrane. Each monomer forms a 16-stranded anti-parallel β-barrel with an internal pore constricted by loop L3 (exclusion limit ~600 Da). Allows passive diffusion of water, ions, and small hydrophilic nutrients (glucose, amino acids) into the periplasm. OmpF has a wider pore (~1.1 nm) and is expressed in low-osmolarity conditions, whereas OmpC has a narrower pore (~0.9 nm) and is favored under high osmolarity and bile salt stress.',

 'braun lipoprotein (lpp) cross-linkers':
  'The most numerically abundant protein in E. coli (~10⁶ copies per cell). A small (7.2 kDa) trimeric α-helical coiled-coil anchored to the inner leaflet of the outer membrane via an N-terminal lipid moiety. Approximately one-third of Lpp molecules are covalently cross-linked via their C-terminal lysine to the meso-DAP residue of the peptidoglycan sacculus by L,D-transpeptidases (LdtA-E), providing essential mechanical tethering between the outer membrane and the cell wall.',

 'type 1 fimbriae (pili) with fimh adhesin tips':
  'Rigid, hair-like proteinaceous surface appendages (~1–2 µm long, 7 nm diameter) distributed peritrichously across the cell. Assembled via the chaperone-usher pathway (FimC/FimD) from ~1,000 polymerized FimA rod subunits, capped by a distal tip complex containing the FimH adhesin. FimH binds terminal D-mannose residues on host epithelial cell glycoproteins with "catch-bond" kinetics, mediating colonization of the urinary and gastrointestinal tracts.',

 'anterior-left flagellar filament (flic)':
  'A long (~5–10 µm), semi-rigid left-handed helical corkscrew filament composed of ~20,000 subunits of flagellin (FliC) protein assembled by a Type III flagellar export apparatus. Counterclockwise (CCW) rotation bundles all peritrichous filaments together at the posterior pole into a coordinated propeller, driving smooth forward swimming ("run") at speeds up to 30 µm/s.',

 'lateral-left flagellar filament (flic)':
  'Helical flagellin filament. Clockwise (CW) rotation unbundles the flagellar bundle, causing the bacterium to tumble and reorient randomly before the next run, enabling directed three-dimensional chemotaxis toward nutrient attractants and away from repellents.',

 'posterior-left flagellar filament (flic)':
  'Peritrichous helical flagellin filament propelled by its proton-driven basal rotary motor, dynamically coordinated during run-and-tumble chemotactic navigation.',

 'dorsal-posterior flagellar filament (flic)':
  'Dorsal helical flagellin filament cooperating with other filaments in the multi-flagellar propulsive bundle.',

 'flagellar basal motors (l, p, ms, c rings & mota/b stator)':
  'A high-torque reversible rotary nanomotor spanning the entire cell envelope. Consists of a rotor (MS ring in the inner membrane, C ring switch complex in the cytoplasm, P ring in the peptidoglycan, and L ring in the outer membrane) and stator complexes (MotA₄MotB₂) anchored to the peptidoglycan. Utilizes transmembrane proton flux (H⁺ translocation) to generate torque, rotating the flagellar hook and filament at speeds up to 100,000 RPM.',

 'nucleoid (circular 4.64 mb chromosome & naps)':
  'The compact, highly organized genetic core of E. coli containing a single circular double-stranded DNA genome (4,641,652 base pairs in K-12 MG1655; 4,288 protein-coding genes). Lacking a nuclear envelope, the chromosome is dynamically organized into ~400 topological looped domains (plectonemic supercoiling maintained by DNA gyrase and topoisomerase IV) and compacted by Nucleoid-Associated Proteins (NAPs) including HU, H-NS, Fis, and IHF.',

 'small high-copy plasmid (puc19 / cole1 with bla resistance)':
  'A high-copy (~500–700 copies/cell) 2,686-bp autonomous cloning vector derived from ColE1. Replicates unidirectionally via an RNA I / RNA II / Rom-regulated mechanism independent of chromosomal replication. Carries the bla gene encoding TEM-1 β-lactamase, which hydrolyzes the β-lactam ring of penicillins and ampicillin to confer high-level antibiotic resistance, and the lacZα marker for blue-white colony screening.',

 'large low-copy conjugative f-plasmid (fertility factor)':
  'A 99.2-kb circular conjugative plasmid present at 1–2 copies per cell. Encodes the complete tra (transfer) operon of ~33 genes responsible for Type IV secretion machinery and the conjugative F-pilus. Mediates horizontal gene transfer (HGT) by forming mating pairs with recipient (F-) bacteria, transferring single-stranded DNA via rolling-circle replication. Can integrate into the chromosome to yield Hfr (high frequency of recombination) strains.',

 '70s ribosome complexes (30s + 50s translation machinery)':
  'Bacterial ribonucleoprotein translation factories (~2.5 MDa; ~20 nm diameter; 20,000–50,000 copies per actively dividing cell). Composed of a small 30S subunit (16S rRNA + 21 r-proteins) responsible for mRNA decoding and codon-anticodon fidelity, and a large 50S subunit (23S rRNA, 5S rRNA + 34 r-proteins) housing the peptidyl transferase center (PTC). Transcribes and translates concurrently in coupled polysome clusters; prime target of aminoglycosides, tetracyclines, and macrolides.',

 'rna polymerase transcription complexes (sigma70 factor)':
  'The core transcription machinery (α₂ββ\'ω; ~400 kDa) coupled to the primary vegetative sigma-70 (RpoD) initiation factor to form the transcription holoenzyme. Recognizes consensus -10 (Pribnow box) and -35 promoter elements to initiate gene transcription, unwinding DNA to form the open promoter complex. Coordinates closely with ribosomes in transcription-translation coupling (expressome).',

 'f1f0-atp synthase complexes (proton motive rotary engine)':
  'A multisubunit rotary molecular engine embedded in the inner cytoplasmic membrane. Composed of an inner-membrane F0 proton channel (a, b₂, c₁₀₋₁₂) and a catalytic F1 headpiece (α₃β₃γδε) protruding into the cytoplasm. Driven by the inward flux of protons down the proton motive force (PMF), the c-ring and γε central stalk rotate at hundreds of revolutions per second, driving conformational changes in the catalytic β subunits that synthesize ATP from ADP and inorganic phosphate.',

 'polyphosphate (volutin) & glycogen energy reserve granules':
  'Dense, insoluble cytoplasmic inclusion bodies used for dynamic metabolic storage. Polyphosphate (volutin) granules consist of long linear chains of inorganic phosphate synthesized by polyphosphate kinase (PPK), serving as an energy reserve, phosphate buffer, and chelator of toxic heavy metals during nutritional stress and stationary phase. Glycogen granules store high-molecular-weight branched α-glucan polymers as carbon and energy reserves.',
};

export function explanation(name:string,system:SystemId){
 const key = name.toLowerCase().trim();
 return EXPLANATIONS[key] ?? SYSTEMS.find(s=>s.id===system)?.description ?? '';
}

