from trame.app import dev
from trame.ui.vuetify import VAppLayout, SinglePageWithDrawerLayout
from trame.widgets import vuetify, paraview, simput, html

from trame_simput import get_simput_manager

from paraview import simple

# from pv_visualizer import html as my_widgets
from pv_visualizer.app.assets import asset_manager
from pv_visualizer.app.ui import (
    pipeline,
    files,
    algorithms,
    settings,
    view_toolbox,
    state_change,
)


def _reload():
    dev.reload(
        pipeline,
        files,
        algorithms,
        settings,
        view_toolbox,
        state_change,
    )


# -----------------------------------------------------------------------------
# Common style properties
# -----------------------------------------------------------------------------

COMPACT = {
    "dense": True,
    "hide_details": True,
}

CONTROLS = [
    pipeline,
    files,
    algorithms,
    settings,
]

# -----------------------------------------------------------------------------
# Dynamic reloading
# -----------------------------------------------------------------------------

LIFE_CYCLES = [
    "on_data_change",
    "on_active_proxy_change",
]

# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------

class CustomSPADrawerLayout(VAppLayout):

    def __init__(self, _server, template_name="main", **kwargs):
        super().__init__(_server, template_name=template_name, **kwargs)
            
        with self:
            print("self.root ",self.root)
            with vuetify.VAppBar(
                app=True, 
                color="transparent",
                collapse=True,
                #classes="float-left"
                ) as toolbar:
                vuetify.VSpacer()
                self.toolbar = toolbar
                self.title = vuetify.VToolbarTitle("Trame application", color="red")
                self.icon = vuetify.VAppBarNavIcon()
            self.content = vuetify.VLayout()
            # with vuetify.VFooter(app=True, classes="my-0 py-0") as footer:
            #     self.footer = footer
            #     vuetify.VProgressCircular(
            #         indeterminate=("!!trame__busy",),
            #         background_opacity=1,
            #         bg_color="#01549b",
            #         color="#04a94d",
            #         size=16,
            #         width=3,
            #         classes="ml-n3 mr-1",
            #     ),
            #     footer.add_child(
            #         '<a href="https://kitware.github.io/trame/" class="grey--text lighten-1--text text-caption text-decoration-none" target="_blank">Powered by trame</a>'
            #     )
            #     vuetify.VSpacer()
            #     reload = self.server.controller.on_server_reload
            #     if reload.exists():
            #         with vuetify.VBtn(
            #             x_small=True,
            #             icon=True,
            #             click=self.on_server_reload,
            #             classes="mx-2",
            #         ):
            #             vuetify.VIcon("mdi-autorenew", x_small=True)

            #     with vuetify.VTooltip(top=True):
            #         with vuetify.Template(v_slot_activator="{on, attrs}"):
            #             vuetify.VIcon(
            #                 "mdi-help-circle",
            #                 x_small=True,
            #                 classes="mr-4",
            #                 v_bind="attrs",
            #                 v_on="on",
            #                 __properties=[("v_bind", "v-bind"), ("v_on", "v-on")],
            #             )
            #         html.Pre(get_trame_versions())

            #     footer.add_child(
            #         '<a href="https://www.kitware.com/" class="grey--text lighten-1--text text-caption text-decoration-none" target="_blank">© 2021 Kitware Inc.</a>'
            #     )
    
    def on_server_reload(self):
        self.server.controller.on_server_reload(self.server)

def initialize(server):

    state, ctrl = server.state, server.controller

    # state
    state.trame__title = "Visualizer"
    state.trame__favicon = asset_manager.icon

    # controller
    ctrl.on_server_reload.add(_reload)
    ctrl.on_data_change.add(ctrl.view_update)
    ctrl.on_data_change.add(ctrl.pipeline_update)

    # Init other components
    state_change.initialize(server)
    for m in CONTROLS:
        m.initialize(server)

    # simput
    simput_manager = get_simput_manager("pxm")
    simput_widget = simput.Simput(
        simput_manager,
        prefix="pxm",
        trame_server=server,
        ref="simput",
        query=("search", ""),
    )
    ctrl.pxm_apply = simput_widget.apply
    ctrl.pxm_reset = simput_widget.reset

    # with SinglePageWithDrawerLayout(server, show_drawer=True, width=300) as layout:

    html = """
<div style="background-color:grey;color:white;padding:20px;">
  <h2>London</h2>
  <p>London is the capital city of England. It is the most populous city in the United Kingdom, with a metropolitan area of over 13 million inhabitants.</p>
  <p>Standing on the River Thames, London has been a major settlement for two millennia, its history going back to its founding by the Romans, who named it Londinium. London is the capital city of England. It is the most populous city in the United Kingdom, with a metropolitan area of over 13 million inhabitants.</p>
</div> 
"""

    """
    https://github.com/vuetifyjs/vuetify/issues/11378
    https://codepen.io/Mert75/pen/bGpEjVP
    https://ej2.syncfusion.com/vue/documentation/treeview/how-to/customize-the-expand-and-collapse-icons
    https://buttercms.com/blog/build-a-beautiful-animated-news-app-with-vuejs-and-vuetify/
    https://stackoverflow.com/questions/51902929/vuetifyjs-toolbar-overlays-content-as-soon-as-fixed-prop-gets-added
    https://vuetifyjs.com/en/components/app-bars/

    """
    with CustomSPADrawerLayout(server) as layout:
        
            
        layout.content.add_child(html)
        

        # with layout.content:
        #     with vuetify.VContainer(fluid=True, classes="pa-0 fill-height") as c:
        #         c.root.add_child(html)
                    #pass
        
        print(layout)
        #pass

        # layout.root = simput_widget


        
        # -----------------------------------------------------------------------------
        # Toolbar
        # -----------------------------------------------------------------------------
        
        #layout.title.set_text("Visualizer")

        # with layout.icon as icon:
        #     html.Img(src=asset_manager.icon, height=40)
        #     icon.click = None

        # with layout.toolbar as tb:
        #     tb.dense = True
        #     tb.clipped_right = True
        #     vuetify.VSpacer()
        #     vuetify.VTextField(
        #         v_show=("!!active_controls",),
        #         v_model=("search", ""),
        #         clearable=True,
        #         outlined=True,
        #         filled=True,
        #         rounded=True,
        #         prepend_inner_icon="mdi-magnify",
        #         style="max-width: 30vw;",
        #         **COMPACT,
        #     )
        #     vuetify.VSpacer()
        #     with vuetify.VBtnToggle(
        #         v_model=("active_controls", "files"),
        #         **COMPACT,
        #         outlined=True,
        #         rounded=True,
        #     ):
        #         for item in CONTROLS:
        #             with vuetify.VBtn(value=item.NAME, **COMPACT):
        #                 vuetify.VIcon(item.ICON, **item.ICON_STYLE)

        # -----------------------------------------------------------------------------=
        # Drawer
        # -----------------------------------------------------------------------------
        # with layout.drawer as dr:
        #     dr.right = True
        #     # dr.expand_on_hover = True
        #     for item in CONTROLS:
        #         item.create_panel(server)

        # -----------------------------------------------------------------------------
        # Main content
        # -----------------------------------------------------------------------------
        # with layout.content:
        #     with vuetify.VContainer(fluid=True, classes="fill-height pa-0 ma-0"):
        #         view_toolbox.create_view_toolbox(server)
        #         html_view = paraview.VtkRemoteLocalView(
        #             simple.GetRenderView() if simple else None,
        #             interactive_ratio=("view_interactive_ratio", 1),
        #             interactive_quality=("view_interactive_quality", 70),
        #             mode="remote",
        #             namespace="view",
        #             style="width: 100%; height: 100%;",
        #         )
        #         ctrl.view_replace = html_view.replace_view
        #         ctrl.view_update = html_view.update
        #         ctrl.view_reset_camera = html_view.reset_camera
        #         ctrl.on_server_ready.add(ctrl.view_update)

        # -----------------------------------------------------------------------------
        # Footer
        # -----------------------------------------------------------------------------
        # layout.footer.hide()
