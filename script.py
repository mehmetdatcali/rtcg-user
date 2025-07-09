import js
import json
import asyncio

KEYS = {
    "politika": "siyaset",
    "ekonomija": "ekonomi",
    "društvo": "toplum",
    "region": "bölge",
    "svijet": "dünya",
    "turizam": "turizm"
    }

async def load():
    r = await js.fetch("db.json")
    return json.loads(await r.text())

def match(c):
    return KEYS.get(c, c)

def card(i, it):
    open_status = "is-open" if i == 0 else ""
    aria_expanded = str(i == 0).lower()
    aria_hidden = "true" if i != 0 else "false"

    return f"""
    <div class="item {open_status}" data-idx="{i}">
        <button class="item-button" aria-expanded="{aria_expanded}" aria-controls="c-{i}">
            <div class="item-text">
                <!-- item-meta için div etiketi kullanıldı -->
                <div class="item-meta">
                    <p>
                        <span class="material-symbols-outlined" aria-hidden="true">attach_file</span>{match(it.get('category'))}
                        <span class="material-symbols-outlined" aria-hidden="true">calendar_month</span>{it.get('date')[0:10]}
                        <span class="material-symbols-outlined" aria-hidden="true">schedule</span>{it.get('date')[10:-3]}
                    </p>
                </div>
                <h3 class="item-title">{it.get('title')}</h3>
            </div>
            <img src="{it.get('image')}" alt="{it.get('title')}" class="item-image">
        </button>
        <div class="item-content" id="c-{i}" aria-hidden="{aria_hidden}">
            <div class="item-content-inner">
                <p>{it.get('content')}</p>
                <!-- İkon ve bağlantı aynı p etiketi içinde ve ikon bağlantının içine taşındı -->
                <p>
                    <a href="{it.get('link')}" target="_blank" rel="noopener noreferrer">
                        <span class="material-symbols-outlined" aria-hidden="true">open_in_new</span>
                        RTCG
                    </a>
                </p>
            </div>
        </div>
    </div>"""

def render(items):
    el = js.document.querySelector(".items")
    el.innerHTML = "".join(card(i, it) for i, it in enumerate(items))
    # İlk açık öğenin içeriğini doğru yüksekliğe ayarlar
    first = el.querySelector(".item.is-open .item-content")
    if first:
        first.style.maxHeight = f"{first.scrollHeight}px"

def navbar(items):
    el = js.document.querySelector(".nav ul")
    categories = {(i.get("category")) for i in items if i.get("category")}
    el.innerHTML = '<li><a href="#" data-category="all" class="active">gündem</a></li>' + "".join(
        f'<li><a href="#" data-category="{c}">{match(c)}</a></li>' for c in (categories))

    def click(e):
        e.preventDefault()
        a = e.target.closest("a")
        if not a: return

        for x in el.querySelectorAll("a"): x.classList.remove("active")
        a.classList.add("active")
        c = a.dataset.category

        render(items if c == "all" else [i for i in items if i.get("category") == c])
        js.window.scroll({"top": 0, "behavior": "smooth"})
        
    el.addEventListener("click", click)

def accordion(e):
    h = e.target.closest(".item-button")
    if not h: return
    i = h.closest(".item")
    c = i.querySelector(".item-content")
    open = i.classList.contains("is-open")

    for x in js.document.querySelectorAll(".items .item"):
        x.classList.remove("is-open")
        x.querySelector(".item-content").style.maxHeight = "0px"
        x.querySelector(".item-button").setAttribute("aria-expanded", "false")
        x.querySelector(".item-content").setAttribute("aria-hidden", "true")

    if not open:
        i.classList.add("is-open")
        c.style.maxHeight = f"{c.scrollHeight}px"
        h.setAttribute("aria-expanded", "true")
        c.setAttribute("aria-hidden", "false")

async def app():
    response = await load()
    navbar(response)
    render(response)
    js.document.querySelector(".items").addEventListener("click", accordion)

asyncio.create_task(app())