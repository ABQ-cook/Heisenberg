from pathlib import Path
import shutil
from collections import defaultdict


def classify_files(source_dir, dry_run = True):
    '''按扩展名将source_dir下的文件进行分类，分类到子目录
    source_dir: 要整理的目录路径
    dry_run: True表示预览，False表示实际执行
    '''
    source: Path = Path(source_dir)
    if not source.is_dir():
        print(f'目录[{source_dir}]不存在')
        return

    # 扫描文件并进行分类
    filegroups = defaultdict(list)
    for f in source.iterdir():
        if f.is_file():
            ext: str = f.suffix.lower().lstrip('.')
            if ext == '':
                ext = '没有扩展名'
            filegroups[ext].append(f)
    
    if not filegroups:
        print('没有文件需要分类')
        return

    # 移动文件
    total: int = 0
    for ext, files in sorted(filegroups.items()):
        target_dir= source / ext
        print(f'\n[{ext}]: {len(files)}个文件')

        # 创建目标目录
        if not dry_run:
            target_dir.mkdir(exist_ok = True)
        
        for f in files:
            print(f"{'[预览]' if dry_run else '->'}{f.name}")
            if not dry_run:
                shutil.move(str(f), str(target_dir/f.name))
        total += len(files)

    if dry_run:
        print(f'\n[预览模式]共{total}个文件，实际未被移动，若想进行实际移动整理，请添加--no-dry-run参数执行')
    else:
        print(f'\n分类完成！总共{total}个文件->{source_dir}')



if __name__ == '__main__':
    import sys

    dry_run = '--no-dry-run' not in sys.argv
    source = sys.argv[1] if len(sys.argv) > 1 else '.'
    classify_files(source, dry_run)


