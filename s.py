import streamlit as st
import string
import math

# ==========================================================
# CẤU HÌNH TRANG
# ==========================================================

st.set_page_config(
    page_title="An toàn mật khẩu",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CSS - GIAO DIỆN
# ==========================================================

st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #2563eb;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .score-box {
        padding: 20px;
        border-radius: 15px;
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        text-align: center;
        margin: 15px 0;
    }

    .score-number {
        font-size: 42px;
        font-weight: bold;
        color: #2563eb;
    }

    .tip-box {
        padding: 15px;
        border-radius: 12px;
        background-color: #f8fafc;
        border-left: 5px solid #2563eb;
        margin: 10px 0;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 14px;
        margin-top: 40px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================================
# SESSION STATE
# ==========================================================

if "password_checked" not in st.session_state:
    st.session_state.password_checked = False

if "password_score" not in st.session_state:
    st.session_state.password_score = 0

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0


# ==========================================================
# HÀM KIỂM TRA MẬT KHẨU
# ==========================================================

def kiem_tra_mat_khau(password):
    """
    Kiểm tra mật khẩu theo nhiều tiêu chí.
    Trả về điểm, danh sách tiêu chí và thông tin bổ sung.
    """

    checks = {
        "Độ dài từ 8 ký tự": len(password) >= 8,
        "Có chữ hoa": any(c.isupper() for c in password),
        "Có chữ thường": any(c.islower() for c in password),
        "Có chữ số": any(c.isdigit() for c in password),
        "Có ký tự đặc biệt": any(c in string.punctuation for c in password),
        "Độ dài từ 12 ký tự": len(password) >= 12
    }

    diem = sum(checks.values())

    # Điểm cơ bản tối đa 5, tiêu chí 12 ký tự là điểm thưởng
    diem_co_ban = sum([
        checks["Độ dài từ 8 ký tự"],
        checks["Có chữ hoa"],
        checks["Có chữ thường"],
        checks["Có chữ số"],
        checks["Có ký tự đặc biệt"]
    ])

    # Phát hiện các trường hợp dễ đoán
    password_lower = password.lower()

    common_passwords = [
        "123456",
        "12345678",
        "password",
        "qwerty",
        "abc123",
        "111111",
        "123123",
        "admin",
        "letmein",
        "welcome"
    ]

    is_common = password_lower in common_passwords

    # Phát hiện chuỗi lặp
    has_repeated_chars = any(
        password[i] == password[i + 1]
        for i in range(len(password) - 1)
    )

    # Phát hiện mật khẩu chỉ gồm một loại ký tự
    char_types = sum([
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in string.punctuation for c in password)
    ])

    # Độ entropy ước lượng đơn giản
    charset_size = 0

    if any(c.islower() for c in password):
        charset_size += 26

    if any(c.isupper() for c in password):
        charset_size += 26

    if any(c.isdigit() for c in password):
        charset_size += 10

    if any(c in string.punctuation for c in password):
        charset_size += len(string.punctuation)

    if charset_size > 0:
        entropy = len(password) * math.log2(charset_size)
    else:
        entropy = 0

    return {
        "checks": checks,
        "diem_co_ban": diem_co_ban,
        "is_common": is_common,
        "has_repeated_chars": has_repeated_chars,
        "char_types": char_types,
        "entropy": entropy
    }


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<div class="main-title">🔐 AN TOÀN MẬT KHẨU</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Tìm hiểu – kiểm tra – luyện tập để bảo vệ tài khoản tốt hơn!'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("📚 MENU")

    lua_chon = st.radio(
        "Chọn nội dung:",
        [
            "🔎 Kiểm tra mật khẩu",
            "📖 Hướng dẫn an toàn",
            "📝 Trắc nghiệm"
        ]
    )

    st.divider()

    st.info(
        "💡 Mẹo:\n\n"
        "Hãy ưu tiên mật khẩu dài, khó đoán "
        "và không sử dụng lại cho nhiều tài khoản."
    )

    st.divider()

    st.caption("🔐 Password Safety App")
    st.caption("Được xây dựng bằng Python + Streamlit")


# ==========================================================
# MỤC 1 - KIỂM TRA MẬT KHẨU
# ==========================================================

if lua_chon == "🔎 Kiểm tra mật khẩu":

    st.header("🔎 Kiểm tra độ an toàn của mật khẩu")

    st.write(
        "Nhập mật khẩu vào ô bên dưới. "
        "Ứng dụng sẽ kiểm tra các tiêu chí cơ bản."
    )

    password = st.text_input(
        "🔑 Mật khẩu:",
        type="password",
        placeholder="Nhập mật khẩu cần kiểm tra...",
        help="Không nên nhập mật khẩu thật đang sử dụng."
    )

    show_password = st.checkbox("👁️ Hiển thị mật khẩu")

    if show_password and password:
        st.code(password)

    if st.button(
        "🔎 KIỂM TRA MẬT KHẨU",
        type="primary",
        use_container_width=True
    ):

        if not password:

            st.warning("⚠️ Bạn chưa nhập mật khẩu.")

            st.session_state.password_checked = False

        else:

            result = kiem_tra_mat_khau(password)

            st.session_state.password_checked = True
            st.session_state.password_score = result["diem_co_ban"]

            checks = result["checks"]
            diem = result["diem_co_ban"]

            st.divider()

            # --------------------------------------------------
            # ĐIỂM
            # --------------------------------------------------

            st.subheader("📊 Kết quả")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Điểm an toàn",
                    f"{diem}/5"
                )

            with col2:
                st.metric(
                    "Độ dài",
                    f"{len(password)} ký tự"
                )

            st.progress(diem / 5)

            # --------------------------------------------------
            # XẾP LOẠI
            # --------------------------------------------------

            if result["is_common"]:

                st.error(
                    "🚨 Mật khẩu này nằm trong nhóm mật khẩu "
                    "phổ biến và dễ đoán."
                )

            elif diem <= 2:

                st.error(
                    "🔴 YẾU – Mật khẩu cần được cải thiện."
                )

            elif diem <= 4:

                st.warning(
                    "🟡 KHÁ – Mật khẩu đã có một số tiêu chí tốt."
                )

            else:

                st.success(
                    "🟢 TỐT – Mật khẩu đáp ứng các tiêu chí cơ bản!"
                )

            # --------------------------------------------------
            # CHI TIẾT TIÊU CHÍ
            # --------------------------------------------------

            st.subheader("📋 Chi tiết")

            for criterion, passed in checks.items():

                # Không hiển thị tiêu chí 12 ký tự trong điểm cơ bản
                if criterion == "Độ dài từ 12 ký tự":
                    continue

                if passed:
                    st.success(f"✅ {criterion}")
                else:
                    st.error(f"❌ {criterion}")

            # --------------------------------------------------
            # PHÂN TÍCH BỔ SUNG
            # --------------------------------------------------

            st.subheader("🔍 Phân tích thêm")

            if len(password) >= 12:
                st.success(
                    "📏 Mật khẩu có độ dài tốt (từ 12 ký tự)."
                )
            else:
                st.warning(
                    "📏 Nên cân nhắc sử dụng mật khẩu từ 12 ký tự trở lên."
                )

            if result["has_repeated_chars"]:
                st.warning(
                    "🔁 Mật khẩu có các ký tự giống nhau đứng cạnh nhau."
                )

            if result["char_types"] >= 3:
                st.success(
                    "🧩 Mật khẩu kết hợp nhiều loại ký tự."
                )
            else:
                st.warning(
                    "🧩 Nên kết hợp thêm chữ hoa, chữ thường, số "
                    "và ký tự đặc biệt."
                )

            # --------------------------------------------------
            # ENTROPY
            # --------------------------------------------------

            st.subheader("🧠 Độ khó đoán ước lượng")

            entropy = result["entropy"]

            if entropy < 40:
                muc_entropy = "Thấp"
                mau_entropy = "🔴"
            elif entropy < 60:
                muc_entropy = "Trung bình"
                mau_entropy = "🟡"
            elif entropy < 80:
                muc_entropy = "Khá tốt"
                mau_entropy = "🟢"
            else:
                muc_entropy = "Cao"
                mau_entropy = "🟢"

            st.info(
                f"{mau_entropy} Mức ước lượng: **{muc_entropy}** "
                f"({entropy:.1f} bits)"
            )

            st.caption(
                "Đây chỉ là ước lượng dựa trên độ dài và loại ký tự, "
                "không phải đánh giá bảo mật tuyệt đối."
            )

            # --------------------------------------------------
            # GỢI Ý
            # --------------------------------------------------

            st.subheader("💡 Gợi ý cải thiện")

            suggestions = []

            if len(password) < 12:
                suggestions.append(
                    "Tăng độ dài lên khoảng 12–16 ký tự hoặc hơn."
                )

            if not any(c.isupper() for c in password):
                suggestions.append("Thêm chữ cái viết hoa.")

            if not any(c.islower() for c in password):
                suggestions.append("Thêm chữ cái viết thường.")

            if not any(c.isdigit() for c in password):
                suggestions.append("Thêm chữ số.")

            if not any(c in string.punctuation for c in password):
                suggestions.append("Thêm ký tự đặc biệt.")

            if result["is_common"]:
                suggestions.append(
                    "Không sử dụng các mật khẩu phổ biến."
                )

            if suggestions:

                for suggestion in suggestions:
                    st.write(f"👉 {suggestion}")

            else:

                st.success(
                    "🎉 Không có đề xuất quan trọng nào thêm "
                    "theo các tiêu chí của ứng dụng."
                )

            st.warning(
                "🔐 Không sử dụng lại mật khẩu thật của bạn "
                "cho mục đích kiểm tra."
            )


# ==========================================================
# MỤC 2 - HƯỚNG DẪN
# ==========================================================

elif lua_chon == "📖 Hướng dẫn an toàn":

    st.header("📖 Tiêu chí để có mật khẩu an toàn")

    st.write(
        "Một mật khẩu tốt không chỉ cần nhiều ký tự. "
        "Điều quan trọng là nó phải đủ dài, khó đoán "
        "và không bị sử dụng lại ở nhiều nơi."
    )

    # --------------------------------------------------
    # TIÊU CHÍ
    # --------------------------------------------------

    with st.expander("📏 1. Sử dụng mật khẩu đủ dài", expanded=True):

        st.write(
            "Mật khẩu dài thường khó đoán hơn mật khẩu quá ngắn."
        )

        st.success(
            "💡 Nên ưu tiên mật khẩu từ 12 ký tự trở lên."
        )

    with st.expander("🔤 2. Kết hợp nhiều loại ký tự"):

        st.write(
            "Có thể kết hợp:"
        )

        st.markdown("""
        - Chữ hoa: `A B C`
        - Chữ thường: `a b c`
        - Số: `0 1 2`
        - Ký tự đặc biệt: `! @ # $ %`
        """)

    with st.expander("🚫 3. Không sử dụng thông tin dễ đoán"):

        st.markdown("""
        Không nên sử dụng:

        - Tên của bạn
        - Ngày sinh
        - Số điện thoại
        - Tên trường
        - Tên thú cưng
        - `123456`
        - `password`
        """)

    with st.expander("🔄 4. Không sử dụng lại mật khẩu"):

        st.write(
            "Mỗi tài khoản quan trọng nên có một mật khẩu riêng."
        )

        st.warning(
            "Nếu một mật khẩu bị lộ, việc dùng lại nó "
            "ở nhiều tài khoản có thể khiến các tài khoản khác "
            "cũng gặp rủi ro."
        )

    with st.expander("🤫 5. Không chia sẻ mật khẩu"):

        st.write(
            "Không gửi mật khẩu cho người khác qua tin nhắn, "
            "email hoặc đăng công khai trên mạng."
        )

    with st.expander("🛡️ 6. Bật xác thực hai yếu tố"):

        st.write(
            "Nếu dịch vụ hỗ trợ xác thực hai yếu tố (2FA/MFA), "
            "nên bật để tăng thêm lớp bảo vệ."
        )

    st.divider()

    # --------------------------------------------------
    # VÍ DỤ
    # --------------------------------------------------

    st.subheader("🔴 Một số mật khẩu dễ đoán")

    vi_du_yeu = [
        "123456",
        "12345678",
        "password",
        "qwerty",
        "abc123",
        "ngaysinh",
        "matkhau123"
    ]

    for password in vi_du_yeu:
        st.error(f"❌ `{password}`")

    st.divider()

    st.subheader("🟢 Ví dụ minh họa")

    vi_du_tot = [
        "Mau@Xanh7!P",
        "ConMeo#72Xanh",
        "T0iThich!STEM",
        "HocPython!2026"
    ]

    for password in vi_du_tot:
        st.success(f"✅ `{password}`")

    st.warning(
        "⚠️ Đây chỉ là ví dụ minh họa. "
        "Không sử dụng nguyên mẫu các mật khẩu trên "
        "cho tài khoản thật."
    )

    st.divider()

    st.info(
        "💡 Gợi ý: Với tài khoản quan trọng, bạn có thể sử dụng "
        "trình quản lý mật khẩu để tạo và lưu các mật khẩu riêng biệt."
    )


# ==========================================================
# MỤC 3 - TRẮC NGHIỆM
# ==========================================================

else:

    st.header("📝 Trắc nghiệm an toàn mật khẩu")

    st.write(
        "🎯 Hãy trả lời 10 câu hỏi để kiểm tra kiến thức!"
    )

    questions = [
        {
            "question": "Mật khẩu nào khó đoán hơn?",
            "options": [
                "12345678",
                "password",
                "01012015",
                "K8!mQ2#vL9"
            ],
            "answer": "K8!mQ2#vL9"
        },
        {
            "question": "Bạn có nên dùng cùng một mật khẩu cho tất cả tài khoản?",
            "options": [
                "Có",
                "Không"
            ],
            "answer": "Không"
        },
        {
            "question": "Thông tin nào không nên dùng làm mật khẩu?",
            "options": [
                "Một chuỗi khó đoán",
                "Tên của mình",
                "Chữ hoa và chữ thường",
                "Một mật khẩu dài"
            ],
            "answer": "Tên của mình"
        },
        {
            "question": "Ký tự nào là ký tự đặc biệt?",
            "options": [
                "A",
                "7",
                "@",
                "b"
            ],
            "answer": "@"
        },
        {
            "question": "Mật khẩu nào dễ đoán nhất?",
            "options": [
                "X7!kP9@Lm",
                "qwerty",
                "H2#vK8!pQ",
                "M9@zL4$xT"
            ],
            "answer": "qwerty"
        },
        {
            "question": "Một mật khẩu tốt nên có đặc điểm nào?",
            "options": [
                "Càng ngắn càng tốt",
                "Chỉ gồm số",
                "Dễ đoán",
                "Dài và khó đoán"
            ],
            "answer": "Dài và khó đoán"
        },
        {
            "question": "Bạn có nên công khai mật khẩu trên mạng?",
            "options": [
                "Có",
                "Không"
            ],
            "answer": "Không"
        },
        {
            "question": "Nếu người lạ hỏi mật khẩu, bạn nên làm gì?",
            "options": [
                "Đưa ngay cho họ",
                "Đăng lên mạng",
                "Không chia sẻ mật khẩu",
                "Gửi cho bạn bè"
            ],
            "answer": "Không chia sẻ mật khẩu"
        },
        {
            "question": "Điều nào giúp tài khoản an toàn hơn?",
            "options": [
                "Dùng mật khẩu giống nhau ở mọi nơi",
                "Chia sẻ mật khẩu",
                "Dùng mật khẩu khó đoán và không dùng lại",
                "Dùng tên của mình làm mật khẩu"
            ],
            "answer": "Dùng mật khẩu khó đoán và không dùng lại"
        },
        {
            "question": "Mục đích của việc tạo mật khẩu an toàn là gì?",
            "options": [
                "Làm cho việc đăng nhập khó hơn",
                "Bảo vệ tài khoản và thông tin",
                "Để khoe với bạn bè",
                "Để nhớ ngày sinh"
            ],
            "answer": "Bảo vệ tài khoản và thông tin"
        }
    ]

    answers = {}

    # --------------------------------------------------
    # HIỂN THỊ CÂU HỎI
    # --------------------------------------------------

    for i, q in enumerate(questions, start=1):

        st.subheader(f"Câu {i}/{len(questions)}")

        answers[i] = st.radio(
            q["question"],
            q["options"],
            key=f"quiz_{i}"
        )

        # Thanh tiến trình
        st.progress(i / len(questions))

    st.divider()

    # --------------------------------------------------
    # NỘP BÀI
    # --------------------------------------------------

    if st.button(
        "📝 NỘP BÀI",
        type="primary",
        use_container_width=True
    ):

        score = 0

        for i, q in enumerate(questions, start=1):

            if answers[i] == q["answer"]:
                score += 1

        st.session_state.quiz_score = score
        st.session_state.quiz_submitted = True

    # --------------------------------------------------
    # KẾT QUẢ
    # --------------------------------------------------

    if st.session_state.quiz_submitted:

        score = st.session_state.quiz_score

        st.divider()

        st.subheader("🏆 KẾT QUẢ")

        st.markdown(
            f"""
            <div class="score-box">
                <div>Điểm của bạn</div>
                <div class="score-number">
                    {score}/10
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(score / 10)

        if score == 10:

            st.balloons()

            st.success(
                "🎉 TUYỆT VỜI! Bạn đã nắm rất tốt "
                "các nguyên tắc cơ bản về an toàn mật khẩu!"
            )

        elif score >= 7:

            st.success(
                "👏 Rất tốt! Bạn đã hiểu phần lớn "
                "các nguyên tắc."
            )

        elif score >= 5:

            st.warning(
                "👍 Khá tốt! Hãy xem lại phần hướng dẫn "
                "để củng cố kiến thức."
            )

        else:

            st.error(
                "💡 Bạn nên đọc lại phần hướng dẫn "
                "và thử làm bài lần nữa."
            )

        # --------------------------------------------------
        # HIỂN THỊ ĐÁP ÁN
        # --------------------------------------------------

        st.subheader("📋 Xem lại đáp án")

        for i, q in enumerate(questions, start=1):

            if answers[i] == q["answer"]:

                st.success(
                    f"Câu {i}: ✅ Đúng"
                )

            else:

                st.error(
                    f"Câu {i}: ❌ Sai — Đáp án đúng: "
                    f"**{q['answer']}**"
                )

        st.info(
            "🔐 Hãy nhớ: mật khẩu là thông tin riêng tư. "
            "Không nên chia sẻ mật khẩu với người khác."
        )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    """
    <div class="footer">
        🔐 An toàn mật khẩu | Python + Streamlit<br>
        Hãy bảo vệ tài khoản của bạn bằng những thói quen tốt!
    </div>
    """,
    unsafe_allow_html=True
)
