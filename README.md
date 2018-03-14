# PyQCLab

# PyQCLab实验控制测量软件架构
> 主要开发者：金怡荣，王战
## 简介
PyQCLab是针对超导量子计算实验研究开发的简单仪器控制与测量、数据处理和可视化相关的应用程序。目前主要开发语言是Python，不排除今后引入其他开发语言进行优化。

## 运行环境与安装

### PyQCLab是与平台无关的可移植开源软件。
依赖的运行环境和库如下：
- Python 3.5+
- Numpy and Scipy
- matplotlib
- pyvisa
- guidata, guiqwt
- scikit-rf
- h5py
- ...

### 安装：
推荐使用[Anaconda](https://www.anaconda.com/download/)集成python科学运算库. Anaconda集成了几乎最常见的Python开发环境和科学运算库，包括numpy, scipy, matplotlib, ipython, notebook, spyder等等，并且提供良好的包管理（conda）系统。

以下以Anaconda安装为例，介绍在windows下安装运行环境：
1. 下载Anaconda for Windows；注意选择 ==Python 3 Version==
2. 运行安装文件，所有的步骤采用推荐设置即可；
3. 安装完成之后，运行"Anaconda prompt"，系统将弹出一个终端
4. 安装必要的库：

```
> conda install scikit-rf
> pip install pyvisa
> pip install guidata
> pip install guiqwt
```
> 注意：guiqwt是pythonqwt的封装，而pythonqwt是Qt绘图库qwt的封装，qwt绘图库安装需要编译，会调用C++编译器，如果系统中没有C++编译器，则会出现安装错误。从Windows官网上下载Visual C++ Tools，安装即可，版本要求14.0以上。

### 文件组织
PyQCLab 
```
graph TD
PyQCLab-->Instrument
PyQCLab-->APPs
PyQCLab-->Utils
PyQCLab-->UIs
PyQCLab-->Documents


```
- Instrument: 包含各仪器设备驱动的python封装；
- Apps：用于实际进行控制和测量的脚本或可执行文件；
- Utils: 数据处理和生成相关的模块；
- UIs：界面相关的模块；
- Documents：仪器设备、各python库的相关文档；

    


