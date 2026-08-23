---
name: test-design
description: Turn requirements (user stories, AC, NFR, UX, API/DB design) into a testable acceptance-criteria audit, a test case specification, a test plan, a traceability matrix and UAT scenarios for this coffee-shop QR self-order project — written straight into docs/03-testing/01-test-plan. Trigger on /test-design, and proactively whenever the user asks for a test plan, test cases, "เขียนเคสทดสอบ", "AC นี้ทดสอบยังไง", a traceability matrix, or asks whether a requirement can be verified at all.
---

# Test Design (Requirement → AC audit → Test Case → Test Plan)

แปลง requirement ที่มีอยู่แล้วใน `docs/01-requirements` + `docs/02-design` ให้เป็นชุดเอกสารทดสอบที่ **หยิบไปรันได้จริงโดยไม่ต้องถามใครเพิ่ม**

**เจ้าของงาน:** OKOYE · **ห้ามใช้กับการบันทึกผลจริง** — นั่นคือ `/test-run`

## When to use
- มี requirement/design ใหม่ หรือมีการเปลี่ยนคำตัดสินที่ทำให้เคสเดิมล้าสมัย
- ต้องตอบว่า requirement ตัวหนึ่ง **ทดสอบได้หรือไม่** ก่อนจะรับเข้าสโคป
- ต้องรู้ว่า coverage ของ Phase ปัจจุบันเหลือช่องว่างตรงไหน

## อ่านอะไรก่อน (ต้นทางบังคับ)

| ชั้น | ไฟล์ | เอาอะไรจากมัน |
|---|---|---|
| requirement | `01-spec/product-backlog-v1.md` | US + AC + BR |
| requirement | `01-spec/acceptance-criteria-v1.md` | ทะเบียน AC-xx ที่มี ID ถาวร |
| requirement | `01-spec/nfr-v1.md` | เกณฑ์ตัวเลขที่ต้องใช้ซ้ำ ห้ามตั้งใหม่ |
| requirement | `01-spec/ux-requirements-v1.md` | UX-xx + error/empty state |
| requirement | `01-spec/initial-menu-data-v1.md` | test data จริง |
| plan | `02-plan/release-roadmap-v1.md` | Phase ไหนอยู่ในสโคป |
| design | `02-technical/api-design-v1.md` §5, §7 | race condition + error contract |
| design | `02-technical/data-model-v1.md` §5 | DB invariant |
| audit | `01-spec/traceability-audit-v1.md` | GAP ที่ยังเปิดอยู่ |

**ถ้าไฟล์ต้นทางขัดกันเอง ให้หยุดและรายงาน ห้ามเลือกข้างเงียบ ๆ**

---

## Workflow

### 1. ล็อกสโคปก่อน
เขียนให้ชัดว่า Phase ไหน · US/NFR/UX กี่ตัว · **และอะไรอยู่นอกสโคปพร้อมเหตุผล**
กติกาประจำโปรเจกต์: **ไม่เขียนเคสให้ของที่ยังไม่มี design** — การเขียนเคสให้ของที่ยังไม่ออกแบบคือการเดาว่ามันจะทำงานอย่างไร

### 2. AC Testability Audit — ขั้นที่ห้ามข้าม
ไล่ทุก AC ในสโคป ตัดสินทีละข้อว่า **PASS / ต้องแก้** ด้วยคำถามเดียว:
> *"คนสองคนอ่าน AC ข้อนี้ แล้ววัดผลได้ตรงกันไหม"*

| ธงแดง | ต้องขออะไรแทน |
|---|---|
| "ทันที" · "รวดเร็ว" · "ไม่กี่คลิก" · "ใช้งานง่าย" | ตัวเลขวินาที / จำนวน tap / success rate |
| **"และ/หรือ"** | เลือกว่าอันไหนบังคับ — ไม่งั้นระบบที่ทำครึ่งเดียวก็ผ่านตามตัวอักษร |
| "ใช้งานได้ดีบนมือถือ" | ผูกกับ NFR/UX ที่มีตัวเลขอยู่แล้ว |
| "ระบบต้องกัน X" | ระบุชั้น: UI หรือ DB — กฎธุรกิจต้องบังคับที่ DB |
| เกณฑ์ที่วัดจริงแล้วทำซ้ำไม่ได้ (เช่น "ได้ยินจาก 3 เมตรในร้านที่เปิดเพลง") | ตัดทิ้งและแทนด้วยเกณฑ์ที่ทำซ้ำได้ |

**ผลลัพธ์ของขั้นนี้:**
- AC ที่ผ่าน → ไปข้อ 3
- AC ที่ไม่ผ่าน → เขียนเป็น **ข้อเสนอแก้ AC** (AC เดิม / ทำไมวัดไม่ได้ / เกณฑ์ที่เสนอ / ใครต้องเคาะ) แล้วส่งคืน XAVIER
  🔴 **ห้ามแก้ไฟล์ backlog เอง และห้ามเขียนเคสให้ AC ที่ยังไม่ถูกเคาะ**

**ใช้เกณฑ์ที่มีอยู่แล้วก่อนเสมอ** — ถ้า NFR-03 กำหนด ≤5 วินาทีอยู่แล้ว อย่าตั้งเลขใหม่

### 3. เขียน Test Case
ลง `01-test-plan/test-case-v1.md` · จัดเป็น suite (S1, S2, …) ตามผู้ใช้/ประเภท

```
| TC | Req ID | Precondition | ขั้นตอน | ผลที่คาดหวัง (วัดผลได้) | ประเภท | Pri |
```

- **ประเภท:** `F` functional · `N` NFR · `E` error-path · `C` concurrency · `I` DB invariant · `U` usability
- **Pri:** `P0` fail = เปิดร้านไม่ได้ · `P1` เจ็บแต่เปิดได้ · `P2` ปรับปรุง
- เลข TC **ถาวร** — แตกเคสให้ใช้ suffix (`TC-015a`) ห้ามเลื่อนเลขเดิม
- ช่อง "ผลที่คาดหวัง" ต้องเป็นสิ่งที่ **วัดหรือนับได้** — "ทำงานถูกต้อง" ไม่ผ่านเกณฑ์นี้

**กติกาเฉพาะประเภท:**
- `I` (invariant) → **ยิง SQL/API ตรงเพื่อพยายามทำผิดกฎ** ห้ามทดสอบผ่าน UI
- `C` (concurrency) → **≥2 เครื่องกดพร้อมกันจริง** และทำซ้ำ ≥3 รอบ
- `U` (usability) → ระบุจำนวนผู้ทดสอบขั้นต่ำ ถ้าหาคนไม่ครบ ผลเป็น indicative ไม่ใช่ pass
- `E` (error-path) → ต้องตรวจทั้ง HTTP code **และ** ข้อความที่ผู้ใช้เห็น + ต้องมีทางออกเสมอ

### 4. Test Data
ลง `01-test-plan/test-data-v1.md` — ชุด `D-x` พร้อมเหตุผลว่า **ทำไมค่าต้องเป๊ะ** และเช็กลิสต์ตรวจรับก่อนเริ่ม
ถ้า seed ผิด เคสบางตัวจะ **pass แบบผิด ๆ** ซึ่งอันตรายกว่า fail

### 5. Traceability Matrix
ลง `01-test-plan/traceability-matrix-v1.md` — หนึ่งแถวต่อหนึ่ง requirement:
`FR/NFR/UX/BR/INV → US → AC → TC → สถานะรัน → ผล`
requirement ที่ไม่มี TC ต้องมีเหตุผลในแถวนั้น ไม่ปล่อยว่าง

### 6. Test Plan
ลง `01-test-plan/test-plan-v1.md` — **กลยุทธ์เท่านั้น ไม่มีตารางเคส**: ขอบเขต in/out · สภาพแวดล้อมและอุปกรณ์ที่ต้องมีจริง · ลำดับการลงมือ · สิ่งที่ถูกบล็อก · **เกณฑ์ผ่าน-ไม่ผ่านของ Phase**

ลำดับการลงมือ **เรียงตามความเสียหายและต้นทุนของการรู้ช้า** ไม่ใช่เลข ID:
1. เงินต้องไม่ผิด (กู้คืนไม่ได้)
2. กฎที่รั่วแล้วของออกจากร้านฟรี
3. architecture ที่แก้ทีหลังแพงมาก (auth/schema)
4. happy path
5. …ที่เหลือ

### 7. UAT Scenario
ลง `01-test-plan/uat-scenario-v1.md` — สคริปต์ที่ **เจ้าของร้านทำเองได้** เป็นเรื่องเล่าต่อเนื่อง ไม่ใช่เคสรายข้อ ภาษาไม่มีศัพท์เทคนิค

### 8. ปิดงาน
- อัปเดต `01-test-plan/index.md` (wikilink + ตัวเลขสรุป + สถานะ)
- ลง `docs/05-log/changelog.md`
- ถ้ามีข้อเสนอแก้ AC ค้าง → ยกขึ้นเป็น NEED-INPUT ถึง XAVIER/Touch

---

## กฎเหล็ก

1. **ห้ามเขียนเคสให้ AC ที่วัดผลไม่ได้ เพื่อให้ coverage ดูสวย** — ประกาศตรง ๆ ว่าเขียนไม่ได้ พร้อมเหตุผล
2. **ห้ามแตะ `02-test-result`** — เอกสารชุดนี้บอกว่าจะทดสอบอะไร ไม่ใช่ผลอะไร
3. **ห้ามแก้ AC ในไฟล์ `01-spec` เอง** — เสนอ ไม่ใช่แก้
4. **เคสที่รันไม่ได้ต้องเขียนไว้ พร้อมเงื่อนไขปลดล็อกและเจ้าของ** ไม่ใช่ตัดทิ้งให้ตัวเลขสวย
5. **ตัวเลขสรุปต้องนับจากตารางจริง** ห้ามประมาณ — ถ้านับได้ 121 ห้ามเขียน 113

## Output

จบด้วย:
```
ส่งงาน — OKOYE → ทัช (งาน / ผลลัพธ์ / ค้าง-เสี่ยง / skill ที่ใช้)
```
พร้อมตัวเลข: เขียนได้กี่เคส · รันได้ทันทีกี่เคส · บล็อกกี่เคสและติดใคร · requirement ที่ยังเขียนเคสไม่ได้กี่ตัว
