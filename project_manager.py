import csv
from pathlib import Path
import json

class ProjectManager:
    '''项目配置管理器：Json存配置、CSV存数据、pathlib存路径'''
    def __init__(self, project_root: str) -> None:
        self.root: Path = Path(project_root)
        self.root.mkdir(parents = True, exist_ok = True)  # parents = True 表示如果父目录不存在，则创建父目录（递归创建多层） exist_ok = True 表示如果目录已存在，则不抛出异常
    
    @property
    def config_path(self) -> Path:
        '''配置路径'''
        return self.root / 'config.json'
    
    @property  # 将某方法变成只读属性
    def data_path(self) -> Path:
        '''数据路径'''
        return self.root / 'data.csv'

    def init_project(self, config: dict[str, object]) -> None:
        '''写入配置文件'''
        _ = self.config_path.write_text(data=json.dumps(obj=config, ensure_ascii = False, indent = 4),encoding = 'utf-8')
        print(f'配置已写入{self.config_path}')

    def save_project(self, data: list[dict[str, str]], fieldnames: list[str]):
        '''写入数据文件'''
        with open(self.data_path, 'w', newline = '', encoding = 'utf-8') as f:
            writer = csv.DictWriter(f, fieldnames = fieldnames)
            writer.writeheader()
            writer.writerows(data) 
        print(f'数据已写入{self.data_path}')

    def list_files(self):
        print(f'项目:{self.root}')
        for f in sorted(self.root.rglob('*')):
            if f.is_file():
                size = f.stat().st_size
                print(f'{f.relative_to(self.root)}({size}bytes)')

pm = ProjectManager("./my_project")
pm.init_project({"app_name": "MyApp", "version": "1.0", "debug": False})

pm.save_project(
    data=[{"id": "1", "title": "学习JSON", "status": "done"},
     {"id": "2", "title": "学习CSV",  "status": "doing"},
     {"id": "3", "title": "学习pathlib", "status": "todo"}],
    fieldnames=["id", "title", "status"]
)

pm.list_files()

