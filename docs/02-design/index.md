# 02 - Design

รวมเอกสารด้าน **การออกแบบ** ของโปรเจกต์ ต่อยอดมาจากความต้องการใน [[../01-requirements/index|01-requirements]] แบ่งเป็น 2 หมวดย่อย:

- [[01-prototypes/index|01-prototypes]] — ต้นแบบหน้าตา UI/UX (mockup, wireframe)
- [[02-technical/index|02-technical]] — การออกแบบเชิงเทคนิค (architecture, database, API)

ผลลัพธ์จากโฟลเดอร์นี้จะถูกนำไปใช้วางแผนการทดสอบต่อใน [[../03-testing/index|03-testing]]

## สถานะ (2026-08-22) — เข้าสู่ implementation แล้ว

เอกสารชั้นนี้ถูก **นำไปสร้างของจริง** แล้วใน repo แยก <https://github.com/korakotcha06-dev/qr-order-app> (private) — ดู [[../05-log/changelog|05-log/changelog]] วันที่ 2026-08-22

รอบแรกปิด **schema เต็ม + เส้นทาง dine-in (J1) ครบวง + 12 จาก 23 หน้าจอ** — ช่องทางเคาน์เตอร์และหน้าจอแอดมินยังไม่ทำ

🔴 **ช่องว่างของเอกสารชั้นนี้ที่เจอตอนลงมือ และยังต้องแก้ที่ตัวเอกสาร:**

1. **ER ใน [[02-technical/data-model-v1|data-model-v1]] §2 สมมติว่า `visit_session` มีอยู่แล้ว แต่ BR ข้อ 11 เปิดมันที่ออเดอร์ใบแรก** — ช่วงก่อนออเดอร์ใบแรกจึงไม่มีอะไรให้ผูกตะกร้าร่วม (BR ข้อ 2) และไม่มีที่มาของจุดบริการ · โค้ดแก้ด้วยการผูกตะกร้า dine-in กับ **จุดบริการ** แทน (`cart.scope='service_point'`) — เอกสารควรเขียน ER ให้ตรง
2. ~~**architecture-v1 §10 อ้าง `nfr-v1` ที่ไม่มีอยู่จริง**~~ — ✅ **ปิดแล้ว 2026-08-22** สร้าง [[../01-requirements/01-spec/nfr-v1|nfr-v1]] ครบ 20 ข้อ โดยกู้โครงสร้างจาก `nfr-status-v1.html` ที่ประกาศตัวเองว่าวาดจาก §7 → เลข NFR ทุกตัวที่เอกสารอื่นอ้าง (06/07/10/11/14/15/17) ลงล็อกกับการนับที่กู้คืนมาได้พอดี · **ลิงก์ขาดของ vault เหลือศูนย์**
3. **[[02-technical/api-design-v1|api-design-v1]] คลาดจากการ rename ของ data-model §9.4** — §5.6 ยังใช้ `table_id` · §3 ยังเขียน `table_status_v`
4. **VAT (data-model §10) ยังไม่มี US รองรับ** — โค้ดใส่คอลัมน์ไว้แล้วแต่ปิดใช้งาน จนกว่าจะเปิด US ใหม่

---

## สถานะ (2026-08-11) — COULSON รับช่วงต่อจาก XAVIER แล้ว

XAVIER ปิด backlog ของ [[../01-requirements/index|01-requirements]] (US-01 ถึง US-43, Business Rule 1-23) และส่งต่อ COULSON เริ่ม `02-design` ของ **Phase 0** เรียบร้อยแล้ว — เอกสารชุดแรกครบทั้ง 2 หมวดย่อย

### 🔴 ลำดับความสำคัญของแหล่งอ้างอิง (Precedence) — Touch ยืนยัน 2026-08-11

> **`01-requirements` คือ source of truth เสมอ** — theme design ที่ Touch ให้มา (`Artisan Coffee Design System` จากโฟลเดอร์ `picture coffee/POS coffee shop UI mockups`) เป็น **ตัวอย่างสีและแนวการออกแบบเท่านั้น** ได้แก่ palette, บุคลิกตัวอักษร, จังหวะ spacing, radius, เงา และความรู้สึกโดยรวม (near-monochrome + lime accent จุดเดียว)
> theme **ไม่ใช่**ที่มาของโครงสร้างข้อมูล, ผังหน้าจอ (IA), user flow, จำนวนหน้าจอ, ความหมายของ component หรือพฤติกรรมใด ๆ — เมื่อ theme ขัดกับ requirement **ให้ทำตาม requirement เสมอ** แล้วบันทึกเหตุผลไว้ในเอกสาร ไม่ใช่ประนีประนอมกับ theme
> ตัวอย่างที่ใช้สิทธิ์นี้ไปแล้ว: accessibility baseline (Business Rule ข้อ 23) override ค่าสี/ขนาดของ theme หลายจุดที่ contrast ไม่ผ่าน · theme เป็นแอป pick-up/delivery แต่ของเราเป็น QR โต๊ะ (dine-in) + QR เคาน์เตอร์ (takeaway) ตาม Business Rule ข้อ 12 · theme มีแค่ surface มือถือลูกค้า แต่ของเราต้องมี 3 surface
