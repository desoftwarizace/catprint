import streamlit as st
import asyncio
import catprint
import PIL.Image
from time import gmtime, strftime
import importlib.resources

st.set_page_config(
    page_title="🐈🖨️",
    page_icon="🐈",
    initial_sidebar_state="expanded",
)

if 'blocks' not in st.session_state:
    st.session_state.blocks = []

st.title("🐈🖨️")

st.checkbox(
    "Include IKEA template (logo + header + footer)",
    value=True,
    key="include_ikea_template",
)

if not st.session_state.blocks:
    st.info("Use the buttons below to add content blocks.")

for i, block in enumerate(st.session_state.blocks):
    with st.container():
        col_content, col_actions = st.columns([4, 1], vertical_alignment="center")
        
        with col_content:
            if block['type'] == 'image':
                uploaded_file = st.file_uploader(
                    f"Image Block #{i+1}",
                    type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'],
                    key=f"image_{block['id']}"
                )
                if uploaded_file is not None:
                    try:
                        st.session_state.blocks[i]['data'] = catprint.render.image(PIL.Image.open(uploaded_file))
                    except Exception as e:
                        st.error(f"Error loading image: {e}")
            
            elif block['type'] == 'text':
                widget_key = f"text_{block['id']}"
                if widget_key in st.session_state:
                    current_value = st.session_state[widget_key]
                else:
                    current_value = block['data']
                
                text_content = st.text_area(
                    f"Text Block #{i+1}",
                    value=current_value,
                    height=100,
                    key=widget_key
                )
                st.session_state.blocks[i]['data'] = text_content
            
            elif block['type'] == 'banner':
                widget_key = f"banner_{block['id']}"
                if widget_key in st.session_state:
                    current_value = st.session_state[widget_key]
                else:
                    current_value = block['data']
                
                banner_content = st.text_input(
                    f"Banner Block #{i+1}",
                    value=current_value,
                    key=widget_key
                )
                st.session_state.blocks[i]['data'] = banner_content
        
        with col_actions:
            if st.button("🗑️", key=f"delete_{block['id']}", help="Delete this block"):
                st.session_state.blocks.pop(i)
                st.rerun()

            if i > 0:
                if st.button("⬆️", key=f"up_{block['id']}", help="Move up"):
                    st.session_state.blocks[i], st.session_state.blocks[i-1] = st.session_state.blocks[i-1], st.session_state.blocks[i]
                    st.rerun()

            if i < len(st.session_state.blocks) - 1:
                if st.button("⬇️", key=f"down_{block['id']}", help="Move down"):
                    st.session_state.blocks[i], st.session_state.blocks[i+1] = st.session_state.blocks[i+1], st.session_state.blocks[i]
                    st.rerun()

        st.divider()

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("➕ Image", use_container_width=True):
        st.session_state.blocks.append({
            'id': len(st.session_state.blocks),
            'type': 'image',
            'data': None
        })
        st.rerun()

with col2:
    if st.button("➕ Text", use_container_width=True):
        st.session_state.blocks.append({
            'id': len(st.session_state.blocks),
            'type': 'text',
            'data': ''
        })
        st.rerun()

with col3:
    if st.button("➕ Banner", use_container_width=True):
        st.session_state.blocks.append({
            'id': len(st.session_state.blocks),
            'type': 'banner',
            'data': ''
        })
        st.rerun()

START = """\

IKEA Česká republika, s.r.o.
Prodejna ASGARD,   Roseč 1,   378 46 Roseč
IČO 1337      DIČO 8008135      PYČO 69420
******************************************

"""

END = f"""\

Číslo pokladní:   0xDEADBEEF
Datum      Čas       Obchod  POS   Transak
{strftime("%Y-%m-%d %H:%M:%S", gmtime())}  42      34        007
Číslo dokladu:
123-456-789-{strftime("%Y%m%d%H%M%S", gmtime())}
******************************************
catprint v0.0.0 running on PufOS
******************************************
DATUM VYSTAVENÍ JE DATUM ZDANIT.PLNĚNÍ
USCHOVEJTE PRO REKLAMACI! *DĚKUJEME*
Číslo provozovny: -1
Pokrmy jsou určené k okamžité spotřebě
"""

rendered_blocks = []
if st.session_state.get('include_ikea_template', True):
    with importlib.resources.path("catprint.assets", "ikea.png") as logo_path:
        rendered_blocks.append(catprint.render.image(PIL.Image.open(logo_path)))
    rendered_blocks.append(catprint.render.text(START))
for block in st.session_state.blocks:
    if block['type'] == 'image' and block['data'] is not None:
        rendered_blocks.append(block['data'])
    elif block['type'] == 'text' and block['data'].strip():
        rendered_blocks.append(catprint.render.text(block['data']))
    elif block['type'] == 'banner' and block['data'].strip():
        rendered_blocks.append(catprint.render.text_banner(block['data']))
if st.session_state.get('include_ikea_template', True):
    rendered_blocks.append(catprint.render.text(END))
preview_img = catprint.render.stack(*rendered_blocks) if rendered_blocks else None

if preview_img is not None:
    st.sidebar.image(preview_img, caption="Live Preview", use_container_width=True)
    if st.button("🖨️ Print Receipt", type="primary", use_container_width=True):
        with st.spinner("Printing..."):
            asyncio.run(catprint.printer.print(preview_img))
        st.success("✅ Printing done!")
