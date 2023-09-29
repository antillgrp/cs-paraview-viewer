from trame.app import dev
from trame.ui.vuetify import VAppLayout, SinglePageWithDrawerLayout
from trame.widgets import vuetify, paraview, simput, html

from trame_simput import get_simput_manager

from paraview import simple

from pathlib import Path # https://docs.python.org/3/library/pathlib.html

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

class Certscan3DViewer:
    
    # -----------------------------------------------------------------------------
    # Constructor
    # -----------------------------------------------------------------------------
    def __init__(self, server):
        
        self.__srv = server
        
        # self.__LIFE_CYCLES = [
            #         "on_data_change",
            #         "on_active_proxy_change",
            #     ]
        
        state = self.server.state
        ctrlr = self.server.controller
        
        # state
        state.trame__title = "Certscan® 3D Viewer"
        state.trame__favicon = asset_manager.icon

        # controller
        ctrlr.on_data_change.add(ctrlr.view_update)
        ctrlr.on_data_change.add(ctrlr.pipeline_update)
        ctrlr.on_server_reload.add(self.__reload)    
        
        # simput
        self.__simputWidget = simput.Simput(
                get_simput_manager("pxm"),
                prefix="pxm",
                trame_server=server,
                ref="simput",
                query=("search", ""),
            )
        ctrlr.pxm_apply = self.__simputWidget.apply
        ctrlr.pxm_reset = self.__simputWidget.reset

        self.__registerCallbacks()
    
    # -----------------------------------------------------------------------------
    # Properties
    # -----------------------------------------------------------------------------       
    @property
    def server(self):
        return self.__srv
    
    # -----------------------------------------------------------------------------
    # Private methods
    # -----------------------------------------------------------------------------       
    
    # -----------------------------------------------------------------------------
    # Dynamic reloading
    # -----------------------------------------------------------------------------    
    def __reload(**kwargs):
        dev.reload(
                pipeline,
                files,
                algorithms,
                settings,
                #view_toolbox,
                state_change,
            )
        #DEBUG
        print("__reload --> kwargs:", kwargs)
    
    # -----------------------------------------------------------------------------
    # Callbacks --> https://kitware.github.io/trame/guide/tutorial/html.html#callbacks
    # -----------------------------------------------------------------------------      
    def __registerCallbacks(self):
        state = self.server.state
        ctrlr = self.server.controller
        
        @state.change("img_file")
        def update_img_file(img_file, **kwargs):
            # sample D:\CS4-DEV\cs-paraview-viewer\ParaView\vti\sample.vti
            
            vtiFile = Path(img_file)
            if vtiFile.exists() and vtiFile.is_file():
                # print("file found:", img_file) #debug
                # print("file name:", vtiFile.name) #debug
                # print("file suffix:", vtiFile.suffix) #debug
                ctrlr.files_load_file(img_file, False)
            else:
                print("file not found:", img_file)
            
        @state.change("active_controls")
        def update_active_panel(active_controls, **kwargs):
            state.main_drawer = active_controls is not None
        
        @ctrlr.add("on_active_proxy_change")
        def update_active_proxies(**kwargs):
            
            state.active_proxy_view_id = 0
            state.active_proxy_source_id = 0
            state.active_proxy_representation_id = 0
            
            if simple is not None:
                active_view = simple.GetActiveView()
                state.active_proxy_view_id               = active_view.GetGlobalIDAsString()
                if simple.GetActiveSource() is not None:
                    active_source = simple.GetActiveSource()
                    state.active_proxy_source_id         = active_source.GetGlobalIDAsString()
                    state.active_proxy_representation_id = simple.GetRepresentation(proxy=active_source, view=active_view).GetGlobalIDAsString()
                
            # DEBUG
            print("state.active_proxy_view_id           : ", state.active_proxy_view_id)
            print("state.active_proxy_source_id         : ", state.active_proxy_source_id)
            print("state.active_proxy_representation_id : ", state.active_proxy_representation_id)
        
        update_active_proxies()
    
    # -----------------------------------------------------------------------------
    # UI
    # -----------------------------------------------------------------------------
    
    #----------------------------------------------------------------
    # Main ToolBox (replacing ToolBar)
    #----------------------------------------------------------------    
    def __renderMainToolbox(self, TOOLS):
    
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
                
        # TODO will be replaced by passing file info from iframe parent
        with html.Div(
                color="transparent",
                classes="d-flex justify-center pt-2 pb-2 pl-4 pr-4 mb-4",
                style="""
                    position: absolute; bottom: 0; left: 0; z-index: 1;
                    width: 70%; 
                """
                # border-color: red; border-style: solid; border-width: thin; 
            ):
            vuetify.VTextField(
                    # v_show=("!!active_controls",),
                    v_model=("img_file", ""),
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
                )
    
    #----------------------------------------------------------------
    # Main Drawer
    #----------------------------------------------------------------
    def __renderMainDrawer(self, drawer_name):
        
        server = self.server
        
        with vuetify.VNavigationDrawer(
                app=True,
                right=True,
                clipped=True,
                stateless=True,
                v_model=(drawer_name, True),
                width="30vw",
                color="transparent",
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
                
                files.VISIBLE = False
                               
                for control in CONTROLS: 
                    control.initialize(server)
                
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
                            background_color="transparent",
                            title="Toolbox",
                        ):
                            for control in CONTROLS:
                                if(control.VISIBLE):
                                    with vuetify.VTooltip(bottom=True): 
                                        with vuetify.Template(v_slot_activator="{ on, attrs }"):
                                            with vuetify.VBtn(
                                                    v_bind="attrs",
                                                    v_on="on",
                                                    value=control.NAME,
                                                    color="transparent", 
                                                    **common_attrs
                                                ):
                                                vuetify.VIcon(control.ICON, **control.ICON_STYLE)
                                        html.Span(control.NAME)
                
                # with html.Div(classes="d-flex justify-center"):
                #     for control in CONTROLS:
                #         if(control.VISIBLE): control.create_panel(server)
        
    # ---------------------------------------------------------------
    # Public methods
    #----------------------------------------------------------------
    
    #----------------------------------------------------------------
    # Layout
    #----------------------------------------------------------------                    
    def render(self):
        
        server = self.server
        state = self.server.state
        ctrlr = self.server.controller
        
        with VAppLayout(server) as layout:
            
            layout.root = simput_widget = self.__simputWidget
            
            layout.on_server_reload = lambda self: ctrlr.on_server_reload(self.server)
            
            layout.template_name="main"
            
            # layout.content = vuetify.VMain()
            # debug
            layout.content = html.Div(classes="fill-height pa-0 ma-0", style="border-color: blue;border-style: solid; border-width: thin;")
            
            #---------------------------------------------------------------
            # Main Content
            #---------------------------------------------------------------
                        
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
                    ctrlr.view_replace = html_view.replace_view
                    ctrlr.view_update = html_view.update
                    ctrlr.view_reset_camera = html_view.reset_camera
                    ctrlr.on_server_ready.add(ctrlr.view_update)
                    
            drawer_name = f"{layout.template_name}_drawer"
                        
            self.__renderMainDrawer(drawer_name)
            
            self.__renderMainToolbox(
                    [    
                    #   { "clickFn": ...,"iconName": ..., "tooltipTxt": ... }           
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
                    ]
                )
                    
def initialize(server):
    
    Certscan3DViewer(server).render() 
        
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
    