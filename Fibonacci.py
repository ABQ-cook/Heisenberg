import shutil
from pathlib import Path
from collections import defaultdict


def classify_files(source_dir, dry_run=True):
    """
    按扩展名将文件分类到子目录

    参数:
        source_dir: 要整理的目录路径
        dry_run: True 则只预览不实际移动
    """
    source: Path = Path(source_dir)
    if not source.is_dir():
        print(f"❌ 目录不存在:{source_dir}")
        return

    # 扫描文件并分类
    file_groups = defaultdict(list)
    for f in source.iterdir():
        if f.is_file():
            ext: str = f.suffix.lower().lstrip(".")
            if ext == "":
                ext = "no_extension"
            file_groups[ext].append(f)

    if not file_groups:
        print("没有文件需要分类")
        return

    # 移动文件
    total = 0
    for ext, files in sorted(file_groups.items()):
        target_dir = source / ext
        print(f"\n📁 [{ext}]{len(files)} 个文件")

        # 创建目标目录
        if not dry_run:
            target_dir.mkdir(exist_ok=True)

        for f in files:
            print(f"{'[预览]' if dry_run else '→'}{f.name}")
            if not dry_run:
                shutil.move(str(f), str(target_dir / f.name))
        total += len(files)

    if dry_run:
        print(f"\n⚠️  [预览模式] 共{total} 个文件，实际未被移动。请添加 --no-dry-run 参数执行。")
    else:
        print(f"\n✅ 分类完成！共{total} 个文件 →{source_dir}")


if __name__ == "__main__":
    import sys

    # 简单参数解析（学习计划后续会用 argparse 升级）
    dry_run = "--no-dry-run" not in sys.argv
    source = sys.argv[1] if len(sys.argv) > 1 else "."     # 三元表达式：X if 条件 else Y

    print(f"📂 源目录:{source}")
    classify_files(source, dry_run=dry_run)