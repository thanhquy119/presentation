import streamlit as st
import datetime
import pandas as pd
from PIL import Image
import time

# Cấu hình trang
st.set_page_config(
    page_title="PediGo - Dịch vụ đặt Pedicab",
    page_icon="🚲",
    layout="wide"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .main-header {
        font-size: 36px;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #004D40;
    }
    .info-text {
        font-size: 18px;
        color: #333333;
    }
    .success-message {
        padding: 20px;
        background-color: #E8F5E9;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Hàm tạo dữ liệu mẫu cho tài xế
def generate_sample_drivers():
    return pd.DataFrame({
        'id': range(1, 6),
        'name': ['Nguyễn Văn A', 'Trần Thị B', 'Lê Văn C', 'Phạm Thị D', 'Hoàng Văn E'],
        'rating': [4.8, 4.9, 4.7, 4.6, 4.9],
        'experience': ['3 năm', '5 năm', '2 năm', '4 năm', '6 năm']
    })

# Khởi tạo session state
if 'booking_completed' not in st.session_state:
    st.session_state.booking_completed = False
if 'selected_driver' not in st.session_state:
    st.session_state.selected_driver = None
if 'estimated_price' not in st.session_state:
    st.session_state.estimated_price = None

# Header
st.markdown('<p class="main-header">PediGo - Dịch vụ đặt Pedicab</p>', unsafe_allow_html=True)

# Sidebar cho đăng nhập và thông tin người dùng
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1506/1506450.png", width=100)
    st.markdown("### Đăng nhập")
    
    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type="password")
    
    if st.button("Đăng nhập"):
        st.success("Đăng nhập thành công!")
    
    st.markdown("---")
    st.markdown("### Menu")
    menu = st.radio("", ["Đặt Pedicab", "Lịch sử chuyến đi", "Khuyến mãi", "Trợ giúp"])

# Main content
if menu == "Đặt Pedicab":
    if not st.session_state.booking_completed:
        # Tạo layout 2 cột
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown('<p class="sub-header">Thông tin chuyến đi</p>', unsafe_allow_html=True)
            
            # Form đặt xe
            pickup_location = st.text_input("Điểm đón", "Hồ Gươm, Hà Nội")
            dropoff_location = st.text_input("Điểm đến", "Văn Miếu, Hà Nội")
            
            # Ngày và giờ đón
            col_date, col_time = st.columns(2)
            with col_date:
                pickup_date = st.date_input("Ngày đón", datetime.date.today())
            with col_time:
                pickup_time = st.time_input("Giờ đón", datetime.time(hour=12, minute=0))
            
            # Số lượng hành khách
            passengers = st.slider("Số lượng hành khách", 1, 3, 2)
            
            # Thêm ghi chú
            special_requests = st.text_area("Ghi chú đặc biệt", 
                                           "Ví dụ: Tôi cần tài xế biết tiếng Anh, dừng chụp ảnh tại các điểm du lịch...")
            
            # Loại dịch vụ
            service_type = st.selectbox("Loại dịch vụ", 
                                       ["Đi thẳng đến điểm đến", 
                                        "Tour tham quan (30 phút)",
                                        "Tour tham quan (1 giờ)", 
                                        "Tour tham quan nửa ngày"])
            
            # Phương thức thanh toán
            payment_method = st.radio("Phương thức thanh toán", ["Tiền mặt", "Thẻ tín dụng", "Ví điện tử"])
            
            if st.button("Tìm tài xế"):
                with st.spinner('Đang tìm tài xế phù hợp...'):
                    time.sleep(2)
                drivers = generate_sample_drivers()
                st.session_state.estimated_price = 150000 if service_type == "Đi thẳng đến điểm đến" else 250000
                st.session_state.selected_driver = drivers.iloc[0]
                st.success("Đã tìm thấy tài xế phù hợp!")
                st.experimental_rerun()
        
        with col2:
            st.markdown('<p class="sub-header">Bản đồ</p>', unsafe_allow_html=True)
            st.image("https://maps.googleapis.com/maps/api/staticmap?center=Hanoi&zoom=13&size=400x400&maptype=roadmap&markers=color:red%7Clabel:A%7CHo+Guom,+Hanoi&markers=color:green%7Clabel:B%7CVan+Mieu,+Hanoi&key=YOUR_API_KEY", 
                    caption="Bản đồ tuyến đường")
            
            st.markdown('<p class="sub-header">Ước tính</p>', unsafe_allow_html=True)
            st.info("Khoảng cách: 2.5 km")
            st.info("Thời gian di chuyển: 15-20 phút")
            st.info("Giá ước tính: 150,000đ - 250,000đ")
    
    elif st.session_state.selected_driver is not None:
        # Hiển thị thông tin tài xế và xác nhận đặt xe
        st.markdown('<p class="sub-header">Thông tin tài xế</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)
        
        with col2:
            st.markdown(f"**Tên tài xế:** {st.session_state.selected_driver['name']}")
            st.markdown(f"**Đánh giá:** {st.session_state.selected_driver['rating']}/5.0")
            st.markdown(f"**Kinh nghiệm:** {st.session_state.selected_driver['experience']}")
            st.markdown(f"**Biển số xe:** P-{1000 + st.session_state.selected_driver['id']}")
        
        st.markdown("---")
        
        st.markdown('<p class="sub-header">Chi tiết chuyến đi</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Điểm đón:** Hồ Gươm, Hà Nội")
            st.markdown("**Điểm đến:** Văn Miếu, Hà Nội")
            st.markdown("**Khoảng cách:** 2.5 km")
        
        with col2:
            st.markdown("**Giá ước tính:** {:,}đ".format(st.session_state.estimated_price))
            st.markdown("**Thời gian đến đón:** 5-7 phút")
            st.markdown("**Mã chuyến đi:** PD" + str(10000 + int(time.time())%10000))
        
        if st.button("Xác nhận đặt xe"):
            st.session_state.booking_completed = True
            st.experimental_rerun()
            
        if st.button("Hủy và tìm tài xế khác"):
            st.session_state.selected_driver = None
            st.experimental_rerun()
    
    if st.session_state.booking_completed:
        st.markdown('<div class="success-message">', unsafe_allow_html=True)
        st.markdown("### 🎉 Đặt xe thành công!")
        st.markdown(f"Tài xế **{st.session_state.selected_driver['name']}** sẽ đón bạn trong khoảng **5-7 phút**.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("### Thông tin chuyến đi")
        st.markdown(f"**Mã chuyến:** PD{10000 + int(time.time())%10000}")
        st.markdown("**Điểm đón:** Hồ Gươm, Hà Nội")
        st.markdown("**Điểm đến:** Văn Miếu, Hà Nội")
        st.markdown(f"**Giá ước tính:** {st.session_state.estimated_price:,}đ")
        
        # Giả lập vị trí tài xế
        st.markdown("### Vị trí tài xế")
        st.image("https://maps.googleapis.com/maps/api/staticmap?center=Hanoi&zoom=15&size=600x300&maptype=roadmap&markers=color:red%7Clabel:A%7CHo+Guom,+Hanoi&markers=color:blue%7Clabel:D%7C21.0245,105.8412&key=YOUR_API_KEY", 
                caption="Tài xế đang di chuyển đến điểm đón")
        
        # Thông tin liên hệ
        st.markdown("### Liên hệ tài xế")
        contact_col1, contact_col2 = st.columns(2)
        with contact_col1:
            if st.button("📞 Gọi điện"):
                st.info("Đang kết nối cuộc gọi...")
        with contact_col2:
            if st.button("💬 Nhắn tin"):
                st.info("Đang mở cửa sổ chat...")
        
        if st.button("Hủy chuyến đi"):
            st.warning("Bạn có chắc chắn muốn hủy chuyến đi không?")
            if st.button("Xác nhận hủy"):
                st.session_state.booking_completed = False
                st.session_state.selected_driver = None
                st.experimental_rerun()

elif menu == "Lịch sử chuyến đi":
    st.markdown('<p class="sub-header">Lịch sử chuyến đi</p>', unsafe_allow_html=True)
    
    # Dữ liệu mẫu cho lịch sử chuyến đi
    history_data = {
        'Ngày': ['15/04/2025', '10/04/2025', '05/04/2025', '01/04/2025'],
        'Điểm đón': ['Hồ Gươm, Hà Nội', 'Nhà hát lớn, Hà Nội', 'Lăng Bác, Hà Nội', 'Chùa Trấn Quốc, Hà Nội'],
        'Điểm đến': ['Văn Miếu, Hà Nội', 'Hồ Tây, Hà Nội', 'Hoàng Thành, Hà Nội', 'Phố cổ, Hà Nội'],
        'Giá': ['150,000đ', '200,000đ', '180,000đ', '250,000đ'],
        'Tài xế': ['Nguyễn Văn A', 'Trần Thị B', 'Lê Văn C', 'Phạm Thị D']
    }
    
    history_df = pd.DataFrame(history_data)
    st.dataframe(history_df, use_container_width=True)
    
    # Hiển thị chi tiết chuyến đi khi chọn
    selected_trip = st.selectbox("Xem chi tiết chuyến đi", history_df['Ngày'] + ' - ' + history_df['Điểm đón'] + ' đến ' + history_df['Điểm đến'])
    
    if selected_trip:
        st.markdown("### Chi tiết chuyến đi")
        st.markdown(f"**Ngày:** {selected_trip.split(' - ')[0]}")
        st.markdown(f"**Tuyến đường:** {selected_trip.split(' - ')[1]}")
        st.markdown("**Đánh giá:** ⭐⭐⭐⭐⭐")
        st.markdown("**Phương thức thanh toán:** Tiền mặt")
        
        # Hiển thị bản đồ tuyến đường
        st.image("https://maps.googleapis.com/maps/api/staticmap?center=Hanoi&zoom=13&size=600x300&maptype=roadmap&path=color:0x0000ff|weight:5|Ho+Guom,+Hanoi|Van+Mieu,+Hanoi&key=YOUR_API_KEY", 
                caption="Tuyến đường đã đi")

elif menu == "Khuyến mãi":
    st.markdown('<p class="sub-header">Khuyến mãi hiện có</p>', unsafe_allow_html=True)
    
    # Hiển thị các khuyến mãi
    promo_col1, promo_col2 = st.columns(2)
    
    with promo_col1:
        st.markdown("### 🎁 Giảm 20% cho chuyến đi đầu tiên")
        st.markdown("Sử dụng mã: **FIRSTRIDE**")
        st.markdown("Hạn sử dụng: 31/05/2025")
        st.button("Áp dụng mã FIRSTRIDE")
    
    with promo_col2:
        st.markdown("### 🌟 Giảm 15% cho Tour nửa ngày")
        st.markdown("Sử dụng mã: **HALFDAY15**")
        st.markdown("Hạn sử dụng: 30/06/2025")
        st.button("Áp dụng mã HALFDAY15")
    
    st.markdown("---")
    
    st.markdown("### Nhập mã khuyến mãi")
    promo_code = st.text_input("Mã khuyến mãi")
    if st.button("Kiểm tra"):
        st.info("Mã khuyến mãi hợp lệ! Bạn sẽ được giảm 10% cho chuyến đi tiếp theo.")

elif menu == "Trợ giúp":
    st.markdown('<p class="sub-header">Trợ giúp & Hỗ trợ</p>', unsafe_allow_html=True)
    
    # Accordion cho các câu hỏi thường gặp
    with st.expander("Làm thế nào để đặt Pedicab?"):
        st.markdown("""
        1. Chọn "Đặt Pedicab" từ menu chính
        2. Nhập điểm đón và điểm đến
        3. Chọn ngày và giờ đón
        4. Nhập số lượng hành khách và các yêu cầu đặc biệt
        5. Chọn loại dịch vụ và phương thức thanh toán
        6. Nhấn "Tìm tài xế" và xác nhận đặt xe
        """)
    
    with st.expander("Phương thức thanh toán nào được chấp nhận?"):
        st.markdown("""
        PediGo chấp nhận các phương thức thanh toán sau:
        - Tiền mặt
        - Thẻ tín dụng/ghi nợ (Visa, Mastercard, JCB)
        - Ví điện tử (MoMo, ZaloPay, VNPay)
        """)
    
    with st.expander("Làm thế nào để hủy chuyến đi?"):
        st.markdown("""
        Để hủy chuyến đi:
        1. Vào trang chi tiết chuyến đi
        2. Nhấn nút "Hủy chuyến đi"
        3. Xác nhận hủy
        
        **Lưu ý:** Việc hủy trước 15 phút sẽ không bị tính phí. Hủy trong vòng 15 phút có thể bị tính phí 20,000đ.
        """)
    
    with st.expander("Tôi quên đồ trên Pedicab phải làm sao?"):
        st.markdown("""
        Nếu bạn quên đồ trên Pedicab:
        1. Vào phần "Lịch sử chuyến đi"
        2. Chọn chuyến đi có vấn đề
        3. Nhấn "Báo cáo đồ thất lạc"
        4. Điền thông tin chi tiết về vật phẩm bị mất
        
        Đội ngũ hỗ trợ sẽ liên hệ với tài xế và thông báo cho bạn trong vòng 24 giờ.
        """)
    
    # Form liên hệ
    st.markdown("### Liên hệ hỗ trợ")
    contact_issue = st.text_input("Vấn đề của bạn")
    contact_detail = st.text_area("Mô tả chi tiết")
    contact_email = st.text_input("Email liên hệ")
    
    if st.button("Gửi yêu cầu hỗ trợ"):
        st.success("Yêu cầu hỗ trợ đã được gửi! Chúng tôi sẽ phản hồi trong vòng 24 giờ.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center">
    <p>© 2025 HISTORIC WHEELS</p>
</div>
""", unsafe_allow_html=True)
