# -*- coding: utf-8 -*-
from rdkit import Chem
from rdkit.Chem import AllChem

# 1. SMILES
smiles = "CC1=C(C(=O)N(N1)C)C(=O)C2=C(C=C(C=C2)C(F)(F)F)S(=O)(=O)C"  # 小分子的 SMILES 表示
mol = Chem.MolFromSmiles(smiles)

# 2. 加氢
mol = Chem.AddHs(mol)

# 3. 生成多构象（ETKDG）
params = AllChem.ETKDGv3()
params.numThreads = 6  # 用6线程
params.pruneRmsThresh = 0.5  # RMSD筛选阈值

conf_ids = AllChem.EmbedMultipleConfs(
    mol,
    numConfs=20,   # 生成20个构象
    params=params
)

# 4. 能量最小化（MMFF）
results = AllChem.MMFFOptimizeMoleculeConfs(mol)

# 5. 输出能量
energies = [r[1] for r in results]

# 6. 排序（从低到高）
sorted_confs = sorted(zip(conf_ids, energies), key=lambda x: x[1])

print("Lowest energy:", sorted_confs[0])

# =========================
# 7. 选前5个构象并保存
# =========================

top_n = 5

# 保存为 SDF（推荐保留所有信息）
writer = Chem.SDWriter("top_confs.sdf")

for i, (conf_id, energy) in enumerate(sorted_confs[:top_n]):
    mol.SetProp("Conf_ID", str(conf_id))
    mol.SetProp("Energy", str(energy))
    writer.write(mol, confId=conf_id)

writer.close()

print(f"Saved top {top_n} conformers to top_confs.sdf")

# =========================
# 8. 同时导出 PDB（对接常用）
# =========================

for i, (conf_id, energy) in enumerate(sorted_confs[:top_n]):
    pdb_filename = f"conf_{i}_E_{energy:.2f}.pdb"
    Chem.MolToPDBFile(mol, pdb_filename, confId=conf_id)

print("PDB files saved.")