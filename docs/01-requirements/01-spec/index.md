# 01 - Spec

เก็บเอกสาร **ข้อกำหนดของโปรเจกต์ (Requirements / Specification)** เช่น

- Feature requirements — ฟีเจอร์ที่ต้องมีในระบบ
- User stories / use cases
- Business rules และเงื่อนไขทางธุรกิจ
- ขอบเขตของโปรเจกต์ (scope) — สิ่งที่ทำ และสิ่งที่ไม่ทำ

เอกสารในโฟลเดอร์นี้ควรเป็น **ต้นทาง (source of truth)** ของความต้องการ ก่อนที่จะถูกแตกไปเป็นแผนงานใน [[../02-plan/index|02-plan]] และงานย่อยใน [[../03-task/index|03-task]]

## ระบบ ID ที่ใช้ในโฟลเดอร์นี้ (อ่านก่อนเขียนเอกสารใหม่)

| ชุด ID | จำนวน | เจ้าของเอกสาร | ใช้กับอะไร |
|---|---|---|---|
| `US-01` … `US-45`, `US-50` | 46 | [[product-backlog-v1\|Product Backlog v1]] | **Functional requirement** — user story ที่ demo ได้ |
| `NFR-01` … `NFR-20` | 20 | [[nfr-v1\|NFR v1]] | **Non-functional requirement** — ความเร็ว/ความทนทาน/ความปลอดภัย/ความเป็นส่วนตัว/การเข้าถึง |
| `UX-01` … `UX-19` | 19 | [[ux-requirements-v1\|UX Requirements v1]] | เกณฑ์ usability ที่วัดผลได้ (01–12) + error/empty/edge state (13–19) |
| `Business Rule ข้อ 1` … `ข้อ 27` | 27 | [[product-backlog-v1\|Product Backlog v1]] §3 | กฎทางธุรกิจ — **ไม่มี prefix ตัวอักษร ห้ามเลื่อนเลข** มีการอ้างอิงกระจายกว่า 40 จุด |
| `F-01` … `F-09` (+ `F-xx.y`) | 9 | [[feature-list-v1\|Feature List v1]] | มุมมองลำดับชั้นของฟีเจอร์ |
| `AC-<US>-<n>` เช่น `AC-04-2` | 192 (`AC-01-1` … `AC-50-7`, ครอบ US-01 ถึง US-45 และ US-50 ครบทุกตัว) | [[acceptance-criteria-v1\|Acceptance Criteria v1]] | **Acceptance criteria รายข้อ** — ให้ test case ผูกกลับได้ละเอียดกว่าระดับ `US-xx` |

> **เลข US ตัวถัดไปที่เปิดได้คือ `US-51`** — `US-46` ถึง `US-49` ถูกจองไว้เป็นข้อเสนอใน [[feature-list-v1|Feature List v1]] §5 ที่ยังรอ Touch/XAVIER ตัดสิน · `US-50` (นมโอ๊ต) ถูกใช้ไปแล้วเมื่อ 2026-08-16 · **ห้ามใช้เลขซ้ำ**
> ที่มาของการจัดระเบียบนี้: [[traceability-audit-v1|Traceability Audit v1]] finding **F-1** — เดิมโปรเจกต์นี้ไม่มี ID สำหรับ non-functional requirement เลย ทำให้ NFR สำคัญกระจายอยู่ 3 ระบบคนละแบบ และ 2 ข้อไม่มีเจ้าภาพจน `02-design` ไม่ได้ออกแบบรองรับ

## เอกสารในโฟลเดอร์นี้

- [[product-backlog-v1|Product Backlog v1]] — actor, user story ครบทุกบทบาท (ลูกค้า/ครัว-บาร์/แคชเชียร์/แอดมิน), acceptance criteria, business rules, MoSCoW, และขอบเขตงาน (in/out of scope) ของระบบสั่งอาหารด้วย QR code — **ต้นทางของ `US-xx` และ `Business Rule ข้อ N`**
- [[nfr-v1|NFR v1]] — **ทะเบียนกลางของ non-functional requirement** `NFR-01` ถึง `NFR-20` ใน 6 หมวด (Performance / Concurrency & Reliability / Session & Operability / Security & Access / Privacy-PDPA / Accessibility) ทุกข้อมีเกณฑ์ที่วัดผลได้และระบุต้นทาง · **ชี้กลับไปที่ business rule และ UX-xx เดิม ไม่ได้แทนที่** · ระบุชัดว่า **NFR-06 / NFR-10 / NFR-11 ของ Phase 0 ยังไม่มีใน `02-design` เลย**
- [[traceability-audit-v1|Traceability Audit v1]] — **ผลตรวจสอบความสอดคล้อง backlog → design → test** ตาราง traceability ครบทั้ง 45 US + UX + Business Rule พร้อม GAP 6 ข้อ, ORPHAN 9 รายการ, finding เรื่องระบบ ID, 18 คำถามจาก COULSON ที่ยังไม่มีคำตอบ และ 7 US ที่ AC วัดผลไม่ได้ · **ใช้เป็นจุดตั้งต้นก่อนแก้ requirement รอบถัดไป**
- [[feature-list-v1|Feature List v1]] — **สถานะ DRAFT** feature hierarchy เต็มระบบ (feature → sub-feature → capability) แม็ปกับ US-01 ถึง US-45 ครบทุกตัว พร้อม coverage check, gap check ย้อนกลับ, ความสามารถที่ซ้ำซ้อนข้าม story, และข้อเสนอ backlog item ใหม่ (US-46 ถึง US-49 — รอ XAVIER/Touch อนุมัติ) จัดทำโดย PEGGY
- [[acceptance-criteria-v1|Acceptance Criteria v1]] — **สถานะ ACTIVE (สร้าง 2026-08-16 · ย้าย AC ครบทุก US แล้ว 2026-08-16)** ทะเบียน AC ที่มี **ID ถาวร** (`AC-<US>-<n>`) 192 แถว ครอบ US-01 ถึง US-45 และ US-50 ครบทุกตัว พร้อมสถานะความพร้อมทดสอบรายข้อ (191 ✅ วัดผลได้ / 1 ⛔ ประวัติที่ถูกแทนที่แล้ว / 0 🔶 · 🔴 ในรอบนี้) · **เจ้าของคือ XAVIER — OKOYE เสนอแก้ได้แต่แก้เองไม่ได้** · หัวข้อ 5 บันทึกกรณีศึกษา 7 US ที่ AC เคยวัดผลไม่ได้และถูกปิดไปแล้ว (US-15 "และ/หรือ", US-02 "ใช้งานได้ดีบนมือถือ" ฯลฯ) · หัวข้อ 6 มี 2 ข้อเสนอ AC ที่ backlog ยังไม่มี (US-09 หมายเหตุแพ้อาหาร, US-26 เปิดรับออเดอร์กลับ) รอ Touch เคาะ
- [[initial-menu-data-v1|Initial Menu Data v1]] — **สถานะ DRAFT** เมนูและราคาตั้งต้น 19 รายการ หมวด **ร้อน / เย็น** (ตัดหมวดปั่นออกตามคำสั่ง Touch) พร้อม option group (ความหวาน 5 ระดับ 0/25/50/75/100% default 50% — US-43, ระดับการคั่ว US-35, เมล็ดพิเศษ US-36) — ราคาอ้างอิงจาก UNO Coffee ผ่านรีวิว/สื่อ **ไม่ใช่เมนูทางการ** ทุกตัวเลขกำกับที่มาไว้ครบ รอ Touch เคาะราคาขายจริง

### ชุดเอกสาร UX (Week 3) — สถานะ DRAFT รออนุมัติจาก Touch

อ่านตามลำดับนี้ (แต่ละฉบับต่อยอดจากฉบับก่อนหน้า):

1. [[ux-persona-v1|UX Persona v1]] — proto-persona 5 ตัว (ฟ้า / ต้น / ป้าน้อย / เบียร์ / คุณแอน) พร้อม goals, pain points, และการแม็ปกับ user story ID จาก backlog
2. [[ux-journey-map-v1|UX Journey Map v1]] — journey map 4 เส้น (dine-in / takeaway / worst-case ผู้สูงวัย / มุมพนักงานช่วง peak), moment of truth, pain point ข้าม journey, และข้อเสนอ user story ใหม่ US-37 ถึง US-41 (**Touch อนุมัติแล้ว 2026-08-11** — เขียนลง backlog หมวด 2.8 เรียบร้อย)
3. [[ux-requirements-v1|UX Requirements v1]] — UX principles, usability requirement ที่วัดผลได้ (**UX-01 ถึง UX-12**), accessibility (WCAG 2.1 AA), error/empty/edge states (**UX-13 ถึง UX-19** — ติด ID ให้แล้ว 2026-08-16 เพื่อให้ error contract ใน `02-design` อ้างกลับมาได้) และเกณฑ์ยอมรับสำหรับ usability test

> เอกสารทั้ง 3 ฉบับนี้เป็น **ข้อกำหนดระดับ requirement ไม่ใช่ตัวดีไซน์** — wireframe/mockup และ design system เป็นงานของ [[../../02-design/01-prototypes/index|02-design/01-prototypes]]
> **สถานะ 2026-08-11:** Touch อนุมัติข้อเสนอ US-37 ถึง US-41 แล้ว — เขียนลง [[product-backlog-v1|Product Backlog v1]] หมวด 2.8 พร้อม Business Rule ข้อ 22-23 และไหลเข้า [[../02-plan/release-roadmap-v1|02-plan/release-roadmap-v1]] (Phase 1/2) + [[../03-task/mvp-task-breakdown-v1|03-task/mvp-task-breakdown-v1]] (เฉพาะ accessibility baseline และการเตรียมทางให้ US-41 ที่เป็นงาน Phase 0) เรียบร้อย
> ตัวเอกสาร UX ทั้ง 3 ฉบับยังคงสถานะ **DRAFT** เพราะ NEED-INPUT ที่เหลือ (ทำเลร้าน, สัดส่วน dine-in/takeaway, ความรุนแรงของ peak, อุปกรณ์จอครัว-บาร์, สองภาษาใน MVP, ระดับ WCAG) ยังไม่ปิด
