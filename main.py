import streamlit as st
import os
import base64
from textwrap import dedent

st.set_page_config(
    page_title="华夏百工 | 传统手工文创与非遗文创产品",
    page_icon="◐",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =============================
# 安全渲染 HTML
# 作用：清理 HTML 内部缩进和空行，避免 Streamlit 显示黑色代码框
# =============================
def html(content):
    cleaned = "\n".join(
        line.strip()
        for line in dedent(content).splitlines()
        if line.strip()
    )
    st.markdown(cleaned, unsafe_allow_html=True)


# =============================
# 读取本地图片
# =============================
def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return None


hero_img = get_base64_image("assets/hero.jpg")
craft_img = get_base64_image("assets/craft.jpg")
magnet_img = get_base64_image("assets/magnet.jpg")
artifact_img = get_base64_image("assets/artifact.jpg")
bracelet_img = get_base64_image("assets/bracelet.jpg")


def bg_image_style(img):
    if img:
        return f'background-image: linear-gradient(135deg, rgba(2, 6, 23, 0.56), rgba(15, 23, 42, 0.18)), url("data:image/jpeg;base64,{img}");'
    return ""


def product_card(title, desc, tag, img=None):
    if img:
        img_block = f'''
        <div class="product-image" style='background-image: linear-gradient(180deg, rgba(15,23,42,0.08), rgba(15,23,42,0.18)), url("data:image/jpeg;base64,{img}");'></div>
        '''
    else:
        img_block = f'''
        <div class="product-image placeholder-image">
            <div class="placeholder-orb"></div>
            <div class="placeholder-text">{tag}</div>
        </div>
        '''

    return "\n".join(
        line.strip()
        for line in dedent(f'''
        <div class="product-card">
            {img_block}
            <div class="product-body">
                <div class="product-tag">{tag}</div>
                <div class="product-title">{title}</div>
                <div class="product-desc">{desc}</div>
            </div>
        </div>
        ''').splitlines()
        if line.strip()
    )


# =============================
# CSS
# =============================
html("""
<style>
header[data-testid="stHeader"] {
    background: transparent;
}

div[data-testid="stToolbar"] {
    visibility: hidden;
    height: 0;
    position: fixed;
}

.block-container {
    max-width: 1240px;
    padding-top: 18px;
    padding-bottom: 40px;
}

.stApp {
    background:
        radial-gradient(circle at 12% 8%, rgba(59, 130, 246, 0.16), transparent 28%),
        radial-gradient(circle at 88% 18%, rgba(168, 85, 247, 0.14), transparent 30%),
        radial-gradient(circle at 50% 92%, rgba(14, 165, 233, 0.10), transparent 34%),
        linear-gradient(180deg, #f8fafc 0%, #eef2ff 45%, #f8fafc 100%);
    color: #0f172a;
    font-family: Inter, "Microsoft YaHei", "PingFang SC", sans-serif;
}

.navbar {
    position: sticky;
    top: 12px;
    z-index: 1000;
    margin-bottom: 26px;
    padding: 14px 18px;
    border-radius: 22px;
    border: 1px solid rgba(148, 163, 184, 0.24);
    background: rgba(255, 255, 255, 0.72);
    backdrop-filter: blur(18px);
    box-shadow:
        0 18px 48px rgba(15, 23, 42, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.65);
}

.nav-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.brand-wrap {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo-mark {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    background:
        radial-gradient(circle at 30% 25%, rgba(255,255,255,0.95), transparent 24%),
        linear-gradient(135deg, #111827, #2563eb 55%, #7c3aed);
    box-shadow: 0 12px 28px rgba(37, 99, 235, 0.25);
}

.brand-name {
    font-size: 21px;
    font-weight: 850;
    letter-spacing: -0.5px;
    color: #0f172a;
}

.brand-sub {
    font-size: 12px;
    color: #64748b;
    margin-top: -1px;
}

.nav-links {
    display: flex;
    gap: 22px;
    align-items: center;
}

.nav-link {
    color: #475569;
    font-size: 14px;
    font-weight: 650;
    text-decoration: none;
}

.nav-link:hover {
    color: #2563eb;
}

.nav-actions {
    display: flex;
    gap: 10px;
    align-items: center;
}

.btn-ghost {
    padding: 9px 16px;
    border-radius: 999px;
    color: #334155;
    text-decoration: none;
    font-size: 14px;
    font-weight: 700;
}

.btn-primary {
    padding: 10px 18px;
    border-radius: 999px;
    color: white;
    text-decoration: none;
    font-size: 14px;
    font-weight: 800;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    box-shadow: 0 12px 28px rgba(37, 99, 235, 0.24);
}

.hero {
    position: relative;
    overflow: hidden;
    min-height: 640px;
    border-radius: 34px;
    border: 1px solid rgba(148, 163, 184, 0.24);
    background:
        radial-gradient(circle at 22% 18%, rgba(59,130,246,0.34), transparent 30%),
        radial-gradient(circle at 88% 16%, rgba(124,58,237,0.32), transparent 28%),
        linear-gradient(135deg, #020617 0%, #111827 50%, #172554 100%);
    box-shadow:
        0 28px 80px rgba(15, 23, 42, 0.22),
        inset 0 1px 0 rgba(255,255,255,0.10);
}

.hero.with-image {
    background-size: cover;
    background-position: center;
}

.hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background:
        linear-gradient(90deg, rgba(2,6,23,0.86), rgba(15,23,42,0.50), rgba(15,23,42,0.16)),
        radial-gradient(circle at 75% 70%, rgba(255,255,255,0.10), transparent 28%);
    z-index: 1;
}

.hero::after {
    content: "";
    position: absolute;
    width: 520px;
    height: 520px;
    right: -120px;
    bottom: -140px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(37,99,235,0.35), rgba(124,58,237,0.34));
    filter: blur(12px);
    opacity: 0.82;
    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 760px;
    padding: 86px 64px;
}

.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border-radius: 999px;
    color: #dbeafe;
    font-size: 13px;
    font-weight: 750;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.16);
    backdrop-filter: blur(12px);
}

.hero-title {
    margin-top: 22px;
    font-size: 72px;
    line-height: 1.02;
    letter-spacing: -4px;
    font-weight: 950;
    color: #ffffff;
}

.gradient-text {
    background: linear-gradient(135deg, #93c5fd, #ddd6fe, #ffffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-desc {
    margin-top: 24px;
    max-width: 680px;
    font-size: 19px;
    line-height: 1.85;
    color: rgba(226, 232, 240, 0.92);
}

.hero-buttons {
    margin-top: 34px;
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
}

.hero-button-primary {
    display: inline-block;
    padding: 14px 22px;
    border-radius: 999px;
    color: white;
    font-weight: 850;
    text-decoration: none;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    box-shadow: 0 16px 36px rgba(37,99,235,0.36);
}

.hero-button-secondary {
    display: inline-block;
    padding: 14px 22px;
    border-radius: 999px;
    color: #e2e8f0;
    font-weight: 800;
    text-decoration: none;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.18);
    backdrop-filter: blur(10px);
}

.float-card {
    position: absolute;
    z-index: 3;
    right: 42px;
    bottom: 44px;
    width: 340px;
    padding: 22px;
    border-radius: 26px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.16);
    backdrop-filter: blur(20px);
    box-shadow: 0 24px 60px rgba(0,0,0,0.20);
}

.float-title {
    color: white;
    font-size: 16px;
    font-weight: 850;
    margin-bottom: 14px;
}

.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

.metric {
    padding: 14px;
    border-radius: 18px;
    background: rgba(255,255,255,0.10);
}

.metric-num {
    color: #ffffff;
    font-size: 24px;
    font-weight: 900;
}

.metric-label {
    color: rgba(226,232,240,0.78);
    font-size: 12px;
    margin-top: 4px;
}

.section {
    margin-top: 76px;
}

.section-center {
    max-width: 780px;
    margin: 0 auto 34px auto;
    text-align: center;
}

.section-kicker {
    color: #2563eb;
    font-size: 14px;
    font-weight: 850;
    letter-spacing: 0.8px;
    margin-bottom: 10px;
}

.section-title {
    font-size: 44px;
    line-height: 1.16;
    letter-spacing: -1.8px;
    font-weight: 950;
    color: #0f172a;
}

.section-desc {
    margin-top: 14px;
    color: #64748b;
    font-size: 17px;
    line-height: 1.8;
}

.about-grid {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 22px;
}

.about-card {
    padding: 34px;
    border-radius: 30px;
    background: rgba(255,255,255,0.76);
    border: 1px solid rgba(148,163,184,0.22);
    box-shadow: 0 18px 50px rgba(15,23,42,0.08);
}

.about-card.dark {
    background:
        radial-gradient(circle at 20% 20%, rgba(59,130,246,0.22), transparent 26%),
        linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

.about-title {
    font-size: 26px;
    font-weight: 900;
    letter-spacing: -0.8px;
    margin-bottom: 14px;
}

.about-text {
    font-size: 16px;
    line-height: 1.95;
    color: #475569;
}

.about-card.dark .about-text {
    color: rgba(226,232,240,0.84);
}

.pill-row {
    margin-top: 22px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.pill {
    padding: 9px 13px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 750;
    color: #334155;
    background: #f1f5f9;
    border: 1px solid rgba(148,163,184,0.22);
}

.dark .pill {
    color: #dbeafe;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.14);
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
}

.feature-card {
    padding: 26px;
    border-radius: 26px;
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(148,163,184,0.22);
    box-shadow: 0 16px 44px rgba(15,23,42,0.07);
}

.feature-icon {
    width: 46px;
    height: 46px;
    border-radius: 16px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    box-shadow: 0 12px 26px rgba(37,99,235,0.22);
    margin-bottom: 18px;
}

.feature-title {
    font-size: 20px;
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 9px;
}

.feature-desc {
    color: #64748b;
    font-size: 15px;
    line-height: 1.8;
}

.product-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
}

.product-card {
    overflow: hidden;
    border-radius: 28px;
    background: rgba(255,255,255,0.76);
    border: 1px solid rgba(148,163,184,0.22);
    box-shadow: 0 18px 48px rgba(15,23,42,0.08);
    transition: all 0.32s ease;
}

.product-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 28px 70px rgba(15,23,42,0.13);
}

.product-image {
    height: 210px;
    background-size: cover;
    background-position: center;
}

.placeholder-image {
    position: relative;
    background:
        radial-gradient(circle at 35% 30%, rgba(59,130,246,0.32), transparent 28%),
        radial-gradient(circle at 80% 70%, rgba(124,58,237,0.28), transparent 26%),
        linear-gradient(135deg, #e0f2fe, #eef2ff, #faf5ff);
    overflow: hidden;
}

.placeholder-orb {
    position: absolute;
    width: 160px;
    height: 160px;
    right: -44px;
    top: -36px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(37,99,235,0.34), rgba(124,58,237,0.34));
    filter: blur(2px);
}

.placeholder-text {
    position: absolute;
    left: 22px;
    bottom: 20px;
    color: rgba(15,23,42,0.82);
    font-size: 34px;
    font-weight: 950;
    letter-spacing: -1.5px;
}

.product-body {
    padding: 22px;
}

.product-tag {
    display: inline-block;
    margin-bottom: 12px;
    padding: 6px 10px;
    border-radius: 999px;
    color: #2563eb;
    background: #dbeafe;
    font-size: 12px;
    font-weight: 850;
}

.product-title {
    font-size: 21px;
    font-weight: 920;
    color: #0f172a;
    margin-bottom: 9px;
}

.product-desc {
    color: #64748b;
    font-size: 14.5px;
    line-height: 1.75;
}

.cta {
    margin-top: 78px;
    padding: 56px;
    border-radius: 34px;
    text-align: center;
    color: white;
    background:
        radial-gradient(circle at 20% 20%, rgba(96,165,250,0.42), transparent 30%),
        radial-gradient(circle at 82% 72%, rgba(167,139,250,0.38), transparent 32%),
        linear-gradient(135deg, #020617, #172554 55%, #312e81);
    box-shadow: 0 28px 80px rgba(15,23,42,0.18);
}

.cta-title {
    font-size: 42px;
    line-height: 1.16;
    font-weight: 950;
    letter-spacing: -1.6px;
}

.cta-desc {
    max-width: 720px;
    margin: 16px auto 28px auto;
    color: rgba(226,232,240,0.86);
    font-size: 17px;
    line-height: 1.85;
}

.auth-panel {
    margin-top: 34px;
    padding: 26px;
    border-radius: 28px;
    background: rgba(255,255,255,0.76);
    border: 1px solid rgba(148,163,184,0.24);
    box-shadow: 0 18px 50px rgba(15,23,42,0.08);
}

.auth-title {
    font-size: 24px;
    font-weight: 920;
    letter-spacing: -0.8px;
    color: #0f172a;
    margin-bottom: 4px;
}

.auth-desc {
    color: #64748b;
    font-size: 14px;
    margin-bottom: 16px;
}

.stTextInput input {
    border-radius: 999px;
}

.stButton button {
    border-radius: 999px;
    font-weight: 800;
    border: 0;
    color: white;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
}

.footer {
    margin-top: 56px;
    padding: 28px 0 8px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #64748b;
    font-size: 14px;
    border-top: 1px solid rgba(148,163,184,0.24);
}

@media (max-width: 1100px) {
    .product-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .feature-grid {
        grid-template-columns: 1fr;
    }

    .about-grid {
        grid-template-columns: 1fr;
    }

    .float-card {
        position: relative;
        right: auto;
        bottom: auto;
        margin: 0 36px 36px 36px;
        width: auto;
    }

    .hero-content {
        padding: 62px 38px;
    }

    .hero-title {
        font-size: 52px;
    }
}

@media (max-width: 760px) {
    .nav-links {
        display: none;
    }

    .hero-title {
        font-size: 42px;
        letter-spacing: -2px;
    }

    .hero-desc {
        font-size: 16px;
    }

    .product-grid {
        grid-template-columns: 1fr;
    }

    .section-title {
        font-size: 34px;
    }

    .cta {
        padding: 38px 24px;
    }

    .footer {
        flex-direction: column;
        gap: 10px;
    }
}
</style>
""")


# =============================
# 顶部导航
# =============================
html("""
<div class="navbar">
    <div class="nav-inner">
        <div class="brand-wrap">
            <div class="logo-mark"></div>
            <div>
                <div class="brand-name">华夏百工</div>
                <div class="brand-sub">Craft Culture Studio</div>
            </div>
        </div>
        <div class="nav-links">
            <a class="nav-link" href="#about">产业介绍</a>
            <a class="nav-link" href="#features">核心价值</a>
            <a class="nav-link" href="#products">文创产品</a>
        </div>
        <div class="nav-actions">
            <a class="btn-ghost" href="#login">登录</a>
            <a class="btn-primary" href="#register">注册</a>
        </div>
    </div>
</div>
""")


# =============================
# Hero
# =============================
hero_class = "hero with-image" if hero_img else "hero"
hero_style = bg_image_style(hero_img)

html(f"""
<section class="{hero_class}" style='{hero_style}'>
    <div class="hero-content">
        <div class="eyebrow">Modern Cultural Creative Brand</div>
        <div class="hero-title">
            华夏百工<br>
            <span class="gradient-text">让传统工艺进入现代生活</span>
        </div>
        <div class="hero-desc">
            华夏百工聚焦传统手工文创与非物质文化遗产文创产品，
            以现代品牌系统、数字化展示与高品质产品设计，
            重新表达手工制品、冰箱贴、文玩、手串等东方文化生活方式。
        </div>
        <div class="hero-buttons">
            <a class="hero-button-primary" href="#products">探索产品</a>
            <a class="hero-button-secondary" href="#about">了解产业</a>
        </div>
    </div>
    <div class="float-card">
        <div class="float-title">品牌内容结构</div>
        <div class="metric-grid">
            <div class="metric">
                <div class="metric-num">04</div>
                <div class="metric-label">核心产品类型</div>
            </div>
            <div class="metric">
                <div class="metric-num">03</div>
                <div class="metric-label">官网展示板块</div>
            </div>
            <div class="metric">
                <div class="metric-num">100%</div>
                <div class="metric-label">非购买型展示</div>
            </div>
            <div class="metric">
                <div class="metric-num">Pro</div>
                <div class="metric-label">高级品牌视觉</div>
            </div>
        </div>
    </div>
</section>
""")


# =============================
# 产业介绍
# =============================
html("""
<section class="section" id="about">
    <div class="section-center">
        <div class="section-kicker">INDUSTRY OVERVIEW</div>
        <div class="section-title">一个面向现代生活方式的传统文创品牌</div>
        <div class="section-desc">
            保留文化内核，弱化传统装饰感，以更干净、更国际化、更高级的方式呈现华夏百工。
        </div>
    </div>
</section>
""")

html("""
<div class="about-grid">
    <div class="about-card">
        <div class="about-title">品牌定位</div>
        <div class="about-text">
            华夏百工是一个围绕传统手工文创与非物质文化遗产文创产品展开的文化创意品牌。
            它不只是展示传统工艺本身，而是将工艺、材料、故事与现代审美重新整合，
            让传统文化以更轻盈、更高级、更适合当代用户的方式被看见。
        </div>
        <div class="pill-row">
            <span class="pill">传统手工文创</span>
            <span class="pill">非遗衍生产品</span>
            <span class="pill">现代品牌展示</span>
        </div>
    </div>
    <div class="about-card dark">
        <div class="about-title">视觉方向</div>
        <div class="about-text">
            本页面参考现代官网模板的结构逻辑：大 Hero 首屏、清晰的信息层级、
            高级渐变背景、玻璃拟态导航、模块化卡片和强烈的 CTA 区域。
            整体不使用中国风纹样，而是通过文字与产品内容体现“华夏百工”的文化主题。
        </div>
        <div class="pill-row">
            <span class="pill">Minimal</span>
            <span class="pill">Premium</span>
            <span class="pill">SaaS-style Layout</span>
        </div>
    </div>
</div>
""")


# =============================
# 核心价值
# =============================
html("""
<section class="section" id="features">
    <div class="section-center">
        <div class="section-kicker">CORE VALUE</div>
        <div class="section-title">从传统工艺到现代文创系统</div>
        <div class="section-desc">
            以更接近品牌官网的表达方式，突出产业、产品和文化价值。
        </div>
    </div>
</section>
""")

html("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon"></div>
        <div class="feature-title">文化内容产品化</div>
        <div class="feature-desc">
            将非遗故事、传统工艺、地域符号转化为可以展示、收藏、佩戴和使用的文创产品。
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon"></div>
        <div class="feature-title">现代视觉系统</div>
        <div class="feature-desc">
            通过高级渐变、卡片布局、品牌化字体层级和数字官网结构，让传统主题更年轻化。
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon"></div>
        <div class="feature-title">非购买型展示</div>
        <div class="feature-desc">
            页面不设置购买链接，而是作为产业介绍、产品展示和品牌形象呈现的官网首页。
        </div>
    </div>
</div>
""")


# =============================
# 文创产品
# =============================
html("""
<section class="section" id="products">
    <div class="section-center">
        <div class="section-kicker">PRODUCT SYSTEM</div>
        <div class="section-title">文创产品矩阵</div>
        <div class="section-desc">
            以四类产品构成华夏百工的核心展示内容：手工制品、冰箱贴、文玩、手串。
        </div>
    </div>
</section>
""")

html(f"""
<div class="product-grid">
    {product_card(
        "手工制品",
        "融合传统工艺、材料质感与现代生活审美，强调手作温度与独特性。",
        "Handcraft",
        craft_img
    )}
    {product_card(
        "冰箱贴",
        "将文化符号、地方记忆与视觉设计浓缩为轻量化、易传播的文创物件。",
        "Magnet",
        magnet_img
    )}
    {product_card(
        "文玩",
        "面向赏玩、陈设与收藏场景，呈现器物背后的审美、质感与文化叙事。",
        "Artifact",
        artifact_img
    )}
    {product_card(
        "手串",
        "结合传统材质与现代佩戴方式，形成兼具装饰性与文化意味的随身文创。",
        "Bracelet",
        bracelet_img
    )}
</div>
""")


# =============================
# CTA
# =============================
html("""
<section class="cta">
    <div class="cta-title">以现代官网语言，重新展示传统文创产业</div>
    <div class="cta-desc">
        华夏百工不只是一个产品展示页面，而是一个可以继续扩展为完整品牌官网的基础框架。
        后续可以继续加入品牌故事、产品详情页、非遗专题、新闻动态和会员系统。
    </div>
    <a class="hero-button-primary" href="#register">创建账户</a>
</section>
""")


# =============================
# 登录注册区域
# =============================
html("""
<section class="section" id="login">
    <div class="section-center">
        <div class="section-kicker">ACCOUNT</div>
        <div class="section-title">登录 / 注册</div>
        <div class="section-desc">
            这里目前是前端展示型表单，可以后续接入数据库、用户系统或后台管理功能。
        </div>
    </div>
</section>
""")

left_auth, right_auth = st.columns(2, gap="large")

with left_auth:
    html("""
    <div class="auth-panel">
        <div class="auth-title">用户登录</div>
        <div class="auth-desc">进入华夏百工的会员展示系统。</div>
    </div>
    """)

    st.text_input("登录用户名", placeholder="请输入用户名", key="login_user")
    st.text_input("登录密码", placeholder="请输入密码", type="password", key="login_password")
    st.button("登录", use_container_width=True)

with right_auth:
    html("""
    <div class="auth-panel" id="register">
        <div class="auth-title">用户注册</div>
        <div class="auth-desc">创建账户以体验后续扩展功能。</div>
    </div>
    """)

    st.text_input("注册用户名", placeholder="设置用户名", key="register_user")
    st.text_input("注册密码", placeholder="设置密码", type="password", key="register_password")
    st.text_input("确认密码", placeholder="再次输入密码", type="password", key="register_password_confirm")
    st.button("注册", use_container_width=True)


# =============================
# Footer
# =============================
html("""
<footer class="footer">
    <div>© 2026 华夏百工 · Traditional Craft Cultural Creative Studio</div>
    <div>Handcraft · Magnet · Artifact · Bracelet</div>
</footer>
""")