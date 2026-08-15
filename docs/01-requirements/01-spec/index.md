# 01 - Spec

เก็บเอกสาร **ข้อกำหนดของโปรเจกต์ (Requirements / Specification)** เช่น

- Feature requirements — ฟีเจอร์ที่ต้องมีในระบบ
- User stories / use cases
- Business rules และเงื่อนไขทางธุรกิจ
- ขอบเขตของโปรเจกต์ (scope) — สิ่งที่ทำ และสิ่งที่ไม่ทำ

เอกสารในโฟลเดอร์นี้ควรเป็น **ต้นทาง (source of truth)** ของความต้องการ ก่อนที่จะถูกแตกไปเป็นแผนงานใน [[../02-plan/index|02-plan]] และงานย่อยใน [[../03-task/index|03-task]]

## เอกสารในโฟลเดอร์นี้

- [[product-backlog-v1|Product Backlog v1]] — actor, user story ครบทุกบทบาท (ลูกค้า/ครัว-บาร์/แคชเชียร์/แอดมิน), acceptance criteria, business rules, และขอบเขตงาน (in/out of scope) ของระบบสั่งอาหารด้วย QR code
- [[feature-list-v1|Feature List v1]] — **สถานะ DRAFT** feature hierarchy เต็มระบบ (feature → sub-feature → capability) แม็ปกับ US-01 ถึง US-45 ครบทุกตัว พร้อม coverage check, gap check ย้อนกลับ, ความสามารถที่ซ้ำซ้อนข้าม story, และข้อเสนอ backlog item ใหม่ (US-46 ถึง US-49 — รอ XAVIER/Touch อนุมัติ) จัดทำโดย PEGGY
- [[initial-menu-data-v1|Initial Menu Data v1]] — **สถานะ DRAFT** เมนูและราคาตั้งต้น 19 รายการ หมวด **ร้อน / เย็น** (ตัดหมวดปั่นออกตามคำสั่ง Touch) พร้อม option group (ความหวาน 5 ระดับ 0/25/50/75/100% default 50% — US-43, ระดับการคั่ว US-35, เมล็ดพิเศษ US-36) — ราคาอ้างอิงจาก UNO Coffee ผ่านรีวิว/สื่อ **ไม่ใช่เมนูทางการ** ทุกตัวเลขกำกับที่มาไว้ครบ รอ Touch เคาะราคาขายจริง

### ชุดเอกสาร UX (Week 3) — สถานะ DRAFT รออนุมัติจาก Touch

อ่านตามลำดับนี้ (แต่ละฉบับต่อยอดจากฉบับก่อนหน้า):

1. [[ux-persona-v1|UX Persona v1]] — proto-persona 5 ตัว (ฟ้า / ต้น / ป้าน้อย / เบียร์ / คุณแอน) พร้อม goals, pain points, และการแม็ปกับ user story ID จาก backlog
2. [[ux-journey-map-v1|UX Journey Map v1]] — journey map 4 เส้น (dine-in / takeaway / worst-case ผู้สูงวัย / มุมพนักงานช่วง peak), moment of truth, pain point ข้าม journey, และข้อเสนอ user story ใหม่ US-37 ถึง US-41 (**Touch อนุมัติแล้ว 2026-08-11** — เขียนลง backlog หมวด 2.8 เรียบร้อย)
3. [[ux-requirements-v1|UX Requirements v1]] — UX principles, usability requirement ที่วัดผลได้ (UX-01 ถึง UX-12), accessibility (WCAG 2.1 AA), error/edge states และเกณฑ์ยอมรับสำหรับ usability test

> เอกสารทั้ง 3 ฉบับนี้เป็น **ข้อกำหนดระดับ requirement ไม่ใช่ตัวดีไซน์** — wireframe/mockup และ design system เป็นงานของ [[../../02-design/01-prototypes/index|02-design/01-prototypes]]
> **สถานะ 2026-08-11:** Touch อนุมัติข้อเสนอ US-37 ถึง US-41 แล้ว — เขียนลง [[product-backlog-v1|Product Backlog v1]] หมวด 2.8 พร้อม Business Rule ข้อ 22-23 และไหลเข้า [[../02-plan/release-roadmap-v1|02-plan/release-roadmap-v1]] (Phase 1/2) + [[../03-task/mvp-task-breakdown-v1|03-task/mvp-task-breakdown-v1]] (เฉพาะ accessibility baseline และการเตรียมทางให้ US-41 ที่เป็นงาน Phase 0) เรียบร้อย
> ตัวเอกสาร UX ทั้ง 3 ฉบับยังคงสถานะ **DRAFT** เพราะ NEED-INPUT ที่เหลือ (ทำเลร้าน, สัดส่วน dine-in/takeaway, ความรุนแรงของ peak, อุปกรณ์จอครัว-บาร์, สองภาษาใน MVP, ระดับ WCAG) ยังไม่ปิด
