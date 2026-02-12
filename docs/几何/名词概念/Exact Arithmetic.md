# 精确算术
给定直线 $L: P = P_0 + t \cdot \vec{d}$，其中：
- $P_0 = (x_0, y_0, z_0)$ 是直线上一点
- $\vec{d} = (d_x, d_y, d_z)$ 是方向向量
- $t \in \mathbb{R}$ 是参数

判断直线 $L$ 与单位立方体 $[0,1]^3 = \{(x,y,z) \mid 0 \leq x,y,z \leq 1\}$ 的关系。

## 几何关系分类：
- 相交：$L$穿过立方体内部
- 相切：$L$与立方体表面接触但不穿过内部
- 相离：$L$与立方体无交点
- 包含：$L$段完全在立方体内部（特殊情况）
  
  问题关键在于找到$L$与单位立方体的六个面的所有有效交点参数$t$

## 核心步骤
$P_0 = \left(\frac{a_x}{b_x}, \frac{a_y}{b_y}, \frac{a_z}{b_z}\right), \quad 
\vec{d} = \left(\frac{c_x}{d_x}, \frac{c_y}{d_y}, \frac{c_z}{d_z}\right)$


