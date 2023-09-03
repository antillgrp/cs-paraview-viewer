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
    #view_toolbox,
    state_change,
)
#from pip._vendor.rich import print


def _reload():
    dev.reload(
        pipeline,
        files,
        algorithms,
        settings,
        #view_toolbox,
        state_change,
    )

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

def create_main_toolbox(TOOLS):
    
    with html.Div(
                color="transparent",
                classes="d-flex justify-center pt-4 pl-4",
                style="position: absolute; z-index: 1;"
            ):
        for toolDict in TOOLS:
            with vuetify.VTooltip(bottom=True):
                with vuetify.Template(v_slot_activator="{ on, attrs }"):
                    with vuetify.VBtn(
                        v_bind="attrs",
                        v_on="on",
                        fab=True,
                        elevation=3,
                        rounded=True,
                        small=True,
                        click=toolDict["clickFn"],
                        icon=True,
                    ):
                        vuetify.VIcon(toolDict["iconName"])
                html.Span(toolDict["tooltipTxt"]) 
            vuetify.VSpacer(classes="pa-1")
        vuetify.VSpacer(classes="pa-1")
        vuetify.VTextField(
                v_show=("!!active_controls",), # https://bit.ly/3r1lmn5
                # in JS a double exclamation mark (!!) it’s short way to 
                # cast a variable to be a Boolean (true or false) value. 
                v_model=("search", ""),
                clearable=True,
                outlined=True,
                filled=True,
                rounded=True,
                prepend_inner_icon="mdi-magnify",
                dense= True,
                hide_details= True,
            )
                    
def initialize(server):
    
    #state, ctrl = server.state, server.controller

    # state
    server.state.trame__title = "Visualizer"
    #state.trame__favicon = asset_manager.icon

    # controller
    server.controller.on_server_reload.add(_reload)
    server.controller.on_data_change.add(
            server.controller.view_update
        )
    server.controller.on_data_change.add(
            server.controller.pipeline_update
        )

    # simput
    simput_manager = get_simput_manager("pxm")
    simput_widget = simput.Simput(
            simput_manager,
            prefix="pxm",
            trame_server=server,
            ref="simput",
            query=("search", ""),
        )
    server.controller.pxm_apply = simput_widget.apply
    server.controller.pxm_reset = simput_widget.reset
    
    # from pprint import pprint
    # import inspect
    # print("server.state:")
    # pprint(inspect.getmembers(server.state))
    
    # Init other components
    state_change.initialize(server)
    
    @server.state.change("img_file")
    def update_img_file(img_file, **kwargs):
        print("update_img_file:", img_file)
        # server.controller.view_update()
    
    with VAppLayout(server) as layout:
        
        layout.root = simput_widget
       
        layout.on_server_reload = lambda self: self.server.controller.on_server_reload(self.server)
        
        layout.template_name="main"
        drawer_name = f"{layout.template_name}_drawer"
        
        # -----------------------------------------------------------------------------
        # Main ToolBox (replacing ToolBar)
        # -----------------------------------------------------------------------------
                
        """
            {"clickFn": ...,"iconName": ..., "tooltipTxt": ...}
        """
        create_main_toolbox([               
                { 
                    "clickFn": f"{drawer_name} = !{drawer_name}", 
                    "iconName": "mdi-menu", 
                    "tooltipTxt": "ToolBox"
                },
                { 
                    "clickFn": lambda : print("server.controller.files_load_file:", str(server.controller.files_load_file)),  # "alert(img_file)", 
                    "iconName": "mdi-reload", 
                    "tooltipTxt": "Reload"
                },
                { 
                    "clickFn": #debug code
                        """ 
                        console.log(
                            ((obj, indent = 5) => {
                                let cache = [];
                                const retVal = JSON.stringify(
                                    obj,
                                    (key, value) =>
                                    typeof value === 'object' && value !== null
                                        ? cache.includes(value)
                                        ? undefined 
                                        : cache.push(value) && value 
                                        : value,
                                    indent
                                );
                                cache = null;
                                return retVal;
                            })($vuetify.theme)
                        )
                        """, #debug code end
                    "iconName": "mdi-arrow-collapse-all", 
                    "tooltipTxt": "Center to the screen"
                },
                { 
                    "clickFn": "alert(\'Expand to the screen\')", 
                    "iconName": "mdi-arrow-expand-all", 
                    "tooltipTxt": "Expand to the screen"
                },
                { 
                    "clickFn": "alert(\'Take screen shot\')", 
                    "iconName": "mdi-camera-plus", 
                    "tooltipTxt": "Take screen shot"
                },
            ])
        
        #print(layout) #debug
        
        # -----------------------------------------------------------------------------
        # Main Drawer
        # -----------------------------------------------------------------------------
        
        with vuetify.VNavigationDrawer(
                app=True,
                right=True,
                clipped=True,
                stateless=True,
                v_model=(drawer_name, True),
                width=350,
                #color="transparent",
            ):  # as drawer:
                
                common_attrs = {
                        "dense": True,
                        "hide_details": True,
                    }
                
                CONTROLS = [ 
                        files,
                        pipeline,
                        algorithms,
                        settings,
                    ]
                
                # files.VISIBLE = False
                               
                for control in CONTROLS: control.initialize(server)
                
                with html.Div(classes="d-flex justify-center"):
                    
                    vuetify.VTextField(
                            # v_show=("!!active_controls",),
                            v_model=("img_file", "C:\..."),
                            label="Path to .vti file",
                            placeholder="C:\...",
                            hint="Path to .vti file",
                            clearable=True,
                            outlined=True,
                            filled=True,
                            rounded=True,
                            prepend_inner_icon="mdi-file-image",
                            dense= True,
                            hide_details= True,
                            classes="pt-4 pb-4",
                        )
                
                with html.Div(classes="d-flex justify-center"):
                    
                    with vuetify.VBtnToggle(
                            v_model=(
                                "active_controls", 
                                #The first visible
                                next(filter(lambda c: c.VISIBLE, CONTROLS)).NAME
                            ),
                            **common_attrs,
                            outlined=True,
                            rounded=True,
                            classes="pt-4 pb-4",
                        ):
                            for control in CONTROLS:
                                if(control.VISIBLE): 
                                    with vuetify.VBtn(value=control.NAME, **common_attrs):
                                        vuetify.VIcon(control.ICON, **control.ICON_STYLE)
                
                with html.Div(classes="d-flex justify-center"):
                    for control in CONTROLS:
                        if(control.VISIBLE): control.create_panel(server)
        
        # -----------------------------------------------------------------------------
        # Main Content
        # -----------------------------------------------------------------------------
        
        # layout.content = vuetify.VMain()
        # debug
        layout.content = html.Div(classes="fill-height pa-0 ma-0", style="border-color: blue;border-style: solid; border-width: thin;")
        
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
                server.controller.view_replace = html_view.replace_view
                server.controller.view_update = html_view.update
                server.controller.view_reset_camera = html_view.reset_camera
                server.controller.on_server_ready.add(
                        server.controller.view_update
                    )
        
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