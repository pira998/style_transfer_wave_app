"""
App: Alternative Credit Scoring with Graphs

__version__ : 1.6
__last_updated__ : 12/04/2022

"""

from .utility import *
from .functions.plots import *
from .style import *

from h2o_wave import Q, app, ui, data, main, on, handle_on
from .layout import create_layout, initialize_app, config as global_cfg
from .utility import ui_table_from_df
from .constants import * 

import warnings
warnings.filterwarnings("ignore")

@app('/')
async def serve(q: Q):

	if q.args.reset:
		q.user.init = False

	if q.client.theme_dark == None:
		q.client.theme_dark = True

	if q.user.init != True:
		await initialize_app(q)
	
	if q.client.generate_dashboard == None:
		q.client.generate_dashboard = q.args.generate_dashboard

	if q.args.generate_dashboard == 'generate_dashboard':
		q.args.tabs = 'dashboard_tab'


	
	if q.args.source_img is not None and q.user.source_img != q.args.source_img:
		q.user.source_img = q.args.source_img
		img = q.args.source_img
		q.user.input_image = "./static/" + img
		q.args.tabs = 'dashboard_tab'
	else:
		img = source_image_choice[0]
		q.user.input_image = "./static/" + img

	if q.args.try_your_image:
		q.user.apply_style = False
		if q.user.try_your_image is True:
			q.user.try_your_image = False
		else:
			q.user.try_your_image = True
		q.args.tabs = 'dashboard_tab'

	
	if q.args.apply_style:
		if q.user.try_your_image is True:
			try:
				local_path = await q.site.download(q.args.upload_image[0], './static')
				q.user.input_image = input_image = './static/' + os.path.basename(local_path)
			except:
				q.user.input_image = input_image = "./static/" + img
		else:
			q.user.input_image = input_image = "./static/" + img
		style_name = q.args.style_model
		model = "./src/saved_models/" + style_name + ".pth"
		q.user.output_image = output_image = "./static/" + style_name + "-" + img
		model = load_model(model)     
		stylize(model, input_image, output_image)
		q.user.style_name = q.args.style_model
		q.user.apply_style = q.args.apply_style
		q.args.tabs = 'dashboard_tab'
	if q.user.apply_style:
		q.args.tabs = 'dashboard_tab'

	
	print (q.args)
	details = {}

	
	if q.args.theme_dark is not None and q.args.theme_dark != q.client.theme_dark:
		await update_theme(q)

	elif q.args.tabs == 'about_tab':
		await about_page(q, details)
	elif q.args.tabs == 'dashboard_tab':
		await dashboard_page(q, details)
	else:
		await home_page(q, details)

	await q.page.save()


async def update_theme(q: Q):
	q.client.theme_dark = q.args.theme_dark
	if q.client.theme_dark:
		q.page["meta"].theme = "cdark"
		q.page['header'].icon_color = "#222"
	else:
		q.page["meta"].theme = "light"
		q.page['header'].icon_color = "#fec827"

	q.page["misc"].items[2].toggle.value = q.client.theme_dark
	await q.page.save()


async def home_page(q, details=None):
	cfg = { 
			'tag': 'home', 
			'items' : [ui.text("Home Page")]
		}
	await render_template(q, cfg)


async def about_page(q, details = None):
	cfg = {
		'tag' : 'about',
	}
	await render_template(q, cfg)


async def dashboard_page(q, details=None):
	models = [ui.choice(name=i, label=i)
            for i in models_choice]
	sources = [ui.choice(name=i, label=i)
            for i in source_image_choice]
	image_form = [ui.button(name='try_your_image', label='Try Existing Image' if q.user.try_your_image else 'Try Your Image')]
	if q.user.try_your_image:
		image_form = image_form + [ui.file_upload(
            name='upload_image', label='Upload your image', compact=True),]
	else:
		image_form = image_form + [
			ui.dropdown(trigger = True, popup='always', name = 'source_img', label = 'Source Image', value =q.args.source_img or source_image_choice[0], choices=sources),
		]
	image_form = image_form + [
		ui.dropdown(name='style_model', label='Style Model',
		            value=q.args.style_model or models_choice[0], choices=models),
        ui.button(name='apply_style', label="Apply Style")
	]
	# BASE_URL = 'https://mystique-transfer-learning.herokuapp.com'
	BASE_URL = 'http://localhost:10101'
	local_path_color, = await q.site.upload([q.user.input_image])
	local_path_bw, = await q.site.upload([q.user.output_image if q.user.apply_style else q.user.input_image])
	image_slider_html = '''
<head>
<style>
	html {{
 
}}

*,
*:before,
*:after {{
    box-sizing: inherit;
}}

body {{
    margin: 0;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.container {{
    position: relative;
    width: 900px;
    height: 600px;
    border: 2px solid white;
}}

.container .img {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-size: 900px 100%;
}}

.container .background-img {{
    background-image: url({color});
}}

.container .foreground-img {{
    background-image: url({bw});
    width: 50%;
}}

.container .slider {{
    position: absolute;
    -webkit-appearance: none;
    appearance: none;
    width: 100%;
    height: 100%;
    background: rgba(242, 242, 242, 0.3);
    outline: none;
    margin: 0;
    transition: all 0.2s;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.container .slider:hover {{
    background: rgba(242, 242, 242, 0.1);
}}

.container .slider::-webkit-slider-thumb {{
    -webkit-appearance: none;
    appearance: none;
    width: 6px;
    height: 600px;
    background: white;
    cursor: pointer;
}}

.container .slider::-moz-range-thumb {{
    width: 6px;
    height: 600px;
    background: white;
    cursor: pointer;
}}

.container .slider-button {{
    pointer-events: none;
    position: absolute;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: white;
    left: calc(50% - 18px);
    top: calc(50% - 18px);
    display: flex;
    justify-content: center;
    align-items: center;
}}

.container .slider-button:after {{
    content: "";
    padding: 3px;
    display: inline-block;
    border: solid #5d5d5d;
    border-width: 0 2px 2px 0;
    transform: rotate(-45deg);
}}

.container .slider-button:before {{
    content: "";
    padding: 3px;
    display: inline-block;
    border: solid #5d5d5d;
    border-width: 0 2px 2px 0;
    transform: rotate(135deg);
}}
</style>
<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
</head>

<body>
 <div class='container'>
    <div class='img background-img'></div>
    <div class='img foreground-img'></div>
    <input type="range" min="1" max="100" value="50" class="slider" name='slider' id="slider">
    <div class='slider-button'></div>

  <script>
   $("#slider").on("input change", (e)=>{{
	const sliderPos = e.target.value;
	// Update the width of the foreground image
	$('.foreground-img').css('width', `${{sliderPos}}%`)
	// Update the position of the slider button
	$('.slider-button').css('left', `calc(${{sliderPos}}% - 18px)`)
	}});

  </script>
  

  </div>


</body>
	'''

	image_slider_html = image_slider_html.format(
		color=BASE_URL + local_path_color, bw=BASE_URL + local_path_bw)


	cfg = {
            'tag': 'dashboard',
			'image_form': image_form,
			'image_slider_html': image_slider_html
    }
	await render_template(q, cfg)
	


async def render_template(q: Q, page_cfg):
	
	create_layout(q, tag=page_cfg['tag'])
	
	if page_cfg['tag'] == 'home':
		
		

		q.page['content_left'] = ui.tall_info_card(
					box=ui.box(zone='content_0'),
                    name='generate_dashboard',
					title=global_cfg["app_title"], 
					caption=global_cfg["description"],
					category=global_cfg["sub_title"],
					label='Launch Application',
					image=q.user.home_image,
					image_height='500px'
			)	
	elif page_cfg['tag'] == 'about':
		q.page['content_00'] = ui.form_card(box=ui.box(zone='content_0', width='20%', order=1), title='', items=[])
		q.page['content_01'] = ui.form_card(box=ui.box(zone='content_0', width='80%', order=2), title='', items=[
			ui.image(title='Image title', path=q.user.about_image),
		])
	
	elif page_cfg['tag'] == 'dashboard':
		q.page['content_00'] = ui.form_card(box=ui.box(
			zone='content_0', width='20%', order=1), title='', items=page_cfg['image_form'])
		q.page['content_01'] = ui.frame_card(box=ui.box(
			zone='content_0', width='80%', order=2), title='', content=page_cfg['image_slider_html'])
	await q.page.save()


