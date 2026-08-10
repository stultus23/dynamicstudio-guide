#!/usr/bin/env python3
"""
DynamicStudio Skill 搜索工具
支持在 raw 目录和章节文件中搜索关键词
"""

import os
import re
import sys
from pathlib import Path

# Force UTF-8 stdout on Windows
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

class DynamicStudioSearch:
    def __init__(self, skill_dir):
        self.skill_dir = Path(skill_dir)
        self.raw_dir = self.skill_dir / "raw"
        self.chapters_dir = self.skill_dir / "chapters"
        self.procedures_file = self.skill_dir / "procedures.md"
        self.dialogs_file = self.skill_dir / "dialogs.md"
        
    def search_keyword(self, keyword, context_lines=3):
        """搜索关键词，返回结果和上下文"""
        results = []
        keyword_lower = keyword.lower()
        
        # 搜索 raw 目录
        for txt_file in sorted(self.raw_dir.glob("ch*.txt")):
            chapter_num = txt_file.stem.replace("ch", "")
            lines = txt_file.read_text(encoding='utf-8').splitlines()
            
            for i, line in enumerate(lines):
                if keyword_lower in line.lower():
                    # 获取上下文
                    start = max(0, i - context_lines)
                    end = min(len(lines), i + context_lines + 1)
                    context = lines[start:end]
                    
                    # 查找页码
                    page_num = None
                    for j in range(i, -1, -1):
                        if lines[j].startswith("PAGE|"):
                            page_num = lines[j].replace("PAGE|", "")
                            break
                    
                    results.append({
                        'source': f'raw/ch{chapter_num}.txt',
                        'line': i + 1,
                        'page': page_num,
                        'content': line.strip(),
                        'context': context
                    })
        
        # 搜索 procedures.md
        if self.procedures_file.exists():
            lines = self.procedures_file.read_text(encoding='utf-8').splitlines()
            for i, line in enumerate(lines):
                if keyword_lower in line.lower():
                    results.append({
                        'source': 'procedures.md',
                        'line': i + 1,
                        'page': None,
                        'content': line.strip(),
                        'context': lines[max(0, i-1):i+2]
                    })
        
        # 搜索 dialogs.md
        if self.dialogs_file.exists():
            lines = self.dialogs_file.read_text(encoding='utf-8').splitlines()
            for i, line in enumerate(lines):
                if keyword_lower in line.lower():
                    results.append({
                        'source': 'dialogs.md',
                        'line': i + 1,
                        'page': None,
                        'content': line.strip(),
                        'context': lines[max(0, i-1):i+2]
                    })
        
        return results
    
    def search_page(self, page_num):
        """搜索指定页码的内容"""
        results = []
        
        for txt_file in sorted(self.raw_dir.glob("ch*.txt")):
            chapter_num = txt_file.stem.replace("ch", "")
            content = txt_file.read_text(encoding='utf-8')
            
            # 查找 PAGE|N 标记
            pattern = f"PAGE|{page_num}"
            if pattern in content:
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    if line.strip() == pattern:
                        # 获取该页内容（到下一页标记）
                        page_content = []
                        for j in range(i + 1, len(lines)):
                            if lines[j].startswith("PAGE|"):
                                break
                            page_content.append(lines[j])
                        
                        results.append({
                            'source': f'raw/ch{chapter_num}.txt',
                            'page': page_num,
                            'content': '\n'.join(page_content[:50])  # 前50行
                        })
        
        return results
    
    def search_chapter(self, chapter_num):
        """获取指定章节的信息"""
        chapter_file = self.chapters_dir / f"ch{chapter_num:02d}-*.md"
        raw_file = self.raw_dir / f"ch{chapter_num:02d}.txt"
        
        result = {
            'chapter': chapter_num,
            'chapter_file': None,
            'raw_file': None,
            'stats': {}
        }
        
        # 查找章节文件
        chapter_files = list(self.chapters_dir.glob(f"ch{chapter_num:02d}-*.md"))
        if chapter_files:
            result['chapter_file'] = str(chapter_files[0])
        
        # 查找 raw 文件
        if raw_file.exists():
            result['raw_file'] = str(raw_file)
            content = raw_file.read_text(encoding='utf-8')
            lines = content.splitlines()
            result['stats'] = {
                'total_lines': len(lines),
                'page_count': sum(1 for l in lines if l.startswith("PAGE|")),
                'file_size': raw_file.stat().st_size
            }
        
        return result

def main():
    """主函数"""
    skill_dir = r"C:\Users\wsh\.config\opencode\skills\dynamicstudio-guide"
    search = DynamicStudioSearch(skill_dir)
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python search_tool.py <关键词>      # 搜索关键词")
        print("  python search_tool.py -p <页码>      # 搜索页码")
        print("  python search_tool.py -c <章节号>    # 查看章节信息")
        print("  python search_tool.py --test         # 运行测试")
        return
    
    if sys.argv[1] == "--test":
        # 运行测试
        print("=" * 60)
        print("DynamicStudio Skill 搜索工具测试")
        print("=" * 60)
        
        # 测试1：搜索 PIV
        print("\n1. 搜索 'PIV'：")
        print("-" * 40)
        results = search.search_keyword("PIV")
        print(f"  找到 {len(results)} 个结果")
        for r in results[:3]:
            content = r['content'][:60].encode('utf-8', errors='replace').decode('utf-8')
            print(f"  [{r['source']}] Line {r['line']}: {content}...")
        
        # 测试2：搜索页码
        print("\n2. 搜索页码 130：")
        print("-" * 40)
        results = search.search_page(130)
        print(f"  找到 {len(results)} 个结果")
        for r in results:
            content = r['content'][:80].encode('utf-8', errors='replace').decode('utf-8')
            print(f"  [{r['source']}] {content}...")
        
        # 测试3：查看章节信息
        print("\n3. 章节 13 信息：")
        print("-" * 40)
        info = search.search_chapter(13)
        print(f"  章节文件: {info['chapter_file']}")
        print(f"  Raw 文件: {info['raw_file']}")
        print(f"  统计: {info['stats']}")
        
        print("\n" + "=" * 60)
        print("测试完成！")
        print("=" * 60)
    
    elif sys.argv[1] == "-p" and len(sys.argv) > 2:
        # 搜索页码
        page_num = int(sys.argv[2])
        results = search.search_page(page_num)
        
        print(f"\n搜索页码 {page_num}：")
        print("=" * 60)
        print(f"找到 {len(results)} 个结果")
        
        for r in results:
            content = r['content'][:500].encode('utf-8', errors='replace').decode('utf-8')
            print(f"\n[{r['source']}]")
            print("-" * 40)
            print(content)
    
    elif sys.argv[1] == "-c" and len(sys.argv) > 2:
        # 查看章节信息
        chapter_num = int(sys.argv[2])
        info = search.search_chapter(chapter_num)
        
        print(f"\n章节 {chapter_num} 信息：")
        print("=" * 60)
        print(f"章节文件: {info['chapter_file']}")
        print(f"Raw 文件: {info['raw_file']}")
        print(f"统计: {info['stats']}")
    
    else:
        # 搜索关键词
        keyword = sys.argv[1]
        results = search.search_keyword(keyword)
        
        print(f"\n搜索 '{keyword}'：")
        print("=" * 60)
        print(f"找到 {len(results)} 个结果")
        
        for i, r in enumerate(results[:10]):
            content = r['content'][:100].encode('utf-8', errors='replace').decode('utf-8')
            print(f"\n{i+1}. [{r['source']}] Line {r['line']}")
            if r['page']:
                print(f"   页码: {r['page']}")
            print(f"   内容: {content}...")

if __name__ == "__main__":
    main()
