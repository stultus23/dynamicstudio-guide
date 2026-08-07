# Chapter 16: Python Link（Python 链接与分析模块）

> 完整原文：`raw/ch16.txt`（10956 行）· 各小节均标注打印页码，可据此在原文中定位。

## 核心概念

The Python integration in DynamicStudio allows the creation of custom analysis methods for
DynamicStudio in Python.
The documentation is separate from this manual and is accessed by either clicking the "Help" but-
ton in "File->Python" or clicking the help icon for the method in the method selection or the method
itself, as indicated by the green box in the screenshots below:

## 操作步骤（关键操作）

### 使用 Adaptive PIV（自适应互相关，推荐默认）
- **UI 路径**：Analysis → Adaptive PIV
- **关键参数**：
  - Grid Step Size（IA 间距，决定矢量密度）
  - Min / Max IA Size（IA 尺寸自适应范围）
  - Window/Filter（空间窗函数与频域滤波）
  - Validation（验证方法）
- **步骤**：
  1. 选择输入数据（图像集合）
  2. 配置 Interrogation areas 参数
  3. 设置 Windowing and Filtering
  4. 配置 Validation 方法
  5. 点击 Apply 执行分析

### 使用 DIC（数字图像相关）
- **UI 路径**：Analysis → Digital Image Correlation (DIC)
- **步骤**：
  1. DIC Calibration（标定相机系统）
  2. DIC Processing（处理散斑图像）
  3. DIC Results（查看应变/位移结果）

### 使用模态分析（POD/sPOD/mPOD/FMD）
- **UI 路径**：Analysis → Modal Analysis
- **关键参数**：
  - Mode Count（模态数量）
  - Mean handling（均值处理）
  - Outliers handling（离群值处理）
- **步骤**：
  1. 选择输入数据（时间序列）
  2. 选择分解方法（POD/sPOD/mPOD/FMD）
  3. 配置参数
  4. 执行分析
  5. 查看模态结果

### 使用相机标定
- **UI 路径**：Analysis → Camera Calibration
- **UI 六部分**：
  1. Preview（靶标图像预览）
  2. Image scrollbar（图像滚动）
  3. Target settings（靶标设置）
  4. Calibration model（标定模型）
  5. Search settings（搜索设置）
  6. Search areas（搜索区域）
- **步骤**：
  1. 选择标定靶标类型
  2. 采集标定图像
  3. 配置搜索设置
  4. 选择标定模型（DLT/Pinhole/等）
  5. 执行标定

### 使用 BOS（背景纹影）
- **UI 路径**：Analysis → Background Oriented Schlieren (BOS)
- **步骤**：
  1. 输入背景图像和目标图像
  2. 配置 BOS Analysis Recipe
  3. 执行分析
  4. Display/Export 结果

### 使用 Python Link
- **UI 路径**：File → Python
- **步骤**：
  1. 打开 Python 编辑器
  2. 编写或加载 Python 脚本
  3. 配置输入数据
  4. 执行脚本
  5. 查看输出结果
- **说明**：文档通过 Help 按钮或方法帮助图标访问

### 使用 MATLAB Link
- **UI 路径**：Analysis → MATLAB Link
- **步骤**：
  1. 配置 MATLAB 连接
  2. 选择数据传输到 MATLAB
  3. 在 MATLAB 中处理数据
  4. 将结果返回 DynamicStudio

### 使用图像处理库（IPL）
- **UI 路径**：Analysis → Image Processing Library (IPL)
- **滤波器类型**：
  - Low-pass filters（低通滤波）
  - High-pass filters（高通滤波）
  - Morphology filters（形态学滤波）
  - Utility filters（工具滤波）
  - Signal processing（信号处理）
  - Custom filter（自定义滤波）

## 章节目录（含页码）

- `16` Python Link … p.471
- `16.1` 2D Least squares matching (LSM) … p.471
  - `16.1.1` Background information … p.472
  - `16.1.2` Usage … p.472
  - `16.1.3` References … p.473
- `16.2` 2-Frame 2D PTV … p.474
  - `16.2.1` 1. How it works … p.474
  - `16.2.2` 2. Graphical User Interface … p.474
  - `16.2.3` 3. Typical use … p.475
- `16.3` Time-Resolved 2D PTV … p.476
  - `16.3.1` Applying the Time-Resolved 2D PTV … p.477
  - `16.3.2` Interface and settings … p.477
- `16.4` 3D Particle Tracking Velocimetry … p.478
  - `16.4.1` Applying the 3D Particle Tracking Velocimetry … p.479
  - `16.4.2` Interface and settings … p.479
  - `16.4.3` Analysis process … p.480
- `16.5` Active Image Stitching … p.482
  - `16.5.1` Input to Image Stitching … p.482
  - `16.5.2` Recipe for Active Image Stitching … p.483
  - `16.5.3` Pitfalls … p.485
- `16.6` Adaptive PIV … p.485
  - `16.6.1` Interrogation areas … p.486
  - `16.6.2` Windowing and Filtering … p.487
  - `16.6.3` Validation … p.488
  - `16.6.4` Adaptivity … p.489
  - `16.6.5` Diagnostic … p.493
  - `16.6.6` Reference Vector Map … p.495
- `16.7` Adaptive Shadow Tracking … p.495
  - `16.7.1` Theory … p.495
  - `16.7.2` User interface (UI) … p.499
  - `16.7.3` Detection procedure and results … p.504
  - `16.7.4` Example … p.508
- `16.8` Calibrate Analog inputs … p.508
  - `16.8.1` How to set calibration values? … p.508
  - `16.8.2` Calibration … p.509
- `16.9` Auto-Correlation … p.510
- `16.10` Static Mask Generator - Intensity Statistics … p.510
  - `16.10.1` Theory … p.510
  - `16.10.2` Automask Generator implemented in DynamicStudio … p.511
  - `16.10.3` Pitfalls, Tips & Tricks … p.514
  - `16.10.4` References … p.515
- `16.11` Static Mask Generator – Ensemble Summation … p.515
- `16.12` When to use Average Correlation? … p.519
  - `16.12.1` Using Average Correlation to look at average PIV signal conditions … p.519
  - `16.12.2` Using an offset vector map to improve the results … p.520
  - `16.12.3` Using preconditioning to minimize influence from out of focus particles … p.521
  - `16.12.4` Schematic of Average Correlation … p.521
- `16.13` Average Filter … p.524
- `16.14` Background Oriented Schlieren (BOS) … p.526
  - `16.14.1` Input to BOS Analysis … p.527
  - `16.14.2` Recipe for BOS Analysis … p.528
  - `16.14.3` Displaying BOS results … p.530
  - `16.14.4` Exporting BOS results … p.537
  - `16.14.5` BOS Pattern Generator … p.539
- `16.15` Camera Calibration … p.541
- `1` - A preview of the target image and if detected the markers in blue … p.543
- `2` - A scrollbar for the different images required for the calibration … p.543
- `3` - A target setting option. here the target can be selected, the coordinate system can be defined … p.543
- `4` - The calibration model to be used … p.543
- `5` - Search settings to search the target or to search in specific regions defined in 6 … p.543
- `6` - Add specific target regions, if you have difficultiesproperly detecting the target markers … p.543
  - `16.15.1` Search Settings … p.542
  - `16.15.2` Search Areas … p.545
  - `16.15.3` Coordinate System … p.549
  - `16.15.4` Calibration Models … p.550
  - `16.15.5` Active Target Calibration … p.550
- `16.16` Calibration refinement … p.551
  - `16.16.1` Required input … p.552
  - `16.16.2` Refinement Area … p.553
  - `16.16.3` Frame … p.554
  - `16.16.4` Interrogation Area Size … p.554
  - `16.16.5` Disparity Map … p.554
  - `16.16.6` Dewarped Particle Images … p.555
  - `16.16.7` Average Correlation Map … p.556
  - `16.16.8` Interpreting correlation maps … p.557
  - `16.16.9` Interpreting Disparity Vectors … p.557
  - `16.16.10` Change of Coordinate System … p.559
- `16.17` Coherence Filter … p.560
- `16.18` Combine Tracks … p.562
  - `16.18.1` Inputs: … p.563
  - `16.18.2` Out puts: … p.564
  - `16.18.3` Settings and how to: … p.565
- `16.19` Combustion LIF processing … p.565
  - `16.19.1` Image analysis … p.565
  - `16.19.2` Interpretation of the results … p.567
- `16.20` Curve fit processing … p.567
  - `16.20.1` Curve fitting procedure … p.567
  - `16.20.2` Open data fit as numeric … p.569
  - `16.20.3` Overview on non-linear fitmodels … p.570
- `16.21` Cylindrical coordinate transform … p.570
- `16.22` Define Mask … p.571
  - `16.22.1` Adding shapes to the mask … p.573
  - `16.22.2` Deleting shapes … p.573
  - `16.22.3` Selecting multiple shapes … p.574
  - `16.22.4` Ordering shapes … p.574
  - `16.22.5` Preview the final mask … p.574
  - `16.22.6` Vector map Overlay … p.574
- `16.23` Diameter Statistics … p.574
- `16.24` Digital Image Correlation (DIC) … p.577
  - `16.24.1` DIC Calibration … p.577
  - `16.24.2` DIC Processing … p.579
  - `16.24.3` DIC Results … p.581
- `16.25` Dynamic background removal … p.584
  - `16.25.1` Initial POD Analysis … p.585
  - `16.25.2` Background estimation and removal … p.588
  - `16.25.3` References … p.591
- `16.26` Ensemble PTV … p.591
  - `16.26.1` How it works … p.591
  - `16.26.2` Graphical User Interface … p.591
  - `16.26.3` Typical Use … p.593
  - `16.26.4` Results … p.594
- `16.27` Extract … p.595
  - `16.27.1` Examples … p.595
- `16.28` Feature Tracking … p.597
- `16.29` Flex PIV processing … p.600
  - `16.29.1` Defining grid points … p.602
  - `16.29.2` Defining vector analysis … p.603
- `16.30` Histogram … p.603
  - `16.30.1` The Recipe dialog … p.604
- `16.31` Image Arithmetic … p.606
  - `16.31.1` Image arithmetic with another image … p.608
  - `16.31.2` Image arithmetic with a constant value … p.608
  - `16.31.3` Thresholding … p.608
- `16.32` Image Balancing … p.608
- `16.33` Image Dewarping … p.610
  - `16.33.1` Dewarping image maps … p.611
  - `16.33.2` Recipe dialog: Re sampling grid … p.614
  - `16.33.3` Recipe dialog: Z-coordinate … p.615
  - `16.33.4` Recipe dialog: Re-sampling scheme … p.616
  - `16.33.5` Recipe dialog: Fill color … p.616
- `16.34` Image Histogram … p.616
  - `16.34.1` Using ROI … p.616
  - `16.34.2` Manipulating the ROI rectangle using the mouse. … p.617
  - `16.34.3` Setting the ROI rectangle using the property dialog. … p.618
  - `16.34.5` Input Image types … p.618
  - `16.34.6` Using a Mask … p.618
- `16.35` Image Masking … p.619
- `16.36` Image & Volume Math … p.623
  - `16.36.1` Inputs … p.624
  - `16.36.2` Scalars … p.624
  - `16.36.3` Functions … p.625
  - `16.36.4` Operators … p.627
  - `16.36.5` Error description … p.627
  - `16.36.6` Output Selection … p.628
  - `16.36.7` Save intermediate result … p.628
  - `16.36.8` Example … p.628
  - `16.36.9` Advanced processing … p.630
- `16.37` Image Mean … p.630
  - `16.37.1` Application example … p.630
- `16.38` Image Min/Mean/Max … p.631
- `16.39` Image Processing Library (IPL) … p.635
  - `16.39.1` Low-pass filters … p.635
- `1` 1 1 /9 … p.637
- `1` 1 1 1 1 /25 … p.637
- `1` 1 1 1 1 1 1 /49 … p.637
- `1` 1 1 1 1 1 1 1 1 /81 … p.637
- `2` 4 2 /16 … p.638
- `1` 2 1 … p.638
- `7` 31 52 31 7 … p.639
- `12` 52 127 52 12 /571 … p.639
- `7` 31 52 31 7 … p.639
- `2` 7 12 7 2 … p.639
  - `16.39.2` High-pass filters … p.638
  - `16.39.3` Morphology filters … p.640
  - `16.39.4` Utility filters … p.643
- `1.4826` ⋅εcan be considered to have a S/N-Ratio of 1. For practical purposes you can multiply by … p.648
  - `16.39.5` Signal processing … p.649
  - `16.39.6` Custom filter … p.649
- `16.40` Image Re sampling … p.655
  - `16.40.1` Re-sampling window … p.655
  - `16.40.2` Re sampled maps … p.655
- `16.41` Image Resolution … p.658
- `16.42` Image RMS … p.659
  - `16.42.1` Direct Linear Transform (DLT) … p.659
  - `16.42.2` 3'rd order XYZ polynomial imaging model fit … p.660
  - `16.42.3` Pinhole camera model … p.662
  - `16.42.4` Telecentric camera model … p.665
- `16.43` Imaging Model Fit Import … p.668
- `16.44` RBF - Interpolation … p.669
  - `16.44.1` Usage … p.669
- `16.45` 3D Least Squares Matching … p.671
  - `16.45.1` Introduction … p.671
  - `16.45.2` The Least Squares Matching Recipe … p.672
  - `16.45.3` Results of the analysis … p.678
  - `16.45.4` References … p.678
- `16.46` LIF Calibration … p.678
  - `16.46.1` Custom properties of the calibration images … p.678
  - `16.46.2` Performing the calibration … p.681
- `16.47` LIF Processing … p.684
- `16.48` LII Calibration … p.688
- `16.49` LII Gas composition calibration … p.689
- `16.50` LII Processing … p.691
  - `16.50.1` LII data processing by Region-of-Interest <ROI> methodology … p.691
  - `16.50.2` LII data processing by Line-of-Sight (Lo S) methodology … p.693
- `16.51` Make Double Frame … p.694
- `16.52` Make Single Frame … p.695
- `16.53` Make Reverse Frame … p.695
- `16.54` MATLAB Link … p.696
  - `16.54.1` Contents … p.696
  - `16.54.2` Recipe for the MATLAB Link … p.696
  - `16.54.3` Selecting data for transfer to MATLAB … p.699
  - `16.54.4` DynamicStudio data in MATLAB's workspace … p.700
  - `16.54.5` Parameter String … p.703
  - `16.54.6` General … p.703
  - `16.54.7` The Output variable … p.704
- `16.55` Troubleshooting, Tips & Tricks … p.706
- `3.41` and older are 32-bit applications. They will run smoothly on a 64-bit platform, but be unable to … p.709
- `16.56` 1. Mie-LIF SMD - General … p.709
- `16.57` 2. SMD Calibration … p.710
- `16.58` 3. SMD Process … p.717
- `16.59` Modal Analysis (POD, s POD, m POD & FMD) … p.722
  - `16.59.1` Supported input … p.724
  - `16.59.2` Recipe & settings … p.724
  - `16.59.3` Modal Analysis recipe … p.725
  - `16.59.4` Handling the Mean … p.726
  - `16.59.5` Handling Outliers and Masked out data … p.727
  - `16.59.6` Time resolved Input … p.727
  - `16.59.7` Mode Count … p.727
  - `16.59.8` Multi-Scale POD (m POD) … p.728
- `0.0` and 0.5 in order to start over. Performing an m POD analysis with no cut off frequencies is equivalent to performing a Classic POD analysis. It is not possible to edit cut off frequencies already in … p.729
  - `16.59.9` Spectral POD (s POD) … p.729
  - `16.59.10` Fourier Mode Decomposition (FMD) … p.729
  - `16.59.11` Modal analysis … p.730
  - `16.59.12` Mode Normalization / Scaling … p.734
  - `16.59.13` X/Y Plots of data other than To pos … p.738
  - `16.59.14` Numerical display … p.747
  - `16.59.15` Input requirements … p.747
  - `16.59.16` Numeric Export of Modal results … p.748
  - `16.59.17` Troubleshooting, Tips & Tricks … p.752
- `16.60` Modal Filter … p.752
- `16.61` Modal Reconstruction / Projection … p.757
  - `16.61.1` Modal Reconstruction … p.758
  - `16.61.2` POD Projection … p.759
  - `16.61.3` Initiating Modal Reconstruction /Projection … p.759
- `16.62` Moving Average Validation … p.763
  - `16.62.1` Using the <Moving-average validation > method … p.763
- `16.63` Multi Camera Calibration … p.765
  - `16.63.1` Target Types & Parameters … p.768
  - `16.63.2` Dual level and dual sided targets … p.768
  - `16.63.3` Reference Point … p.769
  - `16.63.4` Automatic/Semi-automatic Calibration … p.769
  - `16.63.5` Active Target Calibration … p.770
  - `16.63.6` Manual Calibration … p.771
- `16.64` N-Sigma Validation … p.774
- `16.65` Octave Link … p.777
  - `16.65.1` Contents … p.777
  - `16.65.2` Installing Octave … p.777
  - `16.65.3` Recipe for the Octave Link … p.777
  - `16.65.4` Selecting data for transfer to Octave … p.781
  - `16.65.5` DynamicStudio data in Octave's workspace … p.781
  - `16.65.6` The Output variable … p.781
- `16.66` Oscillating Pattern Decomposition (OPD) … p.782
- `3.0` (valid signal may be hiding in such noise). … p.786
  - `16.66.1` Numeric Export of OPD results … p.788
  - `16.66.2` References … p.791
- `16.67` Peak Validation … p.792
  - `16.67.1` Interactive setting and finding good parameters … p.792
  - `16.67.2` Example using the peak validation for phase separation … p.792
- `16.68` Phase Boundary Detection … p.794
  - `16.68.1` A) Preview settings … p.794
  - `16.68.2` B) Global threshold … p.795
  - `16.68.3` C) Local threshold … p.795
  - `16.68.4` D) Filters … p.795
  - `16.68.5` E) Output … p.796
  - `16.68.6` F) Phase label … p.796
  - `16.68.7` Publications: … p.796
- `16.69` Dynamic Masking … p.797
- `16.70` PIV Uncertainty … p.797
  - `16.70.1` Rayleigh distribution … p.799
  - `16.70.2` Methodology … p.800
  - `16.70.3` Error messages … p.801
  - `16.70.4` Example … p.802
  - `16.70.5` Expanded uncertainties … p.806
- `16.71` Pressure from PIV … p.807
  - `16.71.1` Define Objects … p.807
  - `16.71.2` Pressure from PIV … p.810
  - `16.71.3` Solver … p.812
  - `16.71.4` Important considerations … p.814
- `16.72` Probability Distribution … p.815
  - `16.72.1` Define and apply a mask … p.815
  - `16.72.2` Distribution processing … p.815
  - `16.72.3` More about ROI data analysis … p.816
- `16.73` Profile plot … p.817
  - `16.73.1` Detailed description … p.818
  - `16.73.2` A handy shortcut … p.821
  - `16.73.3` Obtaining the numerical values … p.822
  - `16.73.4` Examples … p.822
- `16.74` Python Link … p.824
- `16.75` Range Validation … p.825
- `16.76` Rayleigh Thermometry … p.826
  - `16.76.1` Rayleigh Theory … p.827
  - `16.76.2` Rayleigh Thermometry Analysis in DynamicStudio … p.828
  - `16.76.3` Species and Mixture Library … p.836
- `16.77` Track Smoothing - Radial Basis Functions … p.837
  - `16.77.1` Mathematical background … p.837
  - `16.77.2` Usage … p.838
- `16.78` Rigid Object Tracking and Stabilization … p.839
  - `16.78.1` Introduction … p.839
  - `16.78.2` Rigid Object Tracking … p.839
  - `16.78.3` Rigid Object Stabilization … p.841
- `16.79` Region of Interest (ROI) Extract … p.842
  - `16.79.1` Manipulating the ROI rectangle using the mouse. … p.842
  - `16.79.2` Setting the ROI rectangle using the property dialog. … p.843
  - `16.79.3` Using the image view. … p.843
- `16.80` Scalar derivatives … p.844
  - `16.80.1` Calculating the gradients of U, V and W in the x and y direction … p.845
  - `16.80.2` Scalar derivatives that can be calculated … p.846
  - `16.80.3` Propagating uncertainties … p.848
- `16.81` Scalar Map … p.849
  - `16.81.1` Visualization methods… … p.850
- `16.82` Scalar statistics … p.852
- `16.83` Shadow Size Calibration … p.855
  - `16.83.1` Theory … p.856
  - `16.83.2` User Interface (UI) … p.860
  - `16.83.3` Calibration procedure … p.865
  - `16.83.4` Example in Demo Database … p.869
  - `16.83.5` References* … p.869
- `16.84` Shadow Combine … p.869
- `16.85` Shadow Statistics … p.869
  - `16.85.1` Basic theory of particle statistics from shadow imaging … p.870
  - `16.85.2` Shadow Statistics user interface (UI) … p.873
  - `16.85.3` Typical usage and application … p.874
- `16.86` Shadow Re sample … p.877
- `16.87` Shadow Spatial Histogram … p.878
  - `16.87.1` Calculation … p.879
  - `16.87.2` Number of cells … p.879
  - `16.87.3` Process … p.879
- `16.88` Shadow Tracking … p.879
  - `16.88.1` General description of the algorithm … p.879
  - `16.88.2` Dialog window (recipe) … p.880
  - `16.88.3` Data Visualization … p.883
- `16.89` Shadow Validation … p.883
- `16.90` Shadow correlation … p.883
- `16.91` Spectrum … p.886
  - `16.91.1` Example: Spectrum in the wake of a cylinder … p.886
- `16.92` Spray Geometry … p.891
  - `16.92.1` Introduction … p.891
  - `16.92.2` Setup window … p.892
  - `16.92.3` Spray nozzle properties … p.893
  - `16.92.4` Region of interest … p.895
  - `16.92.5` Cone Geometry - Plume geometry … p.895
  - `16.92.6` Spray Pattern … p.897
  - `16.92.7` Spray geometry processing - Temporal evolution … p.899
  - `16.92.8` Trouble shooting … p.904
- `16.93` Stereo-PIV … p.905
  - `16.93.1` Method and formulas … p.905
  - `16.93.2` Input Required … p.907
  - `16.93.3` Recipe for Stereo PIV processing … p.907
  - `16.93.4` Displaying results … p.908
- `16.94` Subpixel Analysis … p.910
- `16.95` Temporal Smoothing … p.912
  - `16.95.1` A) Smoothing settings … p.912
  - `16.95.2` B) Values to smooth … p.913
  - `16.95.3` C) Preview … p.913
- `16.96` Tomographic Particle Tracking Velocimetry … p.913
  - `16.96.1` Tomographic PTV … p.914
  - `16.96.2` Working principle: … p.922
- `16.97` Track Smoothing … p.923
  - `16.97.1` Inputs … p.923
  - `16.97.2` Out puts … p.924
  - `16.97.3` Settings and how to … p.925
- `16.98` Two-Color Pyrometry … p.925
  - `16.98.1` Introduction … p.925
  - `16.98.2` Overview of the procedure … p.925
  - `16.98.3` Spatial calibration … p.926
  - `16.98.4` Two-Color Pyrometry Calibration … p.926
  - `16.98.5` Two-Color Pyrometry Processing … p.931
- `16.99` Universal Out lier Detection … p.936
- `16.100` UV Scatter plot Range Validation … p.940
- `16.101` Vector Arithmetic … p.942
- `16.102` Vector Dewarping … p.944
  - `16.102.1` Setting the z-value and w-value … p.945
- `16.103` Vector Interpolation … p.946
- `16.104` Vector Masking … p.948
- `16.105` Vector Re sampling … p.953
  - `16.105.1` Automatic re-sampling … p.954
  - `16.105.2` User-defined re-sampling … p.955
  - `16.105.3` Edit data … p.956
- `16.106` Vector Statistics … p.957
  - `16.106.1` Visualization methods … p.960
  - `16.106.2` Numeric data display … p.960
  - `16.106.3` Formulas used … p.961
  - `16.106.4` Propagating uncertainties … p.962
- `16.107` Volume Grid … p.963
  - `16.107.1` Inputs … p.964
  - `16.107.2` Out puts … p.964
  - `16.107.3` Settings and how to … p.965
- `16.108` Volumetric calibration refinement … p.965
  - `16.108.1` Introduction: … p.965
  - `16.108.2` Theory of the Volumetric Calibration Refinement. … p.966
  - `16.108.3` The Static Volumetric Calibration Refinement in DynamicStudio … p.968
  - `16.108.4` Example of the VV calibration refinement … p.973
  - `16.108.5` The Temporal Volumetric Calibration Refinement in DynamicStudio … p.979
  - `16.108.6` Side effects of the Volumetric Calibration Refinement … p.979
- `16.109` Voxel Reconstruction … p.979
  - `16.109.1` Introduction … p.979
  - `16.109.2` The different reconstruction techniques in theory … p.980
- `2000` * 2000 * 1000 * 4 by tes = 16 GB for one time step. If you are dealing with double images, you … p.984
  - `16.109.3` The Voxel Reconstruction in DynamicStudio … p.984
- `16.110` Waveform Calculation … p.989
  - `16.110.1` Formulas … p.989
  - `16.110.2` Built-in Functions … p.990
  - `16.110.3` Built-in Operators … p.991
  - `16.110.4` Naming Conventions … p.992
  - `16.110.5` Syntax and Numerical Errors … p.992
  - `16.110.6` Examples … p.992
- `16.111` Waveform Extract … p.993
  - `16.111.1` Extracting Data … p.993
- `16.112` Waveform Statistics … p.994
  - `16.112.1` Statistical Values … p.994
  - `16.112.2` Example … p.995
- `16.113` Waveform Stitch … p.995
  - `16.113.1` Stitching Data … p.995
  - `16.113.2` Analog Stitching … p.997
- `16.114` Correlation option Window/Filter … p.997
  - `16.114.1` Window functions … p.997
  - `16.114.2` Filter functions … p.999

## 注意事项 / 警告

- Note: with the new release of DynamicStudio, the only calibration model available for this method is a Pinhole calibration model. Support for a 3rd order Model will be introduced at a later stage. For more information on the calibration model please and the Multi Camera Calibration please take a look to this section: "Multi Camera Calibration" on page 765
- Note: Although this denoising method performs remarkably good, the user must be warned that it takes a long time to compute (several seconds per image), adding a significant amount of computing time. The menu UI to enable the denoising method and the strength is shown below, together with a pair of images showing the performance of the algorithm.
- *Note: Ifa Shadow Size Calibration is applied with this method, then ideally the same threshold levels for the particle detections should be used. Filters& Tracking Filter Settings
- Note the saturated colors around the edge where displacements are largest, fading to shades of gray and eventually dark as we approach the center where there is almost no motion. For the 'Combined' display color-coding is fixed, but for the other four you can choose any of the color palettes provided with DynamicStudio.
- and so on. Note Targets in the library can be added see "Coordinate System" on page 83 4 - The calibration model to be used 5 - Search settings to search the target or to search in specific regions defined in 6 6 - Add specific target regions, if you have difficultiesproperly detecting the target markers
- front toa marker in the other level on the front. Note the minus on the level distance. This is because the center marker on the front is closer to the camera in this example and the z-axis is positivetowards the camera. Thus the markers on the front are placed in z = 3 mm and z= -1mm, while corresponding markers on the rear are placed in z = 1 mm and z = -3 mm. For single-sided targets, the lightsheet plane is placed in the middle between the two levels (equivalent to thickness being zero).
- Note: Overlaying refined calibration grids on calibration images will not align very well with calibration markers and cannot be expected to.Think ofitas an indication of where the calibration markers should have been if they had been aligned with the center of the lightsheet.
- returned in molecules/m3 (on frame_1) with the instantaneous errorlevels (on frame_2). Note that the error is relative to the global energy absorption; i.e.the map should be multiplied by Tr to obtain the relativeerror in % of[Nx] (See the application manual for the notation used.) Content:
- corners of this area. Note that if this area is larger than the light sheet height, the algorithm will automatically set 0-values in the outer parts of the illuminati on. 4. Select the combustion radical imaged (This will set values to several constants such as the emission line) and complete the absorption cross-section box with the dimension x10-20 cm-2.
- Note: With the version 1.00 of the Combustion-LIF software, only OH is available. The option 'User-defined' is enabled but a couple of spectroscopic constants will not be set properly. Although energy profile correction, energy budget, etc will be implemented the absolute values will not be correct.
- Note that displacements are typically quite small so vectors are usually scaled up. The midpoint of the vectors are anchored at the surface itself.Using fixed limits can be useful e.g. when monitoring how things change over time. The translation and rotation parameters in the righthand side can be used to move and rotate the
- Note: Dewarp using Polynomial IMF's l Recipe dialog: Re-sampling scheme l Recipe dialog: Fillcolor outside image l Recipe dialog: Z-coordinate

## 关联章节

- ch13 数据采集 · ch14 设备 · ch16 分析模块 · ch18 显示