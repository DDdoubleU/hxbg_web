import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
# 图片路径建议：
# assets/hero.jpg
# assets/craft.jpg
# assets/magnet.jpg
# assets/artifact.jpg
# assets/bracelet.jpg
# assets/workshop.jpg
# assets/gallery1.jpg / gallery2.jpg / gallery3.jpg
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
workshop_img = get_base64_image("assets/workshop.jpg")
gallery_img_1 = get_base64_image("assets/gallery1.jpg")
gallery_img_2 = get_base64_image("assets/gallery2.jpg")
gallery_img_3 = get_base64_image("assets/gallery3.jpg")


PRODUCTS = [
    {
        "slug": "handcraft",
        "title": "手工制品",
        "tag": "Handcraft",
        "image": craft_img,
        "desc": "融合传统工艺、材料质感与现代生活审美，强调手作温度与独特性。",
        "long_desc": "手工制品板块适合展示木作、漆器、陶器、织物、纸艺等传统技艺。后续可以继续加入工艺来源、匠人故事、制作步骤、材料说明与作品图库。",
        "keywords": ["手作温度", "材料质感", "工艺故事", "生活美学"],
    },
    {
        "slug": "magnet",
        "title": "冰箱贴",
        "tag": "Magnet",
        "image": magnet_img,
        "desc": "将文化符号、地方记忆与视觉设计浓缩为轻量化、易传播的文创物件。",
        "long_desc": "冰箱贴适合作为城市文化、非遗符号与旅游纪念的轻量化载体。后续可以做成系列化专题，例如节气系列、城市系列、博物馆系列。",
        "keywords": ["轻量传播", "城市记忆", "符号提炼", "礼品场景"],
    },
    {
        "slug": "artifact",
        "title": "文玩",
        "tag": "Artifact",
        "image": artifact_img,
        "desc": "面向赏玩、陈设与收藏场景，呈现器物背后的审美、质感与文化叙事。",
        "long_desc": "文玩板块适合展示器物美学、收藏文化与东方生活方式。后续可以加入材质百科、保养知识、作品档案与文化解读。",
        "keywords": ["器物审美", "陈设收藏", "材质百科", "东方生活"],
    },
    {
        "slug": "bracelet",
        "title": "手串",
        "tag": "Bracelet",
        "image": bracelet_img,
        "desc": "结合传统材质与现代佩戴方式，形成兼具装饰性与文化意味的随身文创。",
        "long_desc": "手串板块适合展示材质、搭配、佩戴场景与文化寓意。后续可以扩展为材质筛选、风格推荐与搭配指南。",
        "keywords": ["随身文创", "材质搭配", "佩戴场景", "东方配饰"],
    },
]


# =============================
# 页面路由：现在用 query 参数模拟“新页面”
# 链接格式：?page=about / ?page=handcraft
# 将来如果想改成 Streamlit pages/ 多页面，只需要把这些 render_xxx 函数拆到 pages 文件夹。
# =============================
def get_page():
    try:
        page = st.query_params.get("page", "home")
        if isinstance(page, list):
            page = page[0]
    except Exception:
        params = st.experimental_get_query_params()
        page = params.get("page", ["home"])[0]
    return page or "home"


current_page = get_page()


def is_active(page_name):
    return "active" if current_page == page_name else ""


def page_url(page_name):
    return f"?page={page_name}"


def image_bg(img, overlay="linear-gradient(135deg, rgba(2,6,23,0.62), rgba(15,23,42,0.20))"):
    if img:
        return f'background-image: {overlay}, url("data:image/jpeg;base64,{img}");'
    return ""


def chips(items, dark=False):
    chip_class = "pill dark-pill" if dark else "pill"
    return "".join([f'<span class="{chip_class}">{item}</span>' for item in items])


def product_card(product):
    img = product["image"]
    if img:
        img_block = f'''
        <div class="product-image" style='background-image: linear-gradient(180deg, rgba(15,23,42,0.05), rgba(15,23,42,0.22)), url("data:image/jpeg;base64,{img}");'></div>
        '''
    else:
        img_block = f'''
        <div class="product-image placeholder-image">
            <div class="placeholder-orb"></div>
            <div class="placeholder-text">{product["tag"]}</div>
        </div>
        '''

    return "\n".join(
        line.strip()
        for line in dedent(f'''
        <a class="product-card reveal" href="{page_url(product["slug"])}" target="_self">
            {img_block}
            <div class="product-body">
                <div class="product-tag">{product["tag"]}</div>
                <div class="product-title">{product["title"]}</div>
                <div class="product-desc">{product["desc"]}</div>
                <div class="card-link">查看详情 →</div>
            </div>
        </a>
        ''').splitlines()
        if line.strip()
    )


def gallery_tile(title, desc, img=None, tall=False):
    tile_class = "gallery-tile tall" if tall else "gallery-tile"
    style = image_bg(img, "linear-gradient(180deg, rgba(2,6,23,0.10), rgba(2,6,23,0.72))") if img else ""
    placeholder = "" if img else '<div class="gallery-pattern"></div>'
    return f'''
    <div class="{tile_class}" style='{style}'>
        {placeholder}
        <div class="gallery-caption">
            <div class="gallery-title">{title}</div>
            <div class="gallery-desc">{desc}</div>
        </div>
    </div>
    '''


# =============================
# 全局 CSS：新增动画、流光、悬浮、详情页样式
# =============================
html("""
<style>
:root {
    --ink: #0f172a;
    --muted: #64748b;
    --blue: #2563eb;
    --purple: #7c3aed;
    --panel: rgba(255,255,255,0.76);
    --line: rgba(148,163,184,0.24);
    --shadow: 0 18px 50px rgba(15,23,42,0.08);
}

html {
    scroll-behavior: smooth;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer, div[data-testid="stToolbar"] {
    visibility: hidden;
    height: 0;
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
    color: var(--ink);
    font-family: Inter, "Microsoft YaHei", "PingFang SC", sans-serif;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes floatSoft {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-12px); }
}

@keyframes pulseGlow {
    0%, 100% { opacity: .58; transform: scale(1); }
    50% { opacity: .92; transform: scale(1.04); }
}

@keyframes marquee {
    from { transform: translateX(0); }
    to { transform: translateX(-50%); }
}

@keyframes shine {
    0% { transform: translateX(-120%); }
    100% { transform: translateX(120%); }
}

.reveal {
    animation: fadeUp .72s ease both;
}

.navbar {
    position: sticky;
    top: 12px;
    z-index: 1000;
    margin-bottom: 26px;
    padding: 14px 18px;
    border-radius: 22px;
    border: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.74);
    backdrop-filter: blur(18px);
    box-shadow:
        0 18px 48px rgba(15, 23, 42, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.65);
}

.nav-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 18px;
}

.brand-wrap {
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
}

.logo-mark {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    background:
        radial-gradient(circle at 30% 25%, rgba(255,255,255,0.95), transparent 24%),
        linear-gradient(135deg, #111827, #2563eb 55%, #7c3aed);
    box-shadow: 0 12px 28px rgba(37, 99, 235, 0.25);
    animation: pulseGlow 4.4s ease-in-out infinite;
}

.brand-name {
    font-size: 21px;
    font-weight: 850;
    letter-spacing: -0.5px;
    color: var(--ink);
}

.brand-sub {
    font-size: 12px;
    color: var(--muted);
    margin-top: -1px;
}

.nav-links {
    display: flex;
    gap: 18px;
    align-items: center;
    flex-wrap: wrap;
    justify-content: center;
}

.nav-link {
    color: #475569;
    font-size: 14px;
    font-weight: 700;
    text-decoration: none;
    padding: 8px 10px;
    border-radius: 999px;
    transition: all .24s ease;
}

.nav-link:hover, .nav-link.active {
    color: #1d4ed8;
    background: rgba(37,99,235,.09);
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
    font-weight: 750;
}

.btn-primary, .hero-button-primary {
    position: relative;
    overflow: hidden;
    display: inline-block;
    padding: 10px 18px;
    border-radius: 999px;
    color: white !important;
    text-decoration: none;
    font-size: 14px;
    font-weight: 850;
    background: linear-gradient(135deg, var(--blue), var(--purple));
    box-shadow: 0 12px 28px rgba(37, 99, 235, 0.24);
}

.btn-primary::after, .hero-button-primary::after {
    content: "";
    position: absolute;
    inset: 0;
    width: 55%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.32), transparent);
    transform: translateX(-120%);
}

.btn-primary:hover::after, .hero-button-primary:hover::after {
    animation: shine .75s ease;
}

.hero {
    position: relative;
    overflow: hidden;
    min-height: 660px;
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
        linear-gradient(90deg, rgba(2,6,23,0.88), rgba(15,23,42,0.52), rgba(15,23,42,0.16)),
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
    animation: pulseGlow 6s ease-in-out infinite;
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 760px;
    padding: 86px 64px;
    animation: fadeUp .78s ease both;
}

.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border-radius: 999px;
    color: #dbeafe;
    font-size: 13px;
    font-weight: 760;
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
    padding: 14px 22px;
}

.hero-button-secondary {
    display: inline-block;
    padding: 14px 22px;
    border-radius: 999px;
    color: #e2e8f0 !important;
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
    width: 360px;
    padding: 22px;
    border-radius: 26px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.16);
    backdrop-filter: blur(20px);
    box-shadow: 0 24px 60px rgba(0,0,0,0.20);
    animation: floatSoft 5.4s ease-in-out infinite;
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

.marquee-wrap {
    margin-top: 24px;
    overflow: hidden;
    border-radius: 22px;
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(12px);
}

.marquee-track {
    display: flex;
    gap: 34px;
    width: max-content;
    padding: 14px 0;
    animation: marquee 24s linear infinite;
}

.marquee-item {
    color: #334155;
    font-size: 13px;
    font-weight: 850;
    white-space: nowrap;
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
    color: var(--blue);
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
    color: var(--ink);
}

.section-desc {
    margin-top: 14px;
    color: var(--muted);
    font-size: 17px;
    line-height: 1.8;
}

.about-grid, .story-grid, .detail-grid {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 22px;
}

.about-card, .stat-card, .timeline-card, .detail-card, .chart-card {
    padding: 34px;
    border-radius: 30px;
    background: var(--panel);
    border: 1px solid rgba(148,163,184,0.22);
    box-shadow: var(--shadow);
}

.about-card.dark, .detail-card.dark {
    background:
        radial-gradient(circle at 20% 20%, rgba(59,130,246,0.22), transparent 26%),
        linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

.about-title, .detail-title {
    font-size: 26px;
    font-weight: 920;
    letter-spacing: -0.8px;
    margin-bottom: 14px;
}

.about-text, .detail-text {
    font-size: 16px;
    line-height: 1.95;
    color: #475569;
}

.dark .about-text, .dark .detail-text {
    color: rgba(226,232,240,0.84);
}

.pill-row {
    margin-top: 22px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.pill {
    display: inline-flex;
    padding: 9px 13px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 760;
    color: #334155;
    background: #f1f5f9;
    border: 1px solid rgba(148,163,184,0.22);
}

.dark-pill, .dark .pill {
    color: #dbeafe;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.14);
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
}

.feature-card, .link-card {
    position: relative;
    overflow: hidden;
    display: block;
    padding: 26px;
    border-radius: 26px;
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(148,163,184,0.22);
    box-shadow: 0 16px 44px rgba(15,23,42,0.07);
    text-decoration: none;
    transition: transform .28s ease, box-shadow .28s ease;
}

.feature-card:hover, .link-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 24px 60px rgba(15,23,42,0.12);
}

.feature-icon {
    width: 46px;
    height: 46px;
    border-radius: 16px;
    background: linear-gradient(135deg, var(--blue), var(--purple));
    box-shadow: 0 12px 26px rgba(37,99,235,0.22);
    margin-bottom: 18px;
}

.feature-title, .link-title {
    font-size: 20px;
    font-weight: 920;
    color: var(--ink);
    margin-bottom: 9px;
}

.feature-desc, .link-desc {
    color: var(--muted);
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
    display: block;
    text-decoration: none;
    border-radius: 28px;
    background: rgba(255,255,255,0.76);
    border: 1px solid rgba(148,163,184,0.22);
    box-shadow: 0 18px 48px rgba(15,23,42,0.08);
    transition: all 0.32s ease;
}

.product-card:hover {
    transform: translateY(-8px) scale(1.01);
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
    color: var(--blue);
    background: #dbeafe;
    font-size: 12px;
    font-weight: 850;
}

.product-title {
    font-size: 21px;
    font-weight: 920;
    color: var(--ink);
    margin-bottom: 9px;
}

.product-desc {
    color: var(--muted);
    font-size: 14.5px;
    line-height: 1.75;
}

.card-link {
    margin-top: 16px;
    color: var(--blue);
    font-size: 14px;
    font-weight: 850;
}

.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

.stat-card {
    padding: 24px;
}

.stat-num {
    font-size: 34px;
    font-weight: 950;
    letter-spacing: -1.2px;
    color: var(--ink);
}

.stat-label {
    margin-top: 8px;
    color: var(--muted);
    font-size: 14px;
    line-height: 1.6;
}

.timeline {
    position: relative;
    display: grid;
    gap: 16px;
}

.timeline-item {
    position: relative;
    padding-left: 44px;
}

.timeline-item::before {
    content: attr(data-step);
    position: absolute;
    left: 0;
    top: 0;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    color: white;
    font-size: 12px;
    font-weight: 900;
    background: linear-gradient(135deg, var(--blue), var(--purple));
}

.timeline-title {
    font-size: 18px;
    font-weight: 900;
    color: var(--ink);
}

.timeline-desc {
    margin-top: 6px;
    color: var(--muted);
    line-height: 1.75;
    font-size: 14.5px;
}

.gallery-grid {
    display: grid;
    grid-template-columns: 1.2fr .8fr .8fr;
    gap: 18px;
}

.gallery-tile {
    position: relative;
    min-height: 270px;
    border-radius: 30px;
    overflow: hidden;
    background:
        radial-gradient(circle at 25% 25%, rgba(59,130,246,.30), transparent 28%),
        radial-gradient(circle at 75% 70%, rgba(124,58,237,.28), transparent 30%),
        linear-gradient(135deg, #111827, #1e293b);
    background-size: cover;
    background-position: center;
    box-shadow: 0 22px 58px rgba(15,23,42,.16);
}

.gallery-tile.tall {
    min-height: 360px;
}

.gallery-pattern {
    position: absolute;
    inset: 0;
    opacity: .7;
    background-image:
        linear-gradient(rgba(255,255,255,.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.06) 1px, transparent 1px);
    background-size: 34px 34px;
}

.gallery-caption {
    position: absolute;
    left: 24px;
    right: 24px;
    bottom: 24px;
    z-index: 1;
}

.gallery-title {
    color: white;
    font-size: 22px;
    font-weight: 920;
    margin-bottom: 8px;
}

.gallery-desc {
    color: rgba(226,232,240,.82);
    font-size: 14px;
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
    margin-top: 10px;
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
    color: var(--ink);
    margin-bottom: 4px;
}

.auth-desc {
    color: var(--muted);
    font-size: 14px;
    margin-bottom: 16px;
}

.stTextInput input {
    border-radius: 999px;
}

.stButton button {
    border-radius: 999px;
    font-weight: 850;
    border: 0;
    color: white;
    background: linear-gradient(135deg, var(--blue), var(--purple));
}

.page-hero {
    position: relative;
    overflow: hidden;
    min-height: 440px;
    border-radius: 34px;
    border: 1px solid rgba(148,163,184,.22);
    background:
        radial-gradient(circle at 18% 20%, rgba(59,130,246,.28), transparent 32%),
        radial-gradient(circle at 85% 40%, rgba(124,58,237,.28), transparent 30%),
        linear-gradient(135deg, #020617, #172554 58%, #312e81);
    background-size: cover;
    background-position: center;
    box-shadow: 0 28px 80px rgba(15,23,42,.18);
}

.page-hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, rgba(2,6,23,.84), rgba(15,23,42,.34));
}

.page-content {
    position: relative;
    z-index: 2;
    max-width: 780px;
    padding: 68px 56px;
}

.back-link {
    display: inline-flex;
    color: #dbeafe !important;
    text-decoration: none;
    font-weight: 850;
    margin-bottom: 22px;
}

.page-title {
    font-size: 58px;
    line-height: 1.05;
    letter-spacing: -2.8px;
    color: white;
    font-weight: 950;
}

.page-desc {
    margin-top: 18px;
    color: rgba(226,232,240,.88);
    font-size: 18px;
    line-height: 1.85;
}

.template-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}

.template-card {
    padding: 24px;
    border-radius: 24px;
    background: rgba(255,255,255,.74);
    border: 1px solid rgba(148,163,184,.22);
    box-shadow: var(--shadow);
}

.template-title {
    font-size: 18px;
    font-weight: 900;
    color: var(--ink);
    margin-bottom: 8px;
}

.template-desc {
    color: var(--muted);
    line-height: 1.75;
    font-size: 14px;
}

.footer-custom {
    margin-top: 56px;
    padding: 28px 0 8px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: var(--muted);
    font-size: 14px;
    border-top: 1px solid rgba(148,163,184,0.24);
}

@media (max-width: 1100px) {
    .product-grid, .stat-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .feature-grid, .about-grid, .story-grid, .detail-grid, .template-grid, .gallery-grid {
        grid-template-columns: 1fr;
    }
    .float-card {
        position: relative;
        right: auto;
        bottom: auto;
        margin: 0 36px 36px 36px;
        width: auto;
    }
    .hero-content, .page-content {
        padding: 62px 38px;
    }
    .hero-title, .page-title {
        font-size: 52px;
    }
}

@media (max-width: 760px) {
    .nav-links {
        display: none;
    }
    .hero-title, .page-title {
        font-size: 42px;
        letter-spacing: -2px;
    }
    .hero-desc, .page-desc {
        font-size: 16px;
    }
    .product-grid, .stat-grid {
        grid-template-columns: 1fr;
    }
    .section-title {
        font-size: 34px;
    }
    .cta {
        padding: 38px 24px;
    }
    .footer-custom {
        flex-direction: column;
        gap: 10px;
    }
}
</style>
""")


# =============================
# 顶部导航
# =============================
def render_nav():
    html(f"""
    <div class="navbar">
        <div class="nav-inner">
            <a class="brand-wrap" href="{page_url('home')}" target="_self">
                <div class="logo-mark"></div>
                <div>
                    <div class="brand-name">华夏百工</div>
                    <div class="brand-sub">Craft Culture Studio</div>
                </div>
            </a>
            <div class="nav-links">
                <a class="nav-link {is_active('about')}" href="{page_url('about')}" target="_self">产业介绍</a>
                <a class="nav-link {is_active('features')}" href="{page_url('features')}" target="_self">核心价值</a>
                <a class="nav-link {is_active('products')}" href="{page_url('products')}" target="_self">文创产品</a>
                <a class="nav-link {is_active('stories')}" href="{page_url('stories')}" target="_self">非遗专题</a>
            </div>
            <div class="nav-actions">
                <a class="btn-ghost" href="{page_url('login')}" target="_self">登录</a>
                <a class="btn-primary" href="{page_url('login')}" target="_self">注册</a>
            </div>
        </div>
    </div>
    """)


# =============================
# 首页模块
# =============================
def render_hero():
    hero_class = "hero with-image" if hero_img else "hero"
    hero_style = image_bg(hero_img)
    html(f"""
    <section class="{hero_class}" style='{hero_style}'>
        <div class="hero-content">
            <div class="eyebrow">Modern Cultural Creative Brand · 非购买型展示官网</div>
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
                <a class="hero-button-primary" href="{page_url('products')}" target="_self">探索产品矩阵</a>
                <a class="hero-button-secondary" href="{page_url('stories')}" target="_self">进入非遗专题</a>
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
                    <div class="metric-num">06</div>
                    <div class="metric-label">可扩展内容页</div>
                </div>
                <div class="metric">
                    <div class="metric-num">100%</div>
                    <div class="metric-label">手工制作</div>
                </div>
                <div class="metric">
                    <div class="metric-num">Pro</div>
                    <div class="metric-label">高级品牌视觉</div>
                </div>
            </div>
        </div>
    </section>
    <div class="marquee-wrap">
        <div class="marquee-track">
            <span class="marquee-item">传统手工文创</span>
            <span class="marquee-item">非遗文化产品</span>
            <span class="marquee-item">城市记忆礼品</span>
            <span class="marquee-item">东方生活方式</span>
            <span class="marquee-item">品牌展示系统</span>
            <span class="marquee-item">手工制品 · 冰箱贴 · 文玩 · 手串</span>
            <span class="marquee-item">传统手工文创</span>
            <span class="marquee-item">非遗文化产品</span>
            <span class="marquee-item">城市记忆礼品</span>
            <span class="marquee-item">东方生活方式</span>
            <span class="marquee-item">品牌展示系统</span>
            <span class="marquee-item">手工制品 · 冰箱贴 · 文玩 · 手串</span>
        </div>
    </div>
    """)


def render_about_section():
    html("""
    <section class="section" id="about">
        <div class="section-center reveal">
            <div class="section-kicker">INDUSTRY OVERVIEW</div>
            <div class="section-title">一个面向现代生活方式的传统文创品牌</div>
            <div class="section-desc">
                保留文化内核，弱化传统装饰感，以更干净、更国际化、更高级的方式呈现华夏百工。
            </div>
        </div>
    </section>
    <div class="about-grid">
        <div class="about-card reveal">
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
        <div class="about-card dark reveal">
            <div class="about-title">视觉方向</div>
            <div class="about-text">
                将现代视觉语言与传统文化结合
            </div>
            <div class="about-text">
                打造全新的文创收藏品
            </div>
            <div class="pill-row">
                <span class="pill">Minimal</span>
                <span class="pill">Premium</span>
                <span class="pill">Expandable Pages</span>
            </div>
        </div>
    </div>
    """)


def render_stats_section():
    html("""
    <section class="section">
        <div class="section-center reveal">
            <div class="section-kicker">BRAND DASHBOARD</div>
            <div class="section-title">用数据感增强官网的现代感</div>
            <div class="section-desc">
                这些数字现在是展示型内容，以后可以接入真实后台数据、用户系统或产品数据库。
            </div>
        </div>
    </section>
    <div class="stat-grid">
        <div class="stat-card reveal">
            <div class="stat-num">12+</div>
            <div class="stat-label">可扩展的非遗专题方向，例如陶、木、织、漆、纸、金工。</div>
        </div>
        <div class="stat-card reveal">
            <div class="stat-num">4</div>
            <div class="stat-label">核心产品矩阵：手工制品、冰箱贴、文玩、手串。</div>
        </div>
        <div class="stat-card reveal">
            <div class="stat-num">8</div>
            <div class="stat-label">未来可添加的详情页：故事、工艺、图库、新闻、会员、后台。</div>
        </div>
        <div class="stat-card reveal">
            <div class="stat-num">0</div>
            <div class="stat-label">当前不设置购买链接，更适合作为展示型品牌官网。</div>
        </div>
    </div>
    """)


def render_chart_section():
    html("""
    <section class="section">
        <div class="section-center reveal">
            <div class="section-kicker">CONTENT TREND</div>
            <div class="section-title">内容展示趋势示例</div>
            <div class="section-desc">
                这里示范使用 pandas、numpy、matplotlib 生成图表，让页面不仅有静态介绍，也能放数据内容。
            </div>
        </div>
    </section>
    """)

    months = pd.date_range("2026-01-01", periods=6, freq="M").strftime("%m月")
    x = np.arange(len(months))
    df = pd.DataFrame({
        "月份": months,
        "手工制品": 36 + np.array([0, 8, 14, 18, 26, 34]),
        "冰箱贴": 22 + np.array([4, 12, 16, 28, 33, 45]),
        "文玩": 18 + np.array([2, 8, 13, 17, 24, 30]),
        "手串": 28 + np.array([6, 10, 16, 22, 31, 38]),
    })

    chart_col, text_col = st.columns([1.28, 0.72], gap="large")

    with chart_col:
        html('<div class="chart-card reveal"><div class="about-title">产品内容热度模拟</div><div class="about-text">这是展示用趋势图。之后你可以把它替换为真实访问量、收藏量、浏览量或产品数据。</div></div>')
        fig, ax = plt.subplots(figsize=(9, 4.8))
        for column in ["手工制品", "冰箱贴", "文玩", "手串"]:
            ax.plot(x, df[column], marker="o", linewidth=2.5, label=column)
        ax.set_xticks(x)
        ax.set_xticklabels(df["月份"])
        ax.set_ylabel("展示热度")
        ax.set_title("华夏百工内容展示趋势")
        ax.grid(alpha=0.18)
        ax.legend(frameon=False, ncol=4, loc="upper left")
        fig.patch.set_alpha(0)
        st.pyplot(fig, use_container_width=True)

    with text_col:
        html("""
        <div class="about-card dark reveal">
            <div class="about-title">后续可接入的数据</div>
            <div class="about-text">
                你可以把这里扩展为真实后台：产品浏览量、用户收藏、专题点击量、注册人数、
                不同品类的内容热度，甚至用 pandas 读取 CSV 后自动生成图表。
            </div>
            <div class="pill-row">
                <span class="pill">pandas</span>
                <span class="pill">numpy</span>
                <span class="pill">matplotlib</span>
            </div>
        </div>
        """)


def render_features_section():
    html("""
    <section class="section" id="features">
        <div class="section-center reveal">
            <div class="section-kicker">CORE VALUE</div>
            <div class="section-title">从传统工艺到现代文创系统</div>
            <div class="section-desc">
                以更接近品牌官网的表达方式，突出产业、产品、专题与文化价值。
            </div>
        </div>
    </section>
    <div class="feature-grid">
        <a class="feature-card reveal" href="?page=stories" target="_self">
            <div class="feature-icon"></div>
            <div class="feature-title">文化内容产品化</div>
            <div class="feature-desc">
                将非遗故事、传统工艺、地域符号转化为可以展示、收藏、佩戴和使用的文创产品。
            </div>
            <div class="card-link">查看专题 →</div>
        </a>
        <a class="feature-card reveal" href="?page=features" target="_self">
            <div class="feature-icon"></div>
            <div class="feature-title">现代视觉系统</div>
            <div class="feature-desc">
                通过高级渐变、卡片布局、品牌化字体层级和数字官网结构，让传统主题更年轻化。
            </div>
            <div class="card-link">查看价值页 →</div>
        </a>
        <a class="feature-card reveal" href="?page=login" target="_self">
            <div class="feature-icon"></div>
            <div class="feature-title">会员系统预留</div>
            <div class="feature-desc">
                页面现在是展示型登录注册，以后可以接数据库、用户权限、收藏夹和后台管理。
            </div>
            <div class="card-link">进入账户页 →</div>
        </a>
    </div>
    """)


def render_products_section():
    cards = "\n".join([product_card(item) for item in PRODUCTS])
    html(f"""
    <section class="section" id="products">
        <div class="section-center reveal">
            <div class="section-kicker">PRODUCT SYSTEM</div>
            <div class="section-title">文创产品矩阵</div>
            <div class="section-desc">
                点击任意卡片即可进入对应的详情页视图。之后你可以把这些视图拆成真正的 Streamlit 多页面文件。
            </div>
        </div>
    </section>
    <div class="product-grid">
        {cards}
    </div>
    """)


def render_story_section():
    html(f"""
    <section class="section">
        <div class="section-center reveal">
            <div class="section-kicker">CRAFT JOURNEY</div>
            <div class="section-title">从一项技艺，到一个可浏览的品牌故事</div>
            <div class="section-desc">
                增加故事线后，页面会更像真正的品牌官网，而不是单纯的静态展示页。
            </div>
        </div>
    </section>
    <div class="story-grid">
        <div class="timeline-card reveal">
            <div class="about-title">内容生产流程</div>
            <div class="timeline">
                <div class="timeline-item" data-step="1">
                    <div class="timeline-title">采集工艺故事</div>
                    <div class="timeline-desc">记录工艺来源、匠人背景、地域文化与材料特征。</div>
                </div>
                <div class="timeline-item" data-step="2">
                    <div class="timeline-title">转化视觉符号</div>
                    <div class="timeline-desc">将纹样、器型、色彩、结构转化为可用于网页与产品的视觉系统。</div>
                </div>
                <div class="timeline-item" data-step="3">
                    <div class="timeline-title">形成产品矩阵</div>
                    <div class="timeline-desc">根据使用场景拆分为手工制品、冰箱贴、文玩、手串等内容板块。</div>
                </div>
                <div class="timeline-item" data-step="4">
                    <div class="timeline-title">沉淀为专题页面</div>
                    <div class="timeline-desc">每个产品、工艺或故事都可以拥有单独详情页。</div>
                </div>
            </div>
        </div>
        <div class="about-card dark reveal" style='{image_bg(workshop_img)}'>
            <div class="about-title">非遗专题入口</div>
            <div class="about-text">
                这个区域可以继续扩展成“非遗百科”“匠人访谈”“工艺流程”“地方文化地图”等内容，
                很适合作为你后续每个详情页的入口。
            </div>
            <div class="pill-row">
                <span class="pill">专题页面</span>
                <span class="pill">故事内容</span>
                <span class="pill">工艺流程</span>
            </div>
        </div>
    </div>
    """)


def render_gallery_section():
    html(f"""
    <section class="section">
        <div class="section-center reveal">
            <div class="section-kicker">VISUAL GALLERY</div>
            <div class="section-title">图片展示区域</div>
            <div class="section-desc">
                你可以把 assets/gallery1.jpg、gallery2.jpg、gallery3.jpg 替换成自己的图片。
            </div>
        </div>
    </section>
    <div class="gallery-grid">
        {gallery_tile("匠作现场", "展示工艺过程、材料与手作细节。", gallery_img_1, tall=True)}
        {gallery_tile("产品陈设", "适合放置文玩、器物、手串等静物图。", gallery_img_2)}
        {gallery_tile("文化符号", "适合放置冰箱贴、纹样、地域视觉元素。", gallery_img_3)}
    </div>
    """)


def render_cta():
    html(f"""
    <section class="cta reveal">
        <div class="cta-title">以现代官网语言，重新展示传统文创产业</div>
        <div class="cta-desc">
            这个版本已经为后续详情页、非遗专题、产品图库、新闻动态和会员系统预留结构。
            你可以先用 query 页面视图开发，最后再拆成 Streamlit 多页面项目。
        </div>
        <a class="hero-button-primary" href="{page_url('login')}" target="_self">创建账户</a>
    </section>
    """)


def render_footer():
    html("""
    <footer class="footer-custom">
        <div>© 2026 华夏百工 · Traditional Craft Cultural Creative Studio</div>
        <div>Handcraft · Magnet · Artifact · Bracelet</div>
    </footer>
    """)


def render_home():
    render_hero()
    render_about_section()
    render_stats_section()
    render_features_section()
    render_products_section()
    render_story_section()
    render_gallery_section()
    render_chart_section()
    render_cta()


# =============================
# 通用详情页
# =============================
def render_page_hero(title, kicker, desc, bg_img=None):
    style = image_bg(bg_img)
    html(f"""
    <section class="page-hero reveal" style='{style}'>
        <div class="page-content">
            <a class="back-link" href="{page_url('home')}" target="_self">← 返回首页</a>
            <div class="eyebrow">{kicker}</div>
            <div class="page-title">{title}</div>
            <div class="page-desc">{desc}</div>
        </div>
    </section>
    """)


def render_template_cards():
    html("""
    <section class="section">
        <div class="section-center reveal">
            <div class="section-kicker">PAGE TEMPLATE</div>
            <div class="section-title">这个详情页可以继续添加什么？</div>
            <div class="section-desc">下面是预留的内容模块，你之后可以直接复制扩展。</div>
        </div>
    </section>
    <div class="template-grid">
        <div class="template-card reveal">
            <div class="template-title">01 · 内容介绍</div>
            <div class="template-desc">放产品故事、文化来源、工艺背景、材质信息和设计理念。</div>
        </div>
        <div class="template-card reveal">
            <div class="template-title">02 · 图片图库</div>
            <div class="template-desc">放 3-6 张产品图或工艺细节图，形成更完整的视觉展示。</div>
        </div>
        <div class="template-card reveal">
            <div class="template-title">03 · 数据/互动</div>
            <div class="template-desc">加入图表、筛选、登录后收藏、留言或后台管理功能。</div>
        </div>
    </div>
    """)


def render_product_detail(product):
    render_page_hero(
        product["title"],
        f"PRODUCT DETAIL · {product['tag']}",
        product["long_desc"],
        product["image"]
    )
    html(f"""
    <section class="section">
        <div class="detail-grid">
            <div class="detail-card reveal">
                <div class="detail-title">内容定位</div>
                <div class="detail-text">
                    {product["desc"]} 这里目前是详情页雏形，后续可以加入更完整的图片、文字、图表和互动功能。
                </div>
                <div class="pill-row">
                    {chips(product["keywords"])}
                </div>
            </div>
            <div class="detail-card dark reveal">
                <div class="detail-title">下一步扩展方向</div>
                <div class="detail-text">
                    可以继续添加：产品编号、系列名称、材质、尺寸、设计来源、工艺流程、文化寓意、图库、相关新闻、相似内容推荐。
                </div>
                <div class="pill-row">
                    <span class="pill">详情页</span>
                    <span class="pill">图库</span>
                    <span class="pill">数据库预留</span>
                </div>
            </div>
        </div>
    </section>
    """)
    render_template_cards()
    render_products_section()


def render_about_page():
    render_page_hero(
        "产业介绍",
        "INDUSTRY OVERVIEW",
        "这里是产业介绍的独立页面入口。未来可以加入行业背景、非遗产业链、地域文化资源、品牌定位和市场分析。",
        hero_img
    )
    render_about_section()
    render_stats_section()
    render_template_cards()


def render_features_page():
    render_page_hero(
        "核心价值",
        "CORE VALUE",
        "这里可以详细解释华夏百工如何把文化内容、现代视觉、产品系统和用户体验连接起来。",
        workshop_img
    )
    render_features_section()
    render_story_section()
    render_template_cards()


def render_products_page():
    render_page_hero(
        "文创产品矩阵",
        "PRODUCT SYSTEM",
        "这里是产品总览页面。每个产品卡片都已经链接到自己的详情页，适合继续扩展产品图库和产品介绍。",
        hero_img
    )
    render_products_section()
    render_gallery_section()
    render_template_cards()


def render_stories_page():
    render_page_hero(
        "非遗专题",
        "HERITAGE STORIES",
        "这里是非遗专题页的入口。你可以把它扩展成文章列表、匠人故事、工艺流程或文化地图。",
        workshop_img
    )
    render_story_section()
    render_gallery_section()
    render_template_cards()


def render_login_page():
    render_page_hero(
        "登录 / 注册",
        "ACCOUNT SYSTEM",
        "这里目前是展示型表单。后续可以接入数据库、用户权限、收藏夹、后台管理和会员系统。",
        hero_img
    )

    html("""
    <section class="section">
        <div class="section-center reveal">
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
        <div class="auth-panel reveal">
            <div class="auth-title">用户登录</div>
            <div class="auth-desc">进入华夏百工的会员展示系统。</div>
        </div>
        """)
        st.text_input("登录用户名", placeholder="请输入用户名", key="login_user")
        st.text_input("登录密码", placeholder="请输入密码", type="password", key="login_password")
        st.button("登录", use_container_width=True)

    with right_auth:
        html("""
        <div class="auth-panel reveal">
            <div class="auth-title">用户注册</div>
            <div class="auth-desc">创建账户以体验后续扩展功能。</div>
        </div>
        """)
        st.text_input("注册用户名", placeholder="设置用户名", key="register_user")
        st.text_input("注册密码", placeholder="设置密码", type="password", key="register_password")
        st.text_input("确认密码", placeholder="再次输入密码", type="password", key="register_password_confirm")
        st.button("注册", use_container_width=True)

    render_template_cards()


# =============================
# 渲染入口
# =============================
render_nav()

product_lookup = {product["slug"]: product for product in PRODUCTS}

if current_page == "home":
    render_home()
elif current_page == "about":
    render_about_page()
elif current_page == "features":
    render_features_page()
elif current_page == "products":
    render_products_page()
elif current_page == "stories":
    render_stories_page()
elif current_page == "login":
    render_login_page()
elif current_page in product_lookup:
    render_product_detail(product_lookup[current_page])
else:
    render_page_hero(
        "页面未找到",
        "404",
        "这个链接还没有对应内容。你可以返回首页，或者在代码里为这个 page 参数添加新的 render 函数。",
        hero_img
    )

render_footer()
