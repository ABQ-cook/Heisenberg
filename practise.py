from pathlib import Path
import json
import csv

class Project_Manager:

    def __init__(self, project_root: str) -> None:
        self.root: Path = Path(project_root)
        self.root.mkdir(parents = True, exist_ok = True)

    @property
    def config_path(self) -> Path:
        return self.root / 'config.json'

    @property
    def data_path(self) -> Path:
        return self.root / 'data.csv'

    def config_init(self, config: dict[str, str]) -> None:
        _ = self.config_path.write_text(data = json.dumps(config, ensure_ascii = False, indent = 4), encoding = 'utf-8')
        print(f'配置已写入[{self.config_path}]')

    def save_data(self, data: list[dict[str, str]], fieldnames: list[str]) -> None:
        with open(self.data_path, 'w', newline = '', encoding = 'utf-8') as f:
            writer = csv.DictWriter(f, fieldnames = fieldnames)
            writer.writeheader()
            writer.writerows(data)
            print(f'数据已写入[{self.data_path}]')

    def list_flies(self) -> None:
        print(f'项目文件：{self.root}')
        for f in sorted(self.root.rglob('*')):
            if f.is_file():
                size = f.stat().st_size
                print(f'{f.relative_to(self.root)}({size}bytes)')


def main():
    pm = Project_Manager('./testproject')
    pm.config_init({'myname':'yanyunxiang', 'age': '20', 'myproject': 'test'})
    pm.save_data(
        data = [{'number': '1', 'name': 'yan', 'age': '20'},
        {'number': '1', 'name': 'yan', 'age': '20'},
        {'number': '1', 'name': 'yan', 'age': '20'}],
        fieldnames = ['number', 'name', 'age']
    )

if __name__ == '__main__':
    main()
    
