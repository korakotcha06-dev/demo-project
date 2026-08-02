# Changelog & Decision Log

บันทึกความเคลื่อนไหวและการตัดสินใจสำคัญของโปรเจกต์แบบเรียงตามลำดับเวลา (ใหม่สุดอยู่บนสุด) ตามที่อธิบายไว้ใน [[index|05-log]]

กลับไปที่ [[index|05-log]]

---

## 2026-08-02 — เพิ่มช่องทางพนักงานคีย์ออเดอร์แทนลูกค้าที่สั่งด้วยวาจา (US-30) เข้าช่องทางเคาน์เตอร์

- Touch ให้ feedback เพิ่มเฉพาะช่องทางเคาน์เตอร์/takeaway ที่เพิ่งเพิ่มเข้าไปในรอบก่อนหน้า (US-28/US-29) — ลูกค้าบางคนไม่อยากสแกน QR เอง อยากสั่งด้วยวาจาแบบร้านกาแฟทั่วไป จึงเพิ่ม **US-30** (แคชเชียร์คีย์ออเดอร์แทนลูกค้า + รับชำระเงินในขั้นตอนเดียวกัน) เข้า [[../01-requirements/01-spec/product-backlog-v1|01-spec/product-backlog-v1]] หมวด 2.5 เป็น P0/Phase 0 — ตัดสินใจแยกเป็น story ใหม่ (ไม่ใช่แก้ US-28/US-29) เพราะตัวที่สร้างออเดอร์ (originator: ลูกค้า vs พนักงาน) ต่างกันจริง แม้กฎจ่ายเงินและคิวปลายทางจะใช้ร่วมกัน — ยืนยันชัดเจนว่านี่คือช่องทางเสริม ไม่ใช่การขัดกับโจทย์ตั้งต้นที่ลูกค้าสั่งเองผ่าน QR ยังเป็น default
- ขยาย Business Rule ข้อ 12 เพิ่ม 2 ประเด็น: **(ก)** order origin field (`customer-self` / `staff-entered`) แยกจาก channel field — ทั้งสองที่มาบรรจบกันที่คิว "รอเสิร์ฟ" เดียวกันหลังจ่ายเงินสำเร็จ **(ข)** จุดรับของ ("ปลายเคาน์เตอร์") แยกทางกายภาพจากจุดสั่ง/จ่ายเงิน ต่างจากช่องทางโต๊ะที่พนักงานนำไปเสิร์ฟเอง
- อัปเดต [[../01-requirements/02-plan/release-roadmap-v1|02-plan/release-roadmap-v1]] เพิ่ม US-30 เข้า Phase 0 และ [[../01-requirements/03-task/mvp-task-breakdown-v1|03-task/mvp-task-breakdown-v1]] ขยายกลุ่มงาน G ด้วย 4 task ใหม่ (หน้าจอคีย์ออเดอร์แทนลูกค้า, origin field, การแสดงจุดรับของ, และยืนยันความหมายของ "รอเสิร์ฟ")
- ประเด็นที่ยังไม่ปิดสนิท (ไม่บล็อก Phase 0): ความหมายที่แท้จริงของสถานะ "รอเสิร์ฟ" — ตีความเป็น label ฝั่งจุดรับของ ไม่ใช่ status field ใหม่แยกจาก pipeline ครัวเดิม แต่ COULSON ควรยืนยันกับ Touch อีกครั้งก่อน finalize data model ของสถานะออเดอร์

---

## 2026-08-02 — เขียน retrospective ฉบับแรกของโปรเจกต์ (เฟส requirements/backlog)

- สร้าง [[../04-retrospectives/requirements-phase-retro-v1|04-retrospectives/requirements-phase-retro-v1]] สรุปบทเรียนจากเฟส requirements-gathering/backlog-creation ที่เพิ่งจบ (สร้าง backlog v1 + 2 รอบ refinement ด้านล่าง) — ใช้หลักฐานจาก entry ทั้งสองของ changelog นี้ ไม่ได้อ้างอิงผลทดสอบเพราะ [[../03-testing/02-test-result/index|03-testing/02-test-result]] ยังว่างเปล่าตามที่ควรเป็น (ยังไม่มีโค้ดในโปรเจกต์)
- ประเด็นหลักที่สรุปได้: MVP หลักไม่ต้องแก้ทิศทางตลอด 3 รอบ, การจด default+NEED-INPUT ทำให้ COULSON ไม่ต้องรอครบทุกข้อ, แต่รอบแรกพลาดถามคำถามเชิงปฏิบัติการ (เช่น มีช่องทางเคาน์เตอร์ไหม) ทำให้ต้องแก้ถึง 2 รอบทีหลัง — ตั้ง action item ให้ใช้ "operational reality checklist" ก่อนร่าง backlog รอบแรกของ feature ถัดไป
- อัปเดต [[../04-retrospectives/index|04-retrospectives/index]] ให้ลิงก์เอกสารใหม่เข้า

---

## 2026-08-02 — Touch ให้ feedback เชิงปฏิบัติการ 4 ข้อ คลี่คลายประเด็นเปิดที่เหลือของ backlog v1

- อัปเดต [[../01-requirements/01-spec/product-backlog-v1|01-spec/product-backlog-v1]]: **(1)** เพิ่ม AC ของ US-01 ให้ชัดว่าสแกน QR ต้องเข้าหน้าสั่งอาหารโดยตรง ไม่มีหน้ากลาง **(2)** US-11 (loyalty) มีรูปแบบชัดแล้ว — opt-in + stamp card ซื้อครบ 10 แถมฟรี 1 — เลื่อนจาก P2 เป็น P1 **(3)** เพิ่ม Business Rule ข้อ 12 แยกกฎจ่ายเงินตามช่องทาง: QR โต๊ะ (dine-in) จ่ายที่เคาน์เตอร์เหมือนเดิม vs QR เคาน์เตอร์ (takeaway) ต้องจ่ายก่อนเสมอ ไม่มีจ่ายทีหลัง — เพิ่ม user story ใหม่ US-28 (ลูกค้าสั่ง+รอจ่ายเงินที่เคาน์เตอร์) และ US-29 (แคชเชียร์ยืนยันรับเงิน) **(4)** แก้ Business Rule ข้อ 2 ให้ชัดว่าตะกร้าต่อโต๊ะรองรับการสั่งพร้อมกันจากหลายคน/หลายอุปกรณ์ (concurrent) ตราบใดที่ยังไม่ปิดบิล ไม่ใช่ single-writer cart
- แก้ Business Rule ข้อ 3 ให้ระบุชัดว่าใช้เฉพาะช่องทางโต๊ะ และปิดสถานะ NEED-INPUT เดิมทั้ง 3 ข้อ (จ่ายก่อน/หลัง, แชร์ตะกร้า/split bill, รูปแบบสมาชิก) เป็น resolved ในหัวข้อ 5 ของเอกสาร
- อัปเดต [[../01-requirements/02-plan/release-roadmap-v1|02-plan/release-roadmap-v1]]: เพิ่ม US-28/US-29 เข้า Phase 0 (ถือเป็นความจริงเชิงปฏิบัติการตั้งแต่วันเปิดร้าน ไม่ใช่แค่ dine-in) และย้าย US-11 จาก Phase 2 มา Phase 1
- อัปเดต [[../01-requirements/03-task/mvp-task-breakdown-v1|03-task/mvp-task-breakdown-v1]]: เพิ่มกลุ่มงาน G (ช่องทางเคาน์เตอร์/takeaway) และ task ใหม่ในกลุ่ม A/B สำหรับ channel field และ concurrent cart — ปิด blocker เดิมในหัวข้อ "งานข้ามกลุ่ม" เพราะ Touch ยืนยันแล้ว
- ประเด็นที่ยังเปิดเล็กน้อย (ไม่บล็อก Phase 0): ถ้อยคำ consent/เงื่อนไขของ loyalty stamp card (US-11) เป็นรายละเอียดระดับ copywriting ของ Phase 1

---

## 2026-08-02 — เริ่มต้น product backlog ระบบสั่งอาหารด้วย QR Code (v1)

- สร้าง product backlog เริ่มต้น (v1) ที่ [[../01-requirements/01-spec/product-backlog-v1|01-spec/product-backlog-v1]] จากโจทย์ตั้งต้นใน `CLAUDE.md` — แตกเป็น 4 actors (ลูกค้า / พนักงานครัว-บาร์ / แคชเชียร์ / แอดมิน), 27 user stories พร้อม acceptance criteria, business rules, และขอบเขตงาน (in/out of scope)
- จัดกลุ่ม backlog เป็น phase ที่ [[../01-requirements/02-plan/release-roadmap-v1|02-plan/release-roadmap-v1]] — Phase 0 (MVP: สแกน QR → เมนู → สั่ง → แจ้งครัว → ปิดบิล) / Phase 1 (ตัวเลือกสินค้า, ใบเสร็จ, คืนเงิน, รายงาน) / Phase 2 (หลายภาษา, สมาชิก/แต้ม, จ่ายเงินออนไลน์, สิทธิ์ผู้ใช้งาน)
- แตก Phase 0 เป็น task breakdown พร้อมส่งต่อ COULSON เริ่ม `02-design` ที่ [[../01-requirements/03-task/mvp-task-breakdown-v1|03-task/mvp-task-breakdown-v1]]
- Touch ยืนยันกฎธุรกิจ 2 ข้อที่เดิมเป็นเพียง assumption/implicit ใน v1 — **(1)** QR ต่อโต๊ะเป็นแบบ static คงที่ 1 โต๊ะ : 1 QR ไม่มี flow regenerate ต่อออเดอร์หรือต่อรอบลูกค้า **(2)** สถานะโต๊ะ (เปิด/ว่าง) ต้อง derive จากวงจรชีวิตออเดอร์เท่านั้น (เปิดเมื่อออเดอร์แรกของรอบเข้าระบบ, ปิดเมื่อแคชเชียร์ปิดบิล/checkout) ไม่ใช่ manual toggle ของพนักงาน — บันทึกเป็น Business Rule ข้อ 10-11 ใน product-backlog-v1 พร้อมอัปเดต acceptance criteria ของ US-01, US-04, US-19, US-24 และ task breakdown ที่เกี่ยวข้องให้สอดคล้องกัน
- ประเด็นที่ยังค้างรอ Touch ตัดสินใจ (ไม่บล็อกการเริ่ม `02-design` ของ Phase 0): จ่ายเงินก่อนหรือหลังส่งออเดอร์เข้าครัว, แชร์ตะกร้าต่อโต๊ะหรือแยกบิลต่อคน (split bill), รูปแบบโปรแกรมสมาชิก/แต้ม — ดูรายละเอียดที่หัวข้อ NEED-INPUT ใน [[../01-requirements/01-spec/product-backlog-v1|01-spec/product-backlog-v1]]
