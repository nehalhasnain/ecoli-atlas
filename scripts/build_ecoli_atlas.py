#!/usr/bin/env python3
"""Build a scientifically accurate, museum-grade 3D anatomical atlas of Escherichia coli K-12.

Key design principles:
1. Two-tier exploded macromolecular inventory layout:
   - TOP ROW: Capsule & cell envelope shells (LPS, Outer Membrane, Periplasm, Peptidoglycan Sacculus, Inner Membrane).
   - BOTTOM ROW: Internal organelles & pili/appendages (Fimbriae, Flagella, Porins, Ribosomes, Nucleoid, Plasmids, Enzymes, Granules).
2. Sleek, professional anatomical geometry on the first 2 red envelope organelles (stepped rims, bilayer edges, embedded channels).
3. Seamless assembled state with stepped front-facing cutaway window.
"""

import sys, json, math, struct
from pathlib import Path
from array import array

root = Path(__file__).resolve().parents[1]
out_dir = root / 'public/models'
out_dir.mkdir(parents=True, exist_ok=True)

def normalize(v):
    l = math.hypot(*v)
    return [x / (l or 1.0) for x in v]

def cross(a, b):
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ]

def add_mesh_data(target_verts, target_norms, target_indices, new_verts, new_norms, new_indices):
    base_idx = len(target_verts) // 3
    target_verts.extend(new_verts)
    target_norms.extend(new_norms)
    for idx in new_indices:
        target_indices.append(base_idx + idx)

def make_tube_along_curve(points, radius=0.012, n_circ=8, closed=False):
    verts, norms, indices = [], [], []
    num_pts = len(points)
    if num_pts < 2:
        return verts, norms, indices

    rings = []
    ref_up = [0.0, 1.0, 0.0]

    for i in range(num_pts):
        p = points[i]
        if i == 0:
            tangent = [points[1][c] - points[0][c] for c in range(3)]
        elif i == num_pts - 1:
            tangent = [points[num_pts-1][c] - points[num_pts-2][c] for c in range(3)]
        else:
            tangent = [points[i+1][c] - points[i-1][c] for c in range(3)]
        t_norm = normalize(tangent)

        side = cross(t_norm, ref_up)
        if math.hypot(*side) < 0.1:
            side = cross(t_norm, [1.0, 0.0, 0.0])
        side = normalize(side)
        up = normalize(cross(side, t_norm))
        ref_up = up

        ring = []
        for j in range(n_circ):
            angle = (j / n_circ) * 2.0 * math.pi
            ca = math.cos(angle)
            sa = math.sin(angle)
            nx = side[0] * ca + up[0] * sa
            ny = side[1] * ca + up[1] * sa
            nz = side[2] * ca + up[2] * sa
            vx = p[0] + nx * radius
            vy = p[1] + ny * radius
            vz = p[2] + nz * radius
            ring.append(len(verts) // 3)
            verts.extend([vx, vy, vz])
            norms.extend([nx, ny, nz])
        rings.append(ring)

    seg_count = num_pts if closed else num_pts - 1
    for i in range(seg_count):
        r1 = rings[i]
        r2 = rings[(i + 1) % num_pts]
        for j in range(n_circ):
            v0 = r1[j]
            v1 = r2[j]
            v2 = r2[(j + 1) % n_circ]
            v3 = r1[(j + 1) % n_circ]
            indices.extend([v0, v1, v2, v0, v2, v3])

    return verts, norms, indices

def make_cylinder(base_p, top_p, radius, n_circ=8):
    return make_tube_along_curve([base_p, top_p], radius=radius, n_circ=n_circ, closed=False)

def make_sphere(center, radius, n_lat=8, n_lon=10):
    verts, norms, indices = [], [], []
    grid = []
    for i in range(n_lat + 1):
        theta = (i / n_lat) * math.pi
        sin_t = math.sin(theta)
        cos_t = math.cos(theta)
        row = []
        for j in range(n_lon + 1):
            phi = (j / n_lon) * 2.0 * math.pi
            nx = sin_t * math.cos(phi)
            ny = cos_t
            nz = sin_t * math.sin(phi)
            vx = center[0] + nx * radius
            vy = center[1] + ny * radius
            vz = center[2] + nz * radius
            row.append(len(verts) // 3)
            verts.extend([vx, vy, vz])
            norms.extend([nx, ny, nz])
        grid.append(row)
    for i in range(n_lat):
        for j in range(n_lon):
            v0 = grid[i][j]
            v1 = grid[i+1][j]
            v2 = grid[i+1][j+1]
            v3 = grid[i][j+1]
            indices.extend([v0, v1, v2, v0, v2, v3])
    return verts, norms, indices

def make_capsule_cutaway(radius, cylinder_height, center_y, phi_start_deg, phi_end_deg, thickness=0.012, n_lat=22, n_lon=32):
    """Generate a sleek cutaway capsule shell with stepped thickness rims along the cutaway boundaries."""
    verts, norms, indices = [], [], []
    y_top = center_y + cylinder_height / 2.0
    y_bot = center_y - cylinder_height / 2.0

    rad_start = math.radians(phi_start_deg)
    rad_end = math.radians(phi_end_deg)
    total_angle = rad_end - rad_start

    # Outer surface
    grid = []
    # Top hemisphere
    for i in range(n_lat // 2 + 1):
        theta = (i / (n_lat // 2)) * (math.pi / 2.0)
        sin_t = math.sin(theta)
        cos_t = math.cos(theta)
        row = []
        for j in range(n_lon + 1):
            phi = rad_start + (j / n_lon) * total_angle
            sin_p = math.sin(phi)
            cos_p = math.cos(phi)
            nx = sin_t * cos_p
            ny = cos_t
            nz = sin_t * sin_p
            vx = nx * radius
            vy = y_top + ny * radius
            vz = nz * radius
            row.append(len(verts) // 3)
            verts.extend([vx, vy, vz])
            norms.extend([nx, ny, nz])
        grid.append(row)

    # Cylinder body
    body_steps = 14
    for k in range(1, body_steps):
        frac = k / body_steps
        y_curr = y_top * (1.0 - frac) + y_bot * frac
        row = []
        for j in range(n_lon + 1):
            phi = rad_start + (j / n_lon) * total_angle
            nx = math.cos(phi)
            ny = 0.0
            nz = math.sin(phi)
            vx = nx * radius
            vy = y_curr
            vz = nz * radius
            row.append(len(verts) // 3)
            verts.extend([vx, vy, vz])
            norms.extend([nx, ny, nz])
        grid.append(row)

    # Bottom hemisphere
    for i in range(n_lat // 2 + 1):
        theta = (math.pi / 2.0) + (i / (n_lat // 2)) * (math.pi / 2.0)
        sin_t = math.sin(theta)
        cos_t = math.cos(theta)
        row = []
        for j in range(n_lon + 1):
            phi = rad_start + (j / n_lon) * total_angle
            sin_p = math.sin(phi)
            cos_p = math.cos(phi)
            nx = sin_t * cos_p
            ny = cos_t
            nz = sin_t * sin_p
            vx = nx * radius
            vy = y_bot + ny * radius
            vz = nz * radius
            row.append(len(verts) // 3)
            verts.extend([vx, vy, vz])
            norms.extend([nx, ny, nz])
        grid.append(row)

    # Quads
    for i in range(len(grid) - 1):
        for j in range(n_lon):
            v0 = grid[i][j]
            v1 = grid[i+1][j]
            v2 = grid[i+1][j+1]
            v3 = grid[i][j+1]
            indices.extend([v0, v1, v2, v0, v2, v3])

    # Add cutaway thickness rims along phi_start and phi_end
    if thickness > 0.002:
        for boundary_col, normal_sign in [(0, -1.0), (n_lon, 1.0)]:
            pts_out = [ [verts[grid[row_idx][boundary_col]*3], verts[grid[row_idx][boundary_col]*3+1], verts[grid[row_idx][boundary_col]*3+2]] for row_idx in range(len(grid)) ]
            phi_val = rad_start if boundary_col == 0 else rad_end
            norm_rim = [-math.sin(phi_val) * normal_sign, 0.0, math.cos(phi_val) * normal_sign]
            rim_grid = []
            for p in pts_out:
                v_out_idx = len(verts) // 3
                verts.extend(p)
                norms.extend(norm_rim)
                norm_rad = normalize([p[0], 0.0, p[2]])
                p_in = [p[0] - norm_rad[0] * thickness, p[1], p[2] - norm_rad[2] * thickness]
                v_in_idx = len(verts) // 3
                verts.extend(p_in)
                norms.extend(norm_rim)
                rim_grid.append((v_out_idx, v_in_idx))
            for r in range(len(rim_grid) - 1):
                o0, i0 = rim_grid[r]
                o1, i1 = rim_grid[r+1]
                if normal_sign < 0:
                    indices.extend([o0, i0, i1, o0, i1, o1])
                else:
                    indices.extend([o0, i1, i0, o0, o1, i1])

    return verts, norms, indices

def make_peptidoglycan_lattice(radius, cylinder_height, center_y, phi_start_deg, phi_end_deg):
    """Generate an authentic porous murein sacculus lattice network."""
    verts, norms, indices = [], [], []
    y_top = center_y + cylinder_height / 2.0
    y_bot = center_y - cylinder_height / 2.0

    rad_start = math.radians(phi_start_deg)
    rad_end = math.radians(phi_end_deg)
    n_rings = 16
    strut_r = 0.0038

    # Horizontal glycan strand hoops
    for i in range(n_rings + 1):
        y_curr = y_bot + (i / n_rings) * cylinder_height
        arc_pts = []
        n_pts = 24
        for j in range(n_pts + 1):
            phi = rad_start + (j / n_pts) * (rad_end - rad_start)
            arc_pts.append([math.cos(phi) * radius, y_curr, math.sin(phi) * radius])
        hv, hn, hi = make_tube_along_curve(arc_pts, radius=strut_r, n_circ=6, closed=False)
        add_mesh_data(verts, norms, indices, hv, hn, hi)

    # Vertical peptide cross-linking bridges
    n_struts = 18
    for j in range(n_struts + 1):
        phi = rad_start + (j / n_struts) * (rad_end - rad_start)
        cx = math.cos(phi) * radius
        cz = math.sin(phi) * radius
        # Top hemisphere rib
        top_pts = []
        for k in range(8):
            theta = (k / 7.0) * (math.pi / 2.0)
            vx = math.sin(theta) * cx
            vy = y_top + math.cos(theta) * radius
            vz = math.sin(theta) * cz
            top_pts.append([vx, vy, vz])
        tv, tn, ti = make_tube_along_curve(top_pts, radius=strut_r, n_circ=6)
        add_mesh_data(verts, norms, indices, tv, tn, ti)

        # Cylinder rib
        cv, cn, ci = make_cylinder([cx, y_bot, cz], [cx, y_top, cz], radius=strut_r, n_circ=6)
        add_mesh_data(verts, norms, indices, cv, cn, ci)

        # Bottom hemisphere rib
        bot_pts = []
        for k in range(8):
            theta = (math.pi / 2.0) + (k / 7.0) * (math.pi / 2.0)
            vx = math.sin(theta) * cx
            vy = y_bot + math.cos(theta) * radius
            vz = math.sin(theta) * cz
            bot_pts.append([vx, vy, vz])
        bv, bn, bi = make_tube_along_curve(bot_pts, radius=strut_r, n_circ=6)
        add_mesh_data(verts, norms, indices, bv, bn, bi)

    return verts, norms, indices

print("Generating perfected E. coli 3D anatomy (two-tier inventory edition)...")

CYL_H = 0.72
CYL_Y = 0.85
R_LPS = 0.355
R_OM = 0.336
R_PERI = 0.318
R_PG = 0.298
R_IM = 0.280

PARTS_SPEC = []

# ==============================================================================
# TOP ROW: CAPSULE & ENVELOPE SHELLS (LPS, OM, PERIPLASM, PEPTIDOGLYCAN, IM)
# ==============================================================================

# 1. Lipopolysaccharide (LPS) Layer: Rich coral red cutaway shell with stepped thickness rim
lps_v, lps_n, lps_idx = make_capsule_cutaway(R_LPS, CYL_H, CYL_Y, 110, 340, thickness=0.014, n_lat=24, n_lon=34)
PARTS_SPEC.append({
    'id': 'EC_LPS',
    'name': 'Lipopolysaccharide (LPS) Outer Layer (O-Antigen & Core)',
    'conceptId': 'GO:0009279',
    'system': 'envelope',
    'v': lps_v, 'n': lps_n, 'idx': lps_idx
})

# 2. Outer Membrane (Asymmetric Bilayer): Deep crimson/coral cutaway shell with stepped bilayer rim
om_v, om_n, om_idx = make_capsule_cutaway(R_OM, CYL_H, CYL_Y, 105, 345, thickness=0.012, n_lat=24, n_lon=34)
PARTS_SPEC.append({
    'id': 'EC_OM',
    'name': 'Outer Membrane (Asymmetric Bilayer & OMPs)',
    'conceptId': 'GO:0019867',
    'system': 'envelope',
    'v': om_v, 'n': om_n, 'idx': om_idx
})

# 3. Periplasmic Space & Transport Gel: Translucent golden-orange cutaway shell
peri_v, peri_n, peri_idx = make_capsule_cutaway(R_PERI, CYL_H, CYL_Y, 100, 350, thickness=0.010, n_lat=22, n_lon=32)
PARTS_SPEC.append({
    'id': 'EC_PERI',
    'name': 'Periplasmic Space & Transport Gel',
    'conceptId': 'GO:0042597',
    'system': 'periplasm',
    'v': peri_v, 'n': peri_n, 'idx': peri_idx
})

# 4. Peptidoglycan Cell Wall Sacculus Lattice Network: Golden open murein cage
pg_v, pg_n, pg_idx = make_peptidoglycan_lattice(R_PG, CYL_H, CYL_Y, 90, 360)
PARTS_SPEC.append({
    'id': 'EC_PG',
    'name': 'Peptidoglycan Sacculus (Cell Wall Mesh)',
    'conceptId': 'GO:0009274',
    'system': 'cell_wall',
    'v': pg_v, 'n': pg_n, 'idx': pg_idx
})

# 5. Inner (Plasma) Membrane: Sleek emerald green cutaway shell
im_v, im_n, im_idx = make_capsule_cutaway(R_IM, CYL_H, CYL_Y, 85, 365, thickness=0.010, n_lat=24, n_lon=34)
PARTS_SPEC.append({
    'id': 'EC_IM',
    'name': 'Inner Cytoplasmic Membrane (Phospholipid Bilayer)',
    'conceptId': 'GO:0005886',
    'system': 'plasma_membrane',
    'v': im_v, 'n': im_n, 'idx': im_idx
})

# ==============================================================================
# BOTTOM AREA: PILI / APPENDAGES & INTERNAL MACROMOLECULES (BELOW CAPSULES)
# ==============================================================================

# Porin Trimer Channels (OmpF/OmpC): Clean beta-barrel channels with open solute pores
porin_v, porin_n, porin_idx = [], [], []
for phi_deg in [130, 160, 190, 220, 250, 280, 310]:
    for y_offset in [-0.22, 0.0, 0.22]:
        rad = math.radians(phi_deg)
        px = math.cos(rad) * R_OM
        py = CYL_Y + y_offset
        pz = math.sin(rad) * R_OM
        norm_r = normalize([px, 0.0, pz])

        for delta_ang in [0.0, 2.0944, 4.1888]:
            cx = px + 0.014 * math.cos(rad + delta_ang)
            cy = py + 0.014 * math.sin(delta_ang)
            cz = pz + 0.014 * math.sin(rad + delta_ang)
            p_in = [cx - norm_r[0] * 0.008, cy, cz - norm_r[2] * 0.008]
            p_out = [cx + norm_r[0] * 0.010, cy, cz + norm_r[2] * 0.010]
            cv, cn, ci = make_cylinder(p_in, p_out, radius=0.0065, n_circ=8)
            add_mesh_data(porin_v, porin_n, porin_idx, cv, cn, ci)

PARTS_SPEC.append({
    'id': 'EC_PORINS',
    'name': 'Porin Trimer Channels (OmpF / OmpC)',
    'conceptId': 'GO:0015288',
    'system': 'envelope',
    'v': porin_v, 'n': porin_n, 'idx': porin_idx
})

# Braun's Lipoproteins (Lpp) linking PG to OM
lpp_v, lpp_n, lpp_idx = [], [], []
for phi_deg in range(110, 340, 25):
    for y_offset in [-0.25, -0.12, 0.0, 0.12, 0.25]:
        rad = math.radians(phi_deg)
        p1 = [math.cos(rad) * R_PG, CYL_Y + y_offset, math.sin(rad) * R_PG]
        p2 = [math.cos(rad) * R_OM * 0.99, CYL_Y + y_offset, math.sin(rad) * R_OM * 0.99]
        cv, cn, ci = make_cylinder(p1, p2, radius=0.004, n_circ=6)
        add_mesh_data(lpp_v, lpp_n, lpp_idx, cv, cn, ci)
PARTS_SPEC.append({
    'id': 'EC_LPP',
    'name': 'Braun Lipoprotein (Lpp) Cross-linkers',
    'conceptId': 'GO:0042597',
    'system': 'cell_wall',
    'v': lpp_v, 'n': lpp_n, 'idx': lpp_idx
})

# Type 1 Fimbriae (Pili): Clean golden bristles with FimH adhesin tips
fimbriae_v, fimbriae_n, fimbriae_idx = [], [], []
for phi_deg in range(115, 335, 18):
    for y_offset in [-0.30, -0.15, 0.0, 0.15, 0.30]:
        rad = math.radians(phi_deg)
        base_x = math.cos(rad) * R_LPS
        base_y = CYL_Y + y_offset
        base_z = math.sin(rad) * R_LPS
        norm_dir = normalize([base_x, 0.0, base_z])
        p1 = [base_x, base_y, base_z]
        p2 = [base_x + norm_dir[0] * 0.13, base_y + norm_dir[1] * 0.13 + 0.015, base_z + norm_dir[2] * 0.13]
        cv, cn, ci = make_cylinder(p1, p2, radius=0.0035, n_circ=6)
        add_mesh_data(fimbriae_v, fimbriae_n, fimbriae_idx, cv, cn, ci)
        sv, sn, si = make_sphere(p2, radius=0.0055, n_lat=5, n_lon=6)
        add_mesh_data(fimbriae_v, fimbriae_n, fimbriae_idx, sv, sn, si)

PARTS_SPEC.append({
    'id': 'EC_FIMBRIAE',
    'name': 'Type 1 Fimbriae (Pili) with FimH Adhesin Tips',
    'conceptId': 'GO:0009289',
    'system': 'appendages',
    'v': fimbriae_v, 'n': fimbriae_n, 'idx': fimbriae_idx
})

# Flagellar Assemblies: Helical corkscrews
flagella_anchors = [
    {'id': 'EC_FLAG_1', 'name': 'Anterior-Left Flagellar Filament (FliC)', 'phi_deg': 140, 'y': CYL_Y + 0.22, 'pitch': 1.0, 'rot': 0.0},
    {'id': 'EC_FLAG_2', 'name': 'Lateral-Left Flagellar Filament (FliC)', 'phi_deg': 180, 'y': CYL_Y - 0.22, 'pitch': -1.0, 'rot': 1.2},
    {'id': 'EC_FLAG_3', 'name': 'Posterior-Left Flagellar Filament (FliC)', 'phi_deg': 220, 'y': CYL_Y + 0.06, 'pitch': 1.1, 'rot': 2.1},
    {'id': 'EC_FLAG_4', 'name': 'Dorsal-Posterior Flagellar Filament (FliC)', 'phi_deg': 255, 'y': CYL_Y - 0.16, 'pitch': -0.9, 'rot': 3.4},
]

motors_v, motors_n, motors_idx = [], [], []

for fa in flagella_anchors:
    rad = math.radians(fa['phi_deg'])
    base_x = math.cos(rad) * R_LPS
    base_y = fa['y']
    base_z = math.sin(rad) * R_LPS
    norm_dir = normalize([base_x, 0.0, base_z])
    
    m_in = [math.cos(rad) * (R_IM * 0.98), fa['y'], math.sin(rad) * (R_IM * 0.98)]
    m_out = [math.cos(rad) * (R_LPS * 1.04), fa['y'], math.sin(rad) * (R_LPS * 1.04)]
    mv, mn, mi = make_cylinder(m_in, m_out, radius=0.022, n_circ=10)
    add_mesh_data(motors_v, motors_n, motors_idx, mv, mn, mi)

    curve_pts = []
    n_curve_steps = 75
    helix_r = 0.075
    wavelength = 0.35
    for s in range(n_curve_steps):
        dist = (s / n_curve_steps) * 0.95
        curve_angle = (dist / wavelength) * 2.0 * math.pi + fa['rot']
        hx = math.cos(curve_angle) * helix_r
        hy = math.sin(curve_angle) * helix_r * fa['pitch']
        px = base_x + norm_dir[0] * dist + hx * (-norm_dir[2])
        py = base_y + norm_dir[1] * dist + hy
        pz = base_z + norm_dir[2] * dist + hx * (norm_dir[0])
        curve_pts.append([px, py, pz])
    
    fv, fn, fi = make_tube_along_curve(curve_pts, radius=0.009, n_circ=8)
    PARTS_SPEC.append({
        'id': fa['id'],
        'name': fa['name'],
        'conceptId': 'GO:0044461',
        'system': 'appendages',
        'v': fv, 'n': fn, 'idx': fi
    })

PARTS_SPEC.append({
    'id': 'EC_FLAG_MOTORS',
    'name': 'Flagellar Basal Motors (L, P, MS, C Rings & MotA/B Stator)',
    'conceptId': 'GO:0009425',
    'system': 'appendages',
    'v': motors_v, 'n': motors_n, 'idx': motors_idx
})

# Nucleoid: 4.64 Mb circular supercoiled double-helical loops
nuc_pts = []
n_loops = 500
coil_radius_x = 0.11
coil_radius_z = 0.11
for i in range(n_loops + 1):
    t = (i / n_loops) * 2.0 * math.pi
    y = CYL_Y + 0.38 * math.sin(t)
    main_r_x = coil_radius_x * (1.0 + 0.25 * math.sin(3.0 * t))
    main_r_z = coil_radius_z * (1.0 + 0.25 * math.cos(4.0 * t))
    theta_coil = t * 9.0
    x = math.cos(t) * main_r_x + 0.028 * math.sin(theta_coil)
    z = math.sin(t) * main_r_z + 0.028 * math.cos(theta_coil)
    nuc_pts.append([x, y, z])

nuc_v, nuc_n, nuc_idx = make_tube_along_curve(nuc_pts, radius=0.016, n_circ=8, closed=True)

# oriC and ter macrodomain markers
sv_ori, sn_ori, si_ori = make_sphere([nuc_pts[0][0], nuc_pts[0][1], nuc_pts[0][2]], radius=0.034, n_lat=8, n_lon=10)
ter_idx_pos = n_loops // 2
sv_ter, sn_ter, si_ter = make_sphere([nuc_pts[ter_idx_pos][0], nuc_pts[ter_idx_pos][1], nuc_pts[ter_idx_pos][2]], radius=0.032, n_lat=8, n_lon=10)
add_mesh_data(nuc_v, nuc_n, nuc_idx, sv_ori, sn_ori, si_ori)
add_mesh_data(nuc_v, nuc_n, nuc_idx, sv_ter, sn_ter, si_ter)

PARTS_SPEC.append({
    'id': 'EC_NUCLEOID',
    'name': 'Nucleoid (Circular 4.64 Mb Chromosome & NAPs)',
    'conceptId': 'GO:0009295',
    'system': 'nucleoid',
    'v': nuc_v, 'n': nuc_n, 'idx': nuc_idx
})

# Plasmids
plasmid1_v, plasmid1_n, plasmid1_idx = [], [], []
p1_center = [0.03, CYL_Y + 0.22, 0.05]
p1_pts = []
for k in range(36):
    ang = (k / 36.0) * 2.0 * math.pi
    p1_pts.append([p1_center[0] + 0.055 * math.cos(ang), p1_center[1] + 0.012 * math.sin(ang * 2), p1_center[2] + 0.055 * math.sin(ang)])
p1_v, p1_n, p1_i = make_tube_along_curve(p1_pts, radius=0.007, n_circ=8, closed=True)
add_mesh_data(plasmid1_v, plasmid1_n, plasmid1_idx, p1_v, p1_n, p1_i)
PARTS_SPEC.append({
    'id': 'EC_PLASMID_1',
    'name': 'Small High-Copy Plasmid (pUC19 / ColE1 with bla Resistance)',
    'conceptId': 'GO:0005694',
    'system': 'plasmids',
    'v': plasmid1_v, 'n': plasmid1_n, 'idx': plasmid1_idx
})

plasmid2_v, plasmid2_n, plasmid2_idx = [], [], []
p2_center = [-0.04, CYL_Y - 0.24, 0.04]
p2_pts = []
for k in range(48):
    ang = (k / 48.0) * 2.0 * math.pi
    p2_pts.append([p2_center[0] + 0.075 * math.cos(ang), p2_center[1] + 0.018 * math.sin(ang * 3), p2_center[2] + 0.075 * math.sin(ang)])
p2_v, p2_n, p2_i = make_tube_along_curve(p2_pts, radius=0.007, n_circ=8, closed=True)
add_mesh_data(plasmid2_v, plasmid2_n, plasmid2_idx, p2_v, p2_n, p2_i)
PARTS_SPEC.append({
    'id': 'EC_PLASMID_2',
    'name': 'Large Low-Copy Conjugative F-Plasmid (Fertility Factor)',
    'conceptId': 'GO:0005694',
    'system': 'plasmids',
    'v': plasmid2_v, 'n': plasmid2_n, 'idx': plasmid2_idx
})

# 70S Ribosomes: 110 translation complexes neatly clustered
ribo_v, ribo_n, ribo_idx = [], [], []
for i in range(110):
    t = (i / 110.0) * 2.0 * math.pi
    rx = 0.17 * math.cos(t * 7.0) * (0.4 + 0.6 * math.cos(t * 3))
    ry = CYL_Y + 0.42 * math.sin(t * 11.0)
    rz = 0.17 * math.sin(t * 5.0) * (0.4 + 0.6 * math.sin(t * 2))
    sv_l, sn_l, si_l = make_sphere([rx, ry, rz], radius=0.014, n_lat=6, n_lon=8)
    add_mesh_data(ribo_v, ribo_n, ribo_idx, sv_l, sn_l, si_l)
    sv_s, sn_s, si_s = make_sphere([rx + 0.008, ry + 0.007, rz + 0.005], radius=0.010, n_lat=5, n_lon=6)
    add_mesh_data(ribo_v, ribo_n, ribo_idx, sv_s, sn_s, si_s)
PARTS_SPEC.append({
    'id': 'EC_RIBOSOMES',
    'name': '70S Ribosome Complexes (30S + 50S Translation Machinery)',
    'conceptId': 'GO:0005840',
    'system': 'ribosomes',
    'v': ribo_v, 'n': ribo_n, 'idx': ribo_idx
})

# RNA Polymerase Complexes
rnap_v, rnap_n, rnap_idx = [], [], []
for idx_pos in [45, 110, 185, 270, 360, 440]:
    p_nuc = nuc_pts[idx_pos]
    sv, sn, si = make_sphere([p_nuc[0] * 1.12, p_nuc[1], p_nuc[2] * 1.12], radius=0.017, n_lat=8, n_lon=10)
    add_mesh_data(rnap_v, rnap_n, rnap_idx, sv, sn, si)
PARTS_SPEC.append({
    'id': 'EC_RNAP',
    'name': 'RNA Polymerase Transcription Complexes (Sigma70 Factor)',
    'conceptId': 'GO:0005665',
    'system': 'machinery',
    'v': rnap_v, 'n': rnap_n, 'idx': rnap_idx
})

# F1F0-ATP Synthase rotary complexes
atp_v, atp_n, atp_idx = [], [], []
for i in range(24):
    phi_deg = 95 + (i / 24.0) * 260
    rad = math.radians(phi_deg)
    y_pos = CYL_Y - 0.28 + ((i * 7) % 24) / 24.0 * 0.56
    stalk_start = [math.cos(rad) * R_IM, y_pos, math.sin(rad) * R_IM]
    stalk_head = [math.cos(rad) * (R_IM - 0.022), y_pos, math.sin(rad) * (R_IM - 0.022)]
    cv, cn, ci = make_cylinder(stalk_start, stalk_head, radius=0.004, n_circ=6)
    sv, sn, si = make_sphere(stalk_head, radius=0.011, n_lat=6, n_lon=8)
    add_mesh_data(atp_v, atp_n, atp_idx, cv, cn, ci)
    add_mesh_data(atp_v, atp_n, atp_idx, sv, sn, si)
PARTS_SPEC.append({
    'id': 'EC_ATP_SYNTHASE',
    'name': 'F1F0-ATP Synthase Complexes (Proton Motive Rotary Engine)',
    'conceptId': 'GO:0005753',
    'system': 'machinery',
    'v': atp_v, 'n': atp_n, 'idx': atp_idx
})

# Storage Granules
gran_v, gran_n, gran_idx = [], [], []
gv1, gn1, gi1 = make_sphere([0.02, CYL_Y + 0.34, 0.05], radius=0.044, n_lat=12, n_lon=16)
gv2, gn2, gi2 = make_sphere([0.02, CYL_Y - 0.34, 0.04], radius=0.042, n_lat=12, n_lon=16)
gv3, gn3, gi3 = make_sphere([0.08, CYL_Y + 0.02, -0.03], radius=0.030, n_lat=10, n_lon=14)
add_mesh_data(gran_v, gran_n, gran_idx, gv1, gn1, gi1)
add_mesh_data(gran_v, gran_n, gran_idx, gv2, gn2, gi2)
add_mesh_data(gran_v, gran_n, gran_idx, gv3, gn3, gi3)
PARTS_SPEC.append({
    'id': 'EC_STORAGE_GRANULES',
    'name': 'Polyphosphate (Volutin) & Glycogen Energy Reserve Granules',
    'conceptId': 'GO:0030141',
    'system': 'storage',
    'v': gran_v, 'n': gran_n, 'idx': gran_idx
})

print(f"Packaging {len(PARTS_SPEC)} perfected anatomical parts into binary buffer...")

blob = bytearray()
parts_manifest = []
concepts_manifest = []
total_triangles = 0

def append_to_blob(values, fmt):
    while len(blob) % 4:
        blob.append(0)
    offset = len(blob)
    blob.extend(array(fmt, values).tobytes())
    return offset

for part in PARTS_SPEC:
    v = part['v']
    n = part['n']
    idx = part['idx']
    
    norm_16 = [round(max(-1.0, min(1.0, x)) * 32767) for x in n]
    
    po = append_to_blob(v, 'f')
    no = append_to_blob(norm_16, 'h')
    io = append_to_blob(idx, 'I')
    
    xs = v[0::3]
    ys = v[1::3]
    zs = v[2::3]
    bounds = [
        [round(min(xs), 5), round(min(ys), 5), round(min(zs), 5)],
        [round(max(xs), 5), round(max(ys), 5), round(max(zs), 5)]
    ]
    
    parts_manifest.append({
        'id': part['id'],
        'name': part['name'],
        'conceptId': part['conceptId'],
        'system': part['system'],
        'chunk': 0,
        'positions': po,
        'normals': no,
        'indices': io,
        'vertexCount': len(v) // 3,
        'indexCount': len(idx),
        'bounds': bounds
    })
    
    concepts_manifest.append({
        'id': part['conceptId'],
        'name': part['name'],
        'elements': [part['id']]
    })
    
    total_triangles += len(idx) // 3

# Remove old chunks
for old_bin in out_dir.glob('body-*.bin*'):
    old_bin.unlink()

bin_path = out_dir / 'body-0.bin'
bin_path.write_bytes(blob)

chunks = [{'url': '/models/body-0.bin', 'bytes': len(blob)}]
atlas = {
    'version': 'Escherichia coli K-12 MG1655 Ultrastructure Atlas 1.0',
    'parts': parts_manifest,
    'concepts': concepts_manifest,
    'chunks': chunks,
    'triangles': total_triangles
}

atlas_path = out_dir / 'atlas.json'
atlas_path.write_text(json.dumps(atlas, separators=(',', ':')))

print(f"Successfully perfected E. coli atlas!")
print(f"Parts: {len(parts_manifest)}")
print(f"Triangles: {total_triangles:,}")
print(f"Binary chunk size: {len(blob) / 1024:.1f} KB")
