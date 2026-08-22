# 01 - Prototypes

เก็บ **ต้นแบบหน้าตาของระบบ (UI/UX Prototype)** เช่น

- Wireframe / mockup ของแต่ละหน้าจอ
- User flow และ navigation flow
- Design system เบื้องต้น เช่น สี ฟอนต์ คอมโพเนนต์หลัก

ใช้สำหรับสื่อสารและตกลงหน้าตาของระบบก่อนลงมือพัฒนาจริง โดยอ้างอิงความต้องการจาก [[../../01-requirements/01-spec/index|01-spec]] และส่งต่อรายละเอียดเชิงระบบให้ [[../02-technical/index|02-technical]]

---

## เอกสารในโฟลเดอร์นี้

| เอกสาร | เนื้อหา | สถานะ |
|---|---|---|
| [[design-system-adoption-v1\|Design System Adoption v1]] | การรับ theme "Artisan Coffee" มาใช้ — token ที่รับตรง ๆ vs ที่ override, accessibility override layer พร้อมค่า contrast ที่คำนวณแล้ว, font stack ไทย+ละติน, รูปแบบราคาบาท, inventory ของ component ที่ theme มีให้แม็ปกับ US, และช่องว่างของ theme | DRAFT |
| [[screen-inventory-v1\|Screen Inventory v1]] | รายการหน้าจอทั้งหมดของ Phase 0 จำนวน 23 หน้าจอ แยก 3 surface (ลูกค้ามือถือ 7 · จอสถานีพนักงาน 8 · จอแอดมิน 8) พร้อม US ที่รองรับ, persona, สิ่งที่ต้องมีบนหน้าจอ, state ที่ต้องออกแบบ และ component ที่ใช้ | DRAFT |
| [[user-flow-v1\|User Flow v1]] | User flow ของ Phase 0 — J1 dine-in · J2 takeaway เคาน์เตอร์ · J3 พนักงานคีย์แทน · J4 ฝั่งพนักงาน พร้อม state machine ของสถานะโต๊ะและสถานะออเดอร์ | DRAFT |

| [[diagrams/index\|Diagrams]] | แผนภาพทั้งหมด 17 ภาพที่วาดจากเอกสารในโปรเจกต์ — user flow, ผังหน้าจอ, สถาปัตยกรรม, ER, state machine, ความเสี่ยง และแผนเฟส | ใช้อยู่ |

ลำดับการอ่าน: **Design System Adoption → Screen Inventory → User Flow**

**ยังไม่ได้ทำในรอบนี้ (งานถัดไปของ SHURI):** wireframe/mockup รายหน้าจอ, prototype แบบกดผ่านได้, และ design token ที่ implement จริงเป็นโค้ด

## บันทึกการตรวจ mockup

- [[mockup-thyna-pos-v1|Mockup Review — Thyna Cafe POS v1]] — ตรวจ mockup ชุด Thyna ที่ Touch ชี้ให้ดู (2026-08-22) · **ปิดช่องว่างที่ [[design-system-adoption-v1|design-system-adoption-v1]] §6.1 บันทึกว่า theme ไม่มีหน้าจอพนักงานเลย** · 5 จุดที่ยืนยันว่าออกแบบถูกทาง · 1 จุดที่รับมาใช้แล้ว (กระดาน 3 คอลัมน์) · **11 จุดที่ไม่รับมาพร้อมเหตุผล** โดยเรื่องใหญ่สุดคือ mockup แสดงชื่อลูกค้าบนตั๋วซึ่งขัด Business Rule ข้อ 14 ตรง ๆ
