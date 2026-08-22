# 02 - Technical

เก็บเอกสาร **การออกแบบเชิงเทคนิค (Technical Design)** เช่น

- System architecture / โครงสร้างระบบโดยรวม
- Database schema
- API design / data contract
- เทคโนโลยีและไลบรารีที่เลือกใช้ พร้อมเหตุผล

เอกสารในโฟลเดอร์นี้คือพิมพ์เขียวที่ทีมพัฒนาใช้อ้างอิงตอนลงมือเขียนโค้ด และเป็นฐานในการวางแผนทดสอบใน [[../../03-testing/01-test-plan/index|01-test-plan]]

## เอกสารในโฟลเดอร์นี้

| เอกสาร | เนื้อหา | สถานะ |
|---|---|---|
| [[architecture-v1\|Architecture v1]] | สถาปัตยกรรม Phase 0 — surface ทั้ง 3, การเลือก stack พร้อมทางเลือกที่ไม่เลือก, กลไก realtime, การ deploy, ตารางความเสี่ยงทางเทคนิค | DRAFT |
| [[data-model-v1\|Data Model v1]] | ER/schema ของ Phase 0 ครบ 21 entity, state machine ของออเดอร์และโต๊ะ, invariant ระดับฐานข้อมูล, การไล่ข้อกำหนดที่ล็อกไว้ทีละข้อ | DRAFT |
| [[api-design-v1\|API Design v1]] | Endpoint แยกตาม surface (guest/staff/admin), กฎ authorization, การจัดการ race condition, error contract ที่ตรงกับ UX Requirements | DRAFT |
| [[vat-tax-invoice-reference-v1\|VAT & ใบกำกับภาษี Reference v1]] | **เอกสารอ้างอิงจากภายนอก ไม่ใช่ข้อกำหนด** — ถอดความรู้เรื่อง VAT และใบกำกับภาษีอิเล็กทรอนิกส์จาก source code ของเครื่องมือ ETDA (ขมธอ. 3-2560 v2.0) ตอบคำถามที่ [[data-model-v1\|Data Model]] §10.5 เปิดค้างไว้ · มีบันไดยอดเงินตามมาตรฐาน, รหัสประเภทเอกสารที่ร้านกาแฟต้องใช้ (**T03** ไม่ใช่ 388), ช่องว่าง 6 ข้อเรียงตามต้นทุนถ้าทำทีหลัง และคำถาม 6 ข้อที่ต้องให้ Touch + ผู้ทำบัญชีตัดสินก่อนเขียน US-21 | REFERENCE |
| [[ai-landscape-v1\|AI Landscape v1]] | **TPQI 7002 (ส่วน AI Landscape)** — สำรวจและประเมินเทคโนโลยี AI ที่เกี่ยวข้องกับระบบนี้ แยก "AI ในกระบวนการพัฒนา" (ใช้อยู่จริง) ออกจาก "AI ในตัวผลิตภัณฑ์" (**ตัดสินใจว่า Phase 0 ไม่มีเลย**) พร้อมตาราง adopt/watch/avoid, จุดยืนจริยธรรม AI + PDPA และ 4 สิ่งที่ Phase 0 ต้องเผื่อไว้เพื่อไม่ปิดทางอนาคต | DRAFT |

สามฉบับแรกครอบคลุมเฉพาะ **Phase 0 (MVP)** ตาม [[../../01-requirements/02-plan/release-roadmap-v1|Release Roadmap v1]] — ต้นทางของความต้องการอยู่ที่ [[../../01-requirements/01-spec/product-backlog-v1|Product Backlog v1]] และงานฝั่ง UI/flow อยู่ที่ [[../01-prototypes/index|01-prototypes]]
