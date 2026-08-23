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
| [[high-level-architecture-conceptual-v1\|High-Level Architecture (Conceptual) v1]] | 🆕 จัดทำโดย **VISION** — ภาพรวมระบบเชิงแนวคิด **ไม่ผูกกับเทคโนโลยี/vendor**: system context, logical component, data flow ตาม user journey (J1-J4), conceptual data domain, trust boundary, ตาราง cross-cutting capability · เป็นต้นทางที่ Architecture v1 ควรย้อนกลับมาตรวจสอบ ไม่ใช่ทางกลับกัน | DRAFT |
| [[architecture-v1\|Architecture v1]] | สถาปัตยกรรม Phase 0 — surface ทั้ง 3, การเลือก stack พร้อมทางเลือกที่ไม่เลือก, กลไก realtime, การ deploy, ตารางความเสี่ยงทางเทคนิค | DRAFT |
| [[data-model-v1\|Data Model v1]] | ER/schema ของ Phase 0 ครบ 21 entity, state machine ของออเดอร์และโต๊ะ, invariant ระดับฐานข้อมูล, การไล่ข้อกำหนดที่ล็อกไว้ทีละข้อ | DRAFT |
| [[api-design-v1\|API Design v1]] | Endpoint แยกตาม surface (guest/staff/admin), กฎ authorization, การจัดการ race condition, error contract ที่ตรงกับ UX Requirements | DRAFT |
| [[detailed-design-v1\|Detailed Design v1]] | 🆕 จัดทำโดย **COULSON** — แตกชั้น "Route Handlers" เป็น 10 module โดเมน + 6 platform module พร้อม dependency rule, โครงร่าง request-handling 7 ขั้นที่ endpoint ทุกตัวใช้ร่วมกัน, กลไกระดับ implementation (argon2id, rate limit, sliding session, idempotency, LISTEN/NOTIFY, VAT rounding, tenancy guard) และ **11 จุดที่เอกสาร architecture/data-model/api-design ไม่ตรงกัน** ที่พบระหว่างเขียน (2 จุดเป็นบั๊กเรื่องเงินที่ต้องแก้ก่อนเริ่ม build) · แผนภาพประกอบยังไม่ได้วาด (ดู §8 ของไฟล์) | DRAFT — แผนภาพค้าง |
| [[ai-landscape-v1\|AI Landscape v1]] | **TPQI 7002 (ส่วน AI Landscape)** — สำรวจและประเมินเทคโนโลยี AI ที่เกี่ยวข้องกับระบบนี้ แยก "AI ในกระบวนการพัฒนา" (ใช้อยู่จริง) ออกจาก "AI ในตัวผลิตภัณฑ์" (**ตัดสินใจว่า Phase 0 ไม่มีเลย**) พร้อมตาราง adopt/watch/avoid, จุดยืนจริยธรรม AI + PDPA และ 4 สิ่งที่ Phase 0 ต้องเผื่อไว้เพื่อไม่ปิดทางอนาคต | DRAFT |

ห้าฉบับแรก (High-Level Architecture (Conceptual), Architecture, Data Model, API Design, Detailed Design) ครอบคลุมเฉพาะ **Phase 0 (MVP)** ตาม [[../../01-requirements/02-plan/release-roadmap-v1|Release Roadmap v1]] — ต้นทางของความต้องการอยู่ที่ [[../../01-requirements/01-spec/product-backlog-v1|Product Backlog v1]] และงานฝั่ง UI/flow อยู่ที่ [[../01-prototypes/index|01-prototypes]]

**High-Level Architecture (Conceptual) กับ Architecture v1 คนละหน้าที่กัน:** ฉบับ conceptual (จัดทำโดย VISION) ตอบว่า "ระบบประกอบด้วยอะไร ข้อมูลไหลอย่างไร" แบบไม่ผูกเทคโนโลยี ส่วน Architecture v1 (จัดทำโดย COULSON) ตอบว่า "สร้างด้วยเทคโนโลยีอะไร" — ทั้งสองไฟล์แก้โดยเจ้าของของตัวเองเท่านั้น
