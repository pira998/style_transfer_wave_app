from h2o_wave import Q, app, ui, data

config = {
    "app_title": "Mystique(Style Transfer)",
    "sub_title": "",
    "footer_text": 'Copyright © 2022 by Piraveen Sivakumar ',
    'description': "Transfer Learning is a technique of using a trained model to solve another related task. It is a Machine Learning research method that stores the knowledge gained while solving a particular problem and use the same knowledge to solve another different yet related problem. This improves efficiency by reusing the information gathered from the previously learned task."
}

async def initialize_app(q):
    q.user.font_color = '#83EEFF'
    q.user.primary_color = '#83EEFF'
    if q.user.config is None:
        q.user.config = config
        q.user.default_config = config
        q.client.selected_tab = 'home_tab'

    if q.user.logo is None:
        q.user.logo, = await q.site.upload(['static/h2o_logo.png'])
        q.user.home_image, = await q.site.upload(['static/home_static.jpeg'])
        q.user.about_image, = await q.site.upload(['static/HOME.png'])
        q.user.logo_height = '50'
     
    q.user.init = True 

def create_layout(q: Q, tag=None):
    config = q.user.config
    q.page.drop()

    q.page['header'] = ui.header_card(
        box='header',
        title=config['app_title'],
        subtitle=config['sub_title'],
        icon='TFVCLogo',
        icon_color='#222',
        items=[
            ui.text(
                """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">
                """
            ),
            # ui.text("<img src='"+q.user.logo+"' width='"+ str(q.user.logo_height)+"px'>"),
        ],
    )
    nav_items = [
            ui.tab(name='home_tab', label='Home', icon='Home'),
            ui.tab(name='about_tab', label='About', icon='info'),
            ]
    if q.client.generate_dashboard:
        nav_items += [
            ui.tab(name='#', label='', icon='BulletedListBulletMirrored'),
            ui.tab(name='dashboard_tab', label='Dashboard', icon='Processing'),
        ]

    navbar_items = [ui.inline(items=[
        ui.tabs(name='tabs', value=q.args.tabs, link=True, items=nav_items)
    ])]

    q.page['navbar'] = ui.form_card(box=ui.box(zone='navbar'), title='', items=navbar_items)
    q.page['footer'] = ui.footer_card(box='footer', caption=config['footer_text'])

    
    zones = [ui.zone(name='content_0', size='800px', direction='row')]
        
    if tag in ['feature']:
        zones = [
            ui.zone(name='content_0', size='500px', direction = 'row'),
            ui.zone(name='content_1', size='500px', direction = 'row'),
        
        ]
    elif tag == 'about':
        zones = [ui.zone(name='content_0', size='1100px', direction='row')]

    else:
        pass


    q.page['meta'] = ui.meta_card(box='',
                                  themes=[ui.theme(
                                        name='cdark',
                                        primary=q.user.primary_color,
                                        text=q.user.font_color,
                                        card='#000',
                                        page='#1b1d1f',
                                    )],
                                  theme='cdark',
                                  title= config['app_title'] ,
                                  # stylesheet=ui.inline_stylesheet(style),
                                  layouts=[
                                      ui.layout(
                                                breakpoint='l',
                                                width='1600px',
                                                zones=[
                                                    ui.zone(name='header', size='75px', direction='row'),
                                                    ui.zone(name='navbar', size='90px', direction='row'),
                                                    ui.zone(name='content', zones = zones),
                                                    ui.zone('footer'),
                                                ])
                                  ])

