from paraview.web import venv  # Available in PV 5.10-RC2+
from paraview import simple

from pathlib import Path
from trame.app import get_server
from trame.widgets import vuetify, paraview, client
from trame.ui.vuetify import SinglePageLayout

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
server.client_type = "vue2"
state, ctrl = server.state, server.controller

# Preload paraview modules onto server
paraview.initialize(server)

# -----------------------------------------------------------------------------
# ParaView code
# -----------------------------------------------------------------------------


def load_data(**kwargs):
    # CLI
    #args, _ = server.cli.parse_known_args()

    #full_path = str(Path(args.data).resolve().absolute())
    #working_directory = str(Path(args.data).parent.resolve().absolute())
    
    working_directory = Path(__file__).with_name("data")
    full_path = working_directory / "pv-state-diskout.pvsm"
    #full_path = full_path.absolute()
    
    print("working_directory:", str(working_directory))
    print("full_path        :", str(full_path))
    
    # ParaView
    simple.LoadState(
        str(full_path),
        data_directory=str(working_directory),
        restrict_to_data_directory=True,
    )
    view = simple.GetActiveView()
    view.MakeRenderWindowInteractor(True)
    simple.Render(view)

    # HTML
    with SinglePageLayout(server) as layout:
        layout.icon.click = ctrl.view_reset_camera
        layout.title.set_text("ParaView State Viewer")

        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                html_view = paraview.VtkRemoteView(view)
                ctrl.view_reset_camera = html_view.reset_camera
                ctrl.view_update = html_view.update


ctrl.on_server_ready.add(load_data)

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

state.trame__title = "State Viewer"

with SinglePageLayout(server) as layout:
    layout.icon.click = ctrl.view_reset_camera
    layout.title.set_text("ParaView State Viewer")

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            client.Loading("Loading state")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    #server.cli.add_argument("--data", help="Path to state file", dest="data")
    server.start()
