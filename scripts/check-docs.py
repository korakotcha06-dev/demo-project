#!/usr/bin/env python3
"""ตรวจความสมบูรณ์ของเอกสารใน vault นี้ — รันก่อน push

🔴 ทำไมต้องมี (Touch สั่ง 2026-08-23):
   vault นี้มีกฎสองข้อที่ **เขียนไว้แล้วแต่ไม่มีใครบังคับ** จึงพังเงียบ ๆ ได้ตลอด

   1. CLAUDE.md: *"ห้ามทำลิงก์เหล่านี้ขาด และต้องอัปเดตทุกครั้งที่เพิ่มหรือย้ายเอกสาร"*
      — wikilink ที่ชี้ไปไฟล์ที่ไม่มีอยู่ **ไม่ใช่ error ของใครเลย** Obsidian แค่แสดง
      เป็นลิงก์สีจาง คนเขียนไม่รู้ตัว คนอ่านกดแล้วเจอทางตัน

   2. decision log 2026-08-23: การแยก vault ออกจากรีโปโค้ดทำให้ต้องพิมพ์
      `qr-order-app@<sha>` ต่อท้ายทุกบันทึกด้วยมือ — **20 จุดและเพิ่มขึ้นเรื่อย ๆ**
      วันที่พิมพ์ผิดหรือ rebase แล้ว sha เปลี่ยน จะไม่มีใครรู้จนกว่าจะมีคนไล่ตาม

🔴 หา path ของรีโปโค้ดจาก **CLAUDE.md เอง** ไม่ใช่ hardcode ไว้ในสคริปต์ —
   เอกสารเป็นแหล่งความจริงอยู่แล้ว การเก็บ path ไว้สองที่คือการเปิดช่องให้มันไม่ตรงกัน
   (ทับได้ด้วย env `QR_APP_REPO` เวลาต้องชี้ไปที่อื่นชั่วคราว)

ใช้: python3 scripts/check-docs.py   ·   ออกด้วยรหัสไม่ใช่ 0 ถ้าเจอปัญหา
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')


def all_markdown():
    for base, _dirs, files in os.walk(DOCS):
        for f in files:
            if f.endswith('.md'):
                yield os.path.join(base, f)


def check_wikilinks():
    """[[path|label]] ทุกอันต้องชี้ไปไฟล์ที่มีอยู่จริง"""
    broken = []
    for path in sorted(all_markdown()):
        base = os.path.dirname(path)
        text = open(path, encoding='utf-8').read()
        for m in re.finditer(r'\[\[([^\]\|]+)(?:\|[^\]]*)?\]\]', text):
            target = m.group(1).strip().rstrip('\\')
            if target.startswith('#'):
                continue                      # ลิงก์ไปหัวข้อในไฟล์เดียวกัน
            target = target.split('#')[0].strip()
            if not target:
                continue
            resolved = os.path.normpath(os.path.join(base, target))
            if not (os.path.exists(resolved) or os.path.exists(resolved + '.md')):
                broken.append((os.path.relpath(path, ROOT), m.group(1)))
    return broken


def code_repo():
    """path ของรีโปโค้ด — env ก่อน แล้วค่อยอ่านจาก CLAUDE.md"""
    env = os.environ.get('QR_APP_REPO')
    if env:
        return env
    claude_md = os.path.join(ROOT, 'CLAUDE.md')
    if not os.path.exists(claude_md):
        return None
    m = re.search(r'local:\s*`([^`]+)`', open(claude_md, encoding='utf-8').read())
    return m.group(1) if m else None


def check_code_refs():
    """ทุก qr-order-app@<sha> ต้องเป็น commit ที่มีอยู่จริงในรีโปโค้ด"""
    repo = code_repo()
    shas = set()
    for path in all_markdown():
        text = open(path, encoding='utf-8').read()
        for m in re.finditer(r'qr-order-app@([0-9a-f]{7,40})', text):
            shas.add(m.group(1))

    if not shas:
        return [], 0, repo
    # ไม่มีรีโปโค้ดในเครื่อง = ข้าม ไม่ใช่ fail — คนที่ clone แค่ vault ต้องรันได้
    if not repo or not os.path.isdir(os.path.join(repo, '.git')):
        return None, len(shas), repo

    dead = []
    for sha in sorted(shas):
        ok = subprocess.run(
            ['git', '-C', repo, 'cat-file', '-e', f'{sha}^{{commit}}'],
            capture_output=True,
        ).returncode == 0
        if not ok:
            dead.append(sha)
    return dead, len(shas), repo


def main():
    failed = False

    broken = check_wikilinks()
    total_md = len(list(all_markdown()))
    if broken:
        failed = True
        print(f'🔴 wikilink ขาด {len(broken)} จุด:')
        for f, link in broken:
            print(f'   {f} → [[{link}]]')
    else:
        print(f'✓ wikilink ครบทุกจุด ({total_md} ไฟล์)')

    dead, count, repo = check_code_refs()
    if dead is None:
        print(f'⚠ ข้ามการตรวจ qr-order-app@sha ({count} จุด) — ไม่พบรีโปโค้ดที่ {repo}')
    elif dead:
        failed = True
        print(f'🔴 qr-order-app@sha ชี้ไป commit ที่ไม่มีอยู่จริง {len(dead)} จุด:')
        for sha in dead:
            print(f'   {sha}')
    else:
        print(f'✓ qr-order-app@sha ชี้ถูกทุกจุด ({count} จุด)')

    if failed:
        print('\nแก้ให้ครบก่อน push')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
