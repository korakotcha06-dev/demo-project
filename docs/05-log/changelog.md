# Changelog & Decision Log

บันทึกความเคลื่อนไหวและการตัดสินใจสำคัญของโปรเจกต์แบบเรียงตามลำดับเวลา (ใหม่สุดอยู่บนสุด) ตามที่อธิบายไว้ใน [[index|05-log]]

กลับไปที่ [[index|05-log]]

---

## 2026-08-02 — เริ่มต้น product backlog ระบบสั่งอาหารด้วย QR Code (v1)

- สร้าง product backlog เริ่มต้น (v1) ที่ [[../01-requirements/01-spec/product-backlog-v1|01-spec/product-backlog-v1]] จากโจทย์ตั้งต้นใน `CLAUDE.md` — แตกเป็น 4 actors (ลูกค้า / พนักงานครัว-บาร์ / แคชเชียร์ / แอดมิน), 27 user stories พร้อม acceptance criteria, business rules, และขอบเขตงาน (in/out of scope)
- จัดกลุ่ม backlog เป็น phase ที่ [[../01-requirements/02-plan/release-roadmap-v1|02-plan/release-roadmap-v1]] — Phase 0 (MVP: สแกน QR → เมนู → สั่ง → แจ้งครัว → ปิดบิล) / Phase 1 (ตัวเลือกสินค้า, ใบเสร็จ, คืนเงิน, รายงาน) / Phase 2 (หลายภาษา, สมาชิก/แต้ม, จ่ายเงินออนไลน์, สิทธิ์ผู้ใช้งาน)
- แตก Phase 0 เป็น task breakdown พร้อมส่งต่อ COULSON เริ่ม `02-design` ที่ [[../01-requirements/03-task/mvp-task-breakdown-v1|03-task/mvp-task-breakdown-v1]]
- Touch ยืนยันกฎธุรกิจ 2 ข้อที่เดิมเป็นเพียง assumption/implicit ใน v1 — **(1)** QR ต่อโต๊ะเป็นแบบ static คงที่ 1 โต๊ะ : 1 QR ไม่มี flow regenerate ต่อออเดอร์หรือต่อรอบลูกค้า **(2)** สถานะโต๊ะ (เปิด/ว่าง) ต้อง derive จากวงจรชีวิตออเดอร์เท่านั้น (เปิดเมื่อออเดอร์แรกของรอบเข้าระบบ, ปิดเมื่อแคชเชียร์ปิดบิล/checkout) ไม่ใช่ manual toggle ของพนักงาน — บันทึกเป็น Business Rule ข้อ 10-11 ใน product-backlog-v1 พร้อมอัปเดต acceptance criteria ของ US-01, US-04, US-19, US-24 และ task breakdown ที่เกี่ยวข้องให้สอดคล้องกัน
- ประเด็นที่ยังค้างรอ Touch ตัดสินใจ (ไม่บล็อกการเริ่ม `02-design` ของ Phase 0): จ่ายเงินก่อนหรือหลังส่งออเดอร์เข้าครัว, แชร์ตะกร้าต่อโต๊ะหรือแยกบิลต่อคน (split bill), รูปแบบโปรแกรมสมาชิก/แต้ม — ดูรายละเอียดที่หัวข้อ NEED-INPUT ใน [[../01-requirements/01-spec/product-backlog-v1|01-spec/product-backlog-v1]]
