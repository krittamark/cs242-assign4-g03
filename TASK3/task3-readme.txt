Task 3 - Global GDP Data Extractor and DataFrame Creator

คำอธิบาย:
โปรแกรมนี้ดึงข้อมูล GDP ของประเทศต่างๆ จากหน้าวิกิพีเดีย โดยใช้ **requests** และ **BeautifulSoup** เพื่อแยกวิเคราะห์ตารางข้อมูล จากนั้นจะสร้าง **Pandas DataFrames** สำหรับข้อมูล GDP จาก IMF, World Bank, และ United Nations โดยแต่ละ DataFrame จะแสดง Rank, Country, และ GDP ที่เกี่ยวข้อง

วิธีการรัน:
1. เปิดไฟล์ `task3.py` (หรือชื่อไฟล์ที่คุณใช้) ด้วย Python 3
2. โปรแกรมจะทำการร้องขอข้อมูลจาก URL ของวิกิพีเดียที่ระบุ
3. หากการร้องขอสำเร็จ โปรแกรมจะดำเนินการแยกวิเคราะห์ตาราง GDP
4. แสดงผลลัพธ์ต่อไปนี้:
   - สถานะการร้องขอไปยังเว็บไซต์
   - จำนวนตารางทั้งหมดที่พบในหน้าเว็บ
   - รายชื่อแหล่งข้อมูลหลักที่พบ (เช่น IMF, World Bank, United Nations)
   - DataFrame ที่จัดรูปแบบแล้วสำหรับแต่ละแหล่งข้อมูล โดยแสดง Index, Rank, Country, และ GDP (million US$)

โมดูลที่ต้องติดตั้ง:
- requests
- beautifulsoup4 (bs4)
- pandas
- re