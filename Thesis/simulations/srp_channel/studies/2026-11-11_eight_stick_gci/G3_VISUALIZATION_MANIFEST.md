# G3 Mature-Flow Visualization Manifest

- Sol job: `2314557`
- Source commit: `beb1fac`
- Grid: `768 x 192 x 192`
- MPI decomposition: `16 x 4 x 1` on 64 ranks
- Final state: `t*=3`, step `30000`
- Runtime: `32:58:22`
- Exit status: `COMPLETED`, `0:0`
- Executable SHA-256: `0935ff1d419cc37dc766bb5e5d25fd31f7de6e551767d2ce5d355f4a689ad901`
- Dataset size: `1.6 GB`
- Sol source: `/scratch/ldayal/srp_benchmark/ellipse_g3_visualization_t3_64_20261123/ensight`
- Local ignored copy: `paraview_data/g3_ellipse_t3/ensight`
- Rendered views: `paraview_data/g3_ellipse_t3/screenshots`

## Mature-state checksums

```text
21f5579326b3976a683990c209352bcf3270eb5115cdb7121f1d62f5bef66fb1  nga.case
394771d9f254e0c41a3a993a935bcf525c996a65766e0b33b14807082129a885  geometry
431c7fca41b62651f28cca69a594db02cf5f72e9098d32c213e65f3ffcc6075b  geometry.fvf
69d7f03a24c8ab7bdccfc1fe6a159032c3a70c815f56b30a671c53ec446cfb80  pressure/pressure.000002
d88046b88991cd27270dab275e3ccc864a264e8f179c55b2c86167936fcd879d  velocity/velocity.000002
b15ff47d5c3b68249695556da7830ede8e0dbaeea64f10264efad90f695796b0  porous_mask/porous_mask.000002
402124e206b75f7fd16b0c63fa775b5be2e361b7cb8f67da2a5b95a33e7e4fea  mesh_mask/mesh_mask.000002
64a8183c481e822effb126321c96388facd398cc5667095e82c2682120291602  wall_vf/wall_vf.000002
```

The Sol copy is temporary scratch storage. Preserve the local dataset on
external or backed-up storage before scratch expiration. Large generated fields
and screenshots remain excluded from Git.
