# -
已知蛋白、配体（小分子）fasta序列\SMILE序列，预测蛋白-小分子复合物结构
现在这种情况（蛋白序列 + 小分子）：

✔️ 标准 pipeline（最靠谱）
Step 1：蛋白结构预测

用：

AlphaFold2 / ColabFold

得到：

蛋白3D结构（PDB）
Step 2：小分子结构准备

用：

RDKit / OpenBabel
生成：
3D conformer
SDF / MOL2
Step 3：分子对接（关键步骤）

工具：

AutoDock Vina
Glide（Schrödinger）
GOLD
DiffDock（深度学习）

👉 输入：

蛋白结构
小分子结构

👉 输出：

结合位点 + pose
Step 4（可选）：复合物 refinement

用：

分子动力学（GROMACS / AMBER）
或 Rosetta relax
