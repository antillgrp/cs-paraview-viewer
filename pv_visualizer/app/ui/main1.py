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
from pip._vendor.rich import print


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

    """
    https://github.com/vuetifyjs/vuetify/issues/11378
    https://codepen.io/Mert75/pen/bGpEjVP
    https://ej2.syncfusion.com/vue/documentation/treeview/how-to/customize-the-expand-and-collapse-icons
    https://buttercms.com/blog/build-a-beautiful-animated-news-app-with-vuejs-and-vuetify/
    https://stackoverflow.com/questions/51902929/vuetifyjs-toolbar-overlays-content-as-soon-as-fixed-prop-gets-added
    https://vuetifyjs.com/en/components/app-bars/

    """

    """
    https://codepen.io/gorilla0513/pen/WLaOwQ
    https://www.thisdot.co/blog/making-sense-of-multiple-v-model-bindings-in-vue-3/
    https://learnvue.co/articles/v-model-guide
    https://vuejs.org/guide/components/v-model.html
    https://www.appsloveworld.com/vuejs/100/1/meaning-of-v-slotactivator-on
    https://vuejs.org/api/#v-on

    https://codingbeautydev.com/blog/vuetify-fab/
    https://javascript.plainenglish.io/create-a-beautiful-to-do-list-app-in-vuetify-displaying-the-list-of-tasks-lists-margins-cc0fde2ed2c1
    https://codepen.io/kematzy/pen/oMgrjE

    https://github.com/Kitware/trame-simput
    https://github.com/Kitware/trame-tutorial
    https://github.com/Kitware/trame-cookiecutter
    
    """
    """
    ICONS: https://icon-sets.iconify.design/mdi/account-card-outline/

    https://icon-sets.iconify.design/mdi/
    
    """
    
    with VAppLayout(server) as layout:
        
        layout.on_server_reload = lambda self: self.server.controller.on_server_reload(self.server)
        
        layout.template_name="main"
        drawer_name = f"{layout.template_name}_drawer"
        
        # -----------------------------------------------------------------------------
        # Fav
        # -----------------------------------------------------------------------------
        
        # with vuetify.VCard(
        #     #elevation=3,
        #     color="transparent",
        #     classes="d-flex flex-row rounded-lg pa-0",
        #     style="position: absolute; left: 15px; top: 15px; z-index: 1;",

        # ):
        with html.Div(
                color="transparent",
                classes="d-flex justify-center",
                style="position: absolute; left: 15px; top: 15px; z-index: 1;"
            ):
            with vuetify.VTooltip(bottom=True):
                with vuetify.Template(v_slot_activator="{ on, attrs }"):
                    with vuetify.VBtn(
                        fab=True,
                        elevation=3,
                        #absolute=True,
                        # right=True,
                        # top=True,
                        #outlined=True,
                        rounded=True,
                        small=True,
                        v_bind="attrs",
                        v_on="on",
                        icon=True,
                        click=f"{drawer_name} = !{drawer_name}",
                    ):
                        vuetify.VIcon("mdi-menu")
                html.Span("ToolBox") 
            vuetify.VSpacer(classes="pa-1")   
            with vuetify.VTooltip(bottom=True):
                with vuetify.Template(v_slot_activator="{ on, attrs }"):
                    with vuetify.VBtn(
                        fab=True,
                        elevation=3,
                        #absolute=True,
                        # right=True,
                        # top=True,
                        #outlined=True,
                        rounded=True,
                        small=True,
                        v_bind="attrs",
                        v_on="on",
                        icon=True,
                        click=f"{drawer_name} = !{drawer_name}",
                    ):
                        vuetify.VIcon("mdi-arrow-collapse-all")
                html.Span("ToolBox") 
            vuetify.VSpacer(classes="pa-1")   
            with vuetify.VTooltip(bottom=True):
                with vuetify.Template(v_slot_activator="{ on, attrs }"):
                    with vuetify.VBtn(
                        fab=True,
                        elevation=3,
                        #absolute=True,
                        # right=True,
                        # top=True,
                        #outlined=True,
                        rounded=True,
                        small=True,
                        v_bind="attrs",
                        v_on="on",
                        icon=True,
                        click=f"{drawer_name} = !{drawer_name}",
                    ):
                        vuetify.VIcon("mdi-arrow-expand-all")
                html.Span("ToolBox")
            vuetify.VSpacer(classes="pa-1")        
            with vuetify.VTooltip(bottom=True):
                with vuetify.Template(v_slot_activator="{ on, attrs }"):
                    with vuetify.VBtn(
                        fab=True,
                        elevation=3,
                        #absolute=True,
                        # right=True,
                        # top=True,
                        #outlined=True,
                        rounded=True,
                        small=True,
                        v_bind="attrs",
                        v_on="on",
                        icon=True,
                        click=f"{drawer_name} = !{drawer_name}",
                    ):
                        vuetify.VIcon("mdi-camera-plus")
                html.Span("ToolBox")  
        
        # -----------------------------------------------------------------------------=
        # Drawer
        # -----------------------------------------------------------------------------
       
        with vuetify.VNavigationDrawer(
            app=True,
            right=True,
            clipped=True,
            stateless=True,
            v_model=(drawer_name, True),
            width=300,
            color="transparent",
        ):  # as drawer:
            with html.Div(classes="d-flex justify-center"):
                with vuetify.VBtnToggle(
                    v_model=("active_controls", "files"),
                    **COMPACT,
                    outlined=True,
                    rounded=True,
                ):
                        #with html.Div(classes="d-flex ma-4 align-center justify-space-around"):
                        for item in CONTROLS:
                            with vuetify.VBtn(value=item.NAME, **COMPACT):
                                vuetify.VIcon(item.ICON, **item.ICON_STYLE)
            with html.Div(classes="d-flex justify-center"):
                for item in CONTROLS:
                    item.create_panel(server)
                    
        # -----------------------------------------------------------------------------
        # Main content
        # -----------------------------------------------------------------------------
        
        # layout.content = vuetify.VMain()
        layout.content = html.Div(classes="fill-height pa-0 ma-0", style="border-color: blue;border-style: solid; border-width: thin;")
        #with html.Div(style="border-color: blue;border-style: solid; border-width: thin;"):
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="fill-height pa-0 ma-0"):
                #view_toolbox.create_view_toolbox(server)
                html_view = paraview.VtkRemoteLocalView(
                    simple.GetRenderView() if simple else None,
                    interactive_ratio=("view_interactive_ratio", 1),
                    interactive_quality=("view_interactive_quality", 70),
                    mode="remote",
                    namespace="view",
                    style="width: 100%; height: 100%;",
                )
                ctrl.view_replace = html_view.replace_view
                ctrl.view_update = html_view.update
                ctrl.view_reset_camera = html_view.reset_camera
                ctrl.on_server_ready.add(ctrl.view_update)
        
        print(layout)
        
       
       
