import streamlit as st
from supabase import create_client, Client
import time

# --- إعدادات الاتصال الآمن (تُجلب من ملف secrets) ---
# السطر الصحيح (نستخدم الاسم البرمجي للمفتاح)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- واجهة المستخدم الاحترافية ---
st.set_page_config(page_title="مكتب الفعاليات | كلية الهندسة الزراعية", page_icon="🌱")

# تنسيقات CSS لتعميق الهوية الزراعية والتفاعلية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; }
    .stButton>button {
        background: linear-gradient(90deg, #2E7D32 0%, #4CAF50 100%);
        color: white; border: none; border-radius: 12px;
        padding: 10px 25px; transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(46, 125, 50, 0.4); }
    .main { background-color: #f9fbf9; }
    </style>
    """, unsafe_allow_html=True)

# عرض اللوغو من المجلد الخاص بك
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    st.image("Logo.png", use_container_width=True)

st.markdown("<h1 style='text-align: center; color: #1B5E20;'>استمارة تطوع مكتب الفعاليات 🎊</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1em;'>شاركنا طاقتك لنصنع فعاليات تليق بكليتنا العريقة 🌾</p>", unsafe_allow_html=True)

# --- الاستمارة ---
with st.expander("📝 اضغط هنا لتعبئة بياناتك", expanded=True):
    with st.form("volunteer_form", clear_on_submit=True):
        name = st.text_input("👤 الاسم الثلاثي")
        
        c1, c2 = st.columns(2)
        with c1:
            year = st.selectbox("🎓 السنة الدراسية", ["السنة الأولى", "السنة الثانية", "السنة الثالثة", "السنة الرابعة", "السنة الخامسة"])
        with c2:
            phone = st.text_input("📞 رقم الهاتف")
            
        skills = st.text_area("🛠️ المهارات (تصميم، تنظيم، تصوير، إلقاء...)", help="لا تتردد في ذكر أي مهارة مهما كانت بسيطة!")
        
        energy = st.select_slider("⚡ حماسك للعمل معنا", options=["هادئ 🌿", "نشيط 🌱", "متحمس 🌳", "خارق 🔥"])
        
        submit = st.form_submit_button("إرسال طلب الانضمام 🚀")

if submit:
    if name and phone:
        with st.spinner('جاري بذر بياناتك في نظامنا... 🌱'):
            # رفع البيانات إلى Supabase
            data = {
                "full_name": name, 
                "academic_year": year, 
                "phone_number": phone, 
                "skills": skills, 
                "energy_level": energy
            }
            response = supabase.table("volunteers").insert(data).execute()
            
            time.sleep(1.5)
            st.balloons()
            st.success("✨ شكراً لتسجيلك يا بطل! سنتواصل معك في أقرب وقت.")
            st.snow() # حركة إضافية للترفيه
    else:
        st.warning("الرجاء التأكد من كتابة الاسم ورقم الهاتف على الأقل ⚠️")
