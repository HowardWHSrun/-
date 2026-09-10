# 源文件与设计过程存档

当前可直接使用的完整交付在仓库 `docs/`；本目录保留建模、渲染、报告、离线漫游、原图提取与几何核对的作者源文件。

- `home-design/blender/`：当前第6户模型数据、家具花园生成器、Blender导出、相机、Three.js漫游引擎、模板与测试。
- `home-design/build_professional_report.py`：A3 PDF、DXF与CSV生成器。
- `home-design/output/unit6-professional/`：报告输入和P02核对脚本。
- `home-design/tmp/cad-recovery/`：仅归档原图提取脚本；没有缓存、运行库或临时CAD输出。
- `history/`：历史调查、更正与前版说明，用于追溯；其中旧参数不应覆盖当前P02报告。

## 复建说明

这些脚本保存实际工作版本，尚不是跨平台一键构建工具。建模使用Blender4.5与Python；报告使用ReportLab、Pillow、Shapely、ezdxf等和macOS宋体字体。部分脚本引用本机运行库路径，离线打包器引用已安装的可视化导出助手；接手开发者需按自己的环境替换路径、配置依赖并准备原图解析副本。原图在 `docs/原图依据/`；当前报告与模型输入亦可从 `docs/核对记录/`、`docs/模型/`获得。

在线网站无需执行这些脚本。发布目录的HTML、PDF、图片和文件已经全部生成；离线漫游无需联网和额外安装。

## 当前版本

最终场景SHA256：`e9501fa42af81245b9acfdc1a1fd88f5f7d8ad7b7d4ec4ca1fda0ca6af334a2b`。

原图证据、新增方案和竖向展示假设的边界以P02报告为准；历史文件仅作追溯。第三方Three.js沿用附带MIT许可；原图及其余项目资料未在此重新授权。
