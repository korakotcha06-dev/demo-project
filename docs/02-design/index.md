# 02 - Design

รวมเอกสารด้าน **การออกแบบ** ของโปรเจกต์ ต่อยอดมาจากความต้องการใน [[../01-requirements/index|01-requirements]] แบ่งเป็น 2 หมวดย่อย:

- [[01-prototypes/index|01-prototypes]] — ต้นแบบหน้าตา UI/UX (mockup, wireframe)
- [[02-technical/index|02-technical]] — การออกแบบเชิงเทคนิค (architecture, database, API)

ผลลัพธ์จากโฟลเดอร์นี้จะถูกนำไปใช้วางแผนการทดสอบต่อใน [[../03-testing/index|03-testing]]

## สถานะ (2026-08-11) — COULSON รับช่วงต่อจาก XAVIER แล้ว

XAVIER ปิด backlog ของ [[../01-requirements/index|01-requirements]] (US-01 ถึง US-43, Business Rule 1-23) และส่งต่อ COULSON เริ่ม `02-design` ของ **Phase 0** เรียบร้อยแล้ว — เอกสารชุดแรกครบทั้ง 2 หมวดย่อย

### 🔴 ลำดับความสำคัญของแหล่งอ้างอิง (Precedence) — Touch ยืนยัน 2026-08-11

> **`01-requirements` คือ source of truth เสมอ** — theme design ที่ Touch ให้มา (`Artisan Coffee Design System` จากโฟลเดอร์ `picture coffee/POS coffee shop UI mockups`) เป็น **ตัวอย่างสีและแนวการออกแบบเท่านั้น** ได้แก่ palette, บุคลิกตัวอักษร, จังหวะ spacing, radius, เงา และความรู้สึกโดยรวม (near-monochrome + lime accent จุดเดียว)
> theme **ไม่ใช่**ที่มาของโครงสร้างข้อมูล, ผังหน้าจอ (IA), user flow, จำนวนหน้าจอ, ความหมายของ component หรือพฤติกรรมใด ๆ — เมื่อ theme ขัดกับ requirement **ให้ทำตาม requirement เสมอ** แล้วบันทึกเหตุผลไว้ในเอกสาร ไม่ใช่ประนีประนอมกับ theme
> ตัวอย่างที่ใช้สิทธิ์นี้ไปแล้ว: accessibility baseline (Business Rule ข้อ 23) override ค่าสี/ขนาดของ theme หลายจุดที่ contrast ไม่ผ่าน · theme เป็นแอป pick-up/delivery แต่ของเราเป็น QR โต๊ะ (dine-in) + QR เคาน์เตอร์ (takeaway) ตาม Business Rule ข้อ 12 · theme มีแค่ surface มือถือลูกค้า แต่ของเราต้องมี 3 surface
